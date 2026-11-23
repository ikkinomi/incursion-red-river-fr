"""Contrôles hors jeu des traductions. Python standard, aucune correction automatique."""
import argparse
from collections import Counter
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TOKENS = re.compile(r'\{[^{}]*\}|<[^>]*>')
FILES = re.compile(r'\b[\w.-]+\.(?:txt|doc|zip|png|exe|json)\b', re.I)


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load_catalogue(directory, *, todos=False):
    """Lit seulement les fichiers chargés par le jeu, ou ses _Todo si demandé."""
    directory = Path(directory)
    if not directory.is_dir():
        raise ValueError('Dossier de textes introuvable : ' + str(directory))
    paths = sorted(directory.glob('_Todo_*.json' if todos else '*.json'))
    if not todos:
        paths = [p for p in paths if not p.name.startswith('_')]
    rows, issues = {}, []
    for path in paths:
        try:
            doc = json.loads(path.read_text(encoding='utf-8-sig'))
            if not isinstance(doc, dict) or not isinstance(doc.get('texts'), list):
                raise ValueError('Le document doit contenir une liste texts.')
            for index, item in enumerate(doc['texts']):
                if not isinstance(item, dict) or not all(isinstance(item.get(k), str) for k in ('ns', 'key', 'source', 'text')):
                    issues.append({'file': path.name, 'index': index, 'code': 'invalid_row'})
                    continue
                identity = (item['ns'], item['key'])
                if identity in rows:
                    issues.append({'file': path.name, 'key': item['key'], 'code': 'duplicate_identity'})
                    continue
                rows[identity] = dict(item, file=path.name)
        except (OSError, ValueError) as error:
            issues.append({'file': path.name, 'code': 'invalid_file', 'detail': str(error)})
    if not paths:
        issues.append({'code': 'empty_catalogue'})
    return rows, issues, len(paths)


def entry(row, code, **extra):
    return {k: row[k] for k in ('file', 'ns', 'key', 'source', 'text')} | {'code': code} | extra


def contains(text, name, flags=0):
    return re.search(r'(?<!\w)' + re.escape(name) + r'(?!\w)', text, flags) is not None


def checks(rows, rules):
    errors, warnings, lengths = [], [], []
    protected = 0
    names = rules['preserve_names']
    for row in rows.values():
        source, text = row['source'], row['text']
        if not text.strip() and source.strip():
            errors.append(entry(row, 'empty_translation'))
        if '\ufffd' in text:
            errors.append(entry(row, 'replacement_character'))
        if Counter(TOKENS.findall(source)) != Counter(TOKENS.findall(text)):
            errors.append(entry(row, 'format_tokens'))
        if re.findall(r'[\r\n]+', source) != re.findall(r'[\r\n]+', text):
            errors.append(entry(row, 'line_breaks'))
        if any(re.search(pattern, source)[0] != re.search(pattern, text)[0] for pattern in (r'^\s*', r'\s*$')):
            errors.append(entry(row, 'edge_spaces'))
        for name in FILES.findall(source):
            if name not in text:
                errors.append(entry(row, 'filename', expected=name))
        # Capitalisation de la source : « Bunker » carte, « bunker » nom commun.
        for name in names:
            flags = re.I if name == 'NVIDIA Reflex' else 0
            if contains(source, name, flags) or (name in ('Quarry', 'Outskirts', 'Delta', 'Bunker') and contains(source, name.upper())):
                protected += 1
                if not contains(text, name, re.I):
                    errors.append(entry(row, 'protected_name', expected=name))
        for command in re.findall(r'`([^`]+)`', source):
            if command not in text:
                errors.append(entry(row, 'terminal_literal', expected=command))
        if source in rules.get('preserve_exact_sources', []) and 'Boost' not in text:
            errors.append(entry(row, 'protected_option', expected='Boost'))
        # Vérifie le mot isolé seulement : pas de remplacement par sous-chaîne.
        expected = rules.get('glossary', {}).get(source.strip())
        specific = [r for r in rules.get('contextual_rules', []) if r.get('key') == row['key'] and r['source'] == source]
        if specific:
            expected = specific[0]['text']
        elif source == 'Stock':
            expected = 'Crosse'
        if expected and text.strip().casefold() != expected.casefold():
            warnings.append(entry(row, 'glossary_review', proposed=expected))
        if source == text and re.search(r'\b(?:the|your|this|please|with|cannot|press)\b', source, re.I):
            warnings.append(entry(row, 'possibly_english'))
        clean_s = TOKENS.sub('', source).strip()
        clean_t = TOKENS.sub('', text).strip()
        # Heuristique uniquement : sans police ni largeur du widget, aucun débordement n'est prouvé.
        if '\n' not in source and 3 <= len(clean_s) <= 60 and len(clean_t) > max(len(clean_s) * 1.5, len(clean_s) + 8):
            lengths.append(entry(row, 'visual_review', source_length=len(clean_s), text_length=len(clean_t),
                                 priority='haute' if len(clean_s) <= 20 else 'normale'))
    lengths.sort(key=lambda r: (r['priority'] != 'haute', -(r['text_length'] - r['source_length'])))
    return errors, warnings, lengths, protected


def snapshot(rows, english=None):
    def hash_rows(catalogue, include_text):
        return [{'ns': ns, 'key': key, 'source_sha256': sha(row['source']),
                 **({'text_sha256': sha(row['text'])} if include_text else {})}
                for (ns, key), row in sorted(catalogue.items())]
    return {'schema': 1, 'translations': hash_rows(rows, True),
            'english': hash_rows(english, False) if english is not None else None}


def changes(rows, old, include_text=True):
    previous = {(r['ns'], r['key']): r for r in old}
    found = []
    for identity, row in rows.items():
        before = previous.get(identity)
        code = ('new' if before is None else 'source_changed' if sha(row['source']) != before['source_sha256']
                else 'text_changed' if include_text and sha(row['text']) != before['text_sha256'] else None)
        if code:
            found.append(entry(row, code))
    for identity in sorted(previous.keys() - rows.keys()):
        found.append({'ns': identity[0], 'key': identity[1], 'code': 'removed'})
    return found


def audit(translations, rules, english=None, baseline=None, market=None):
    rows, structural, file_count = load_catalogue(translations)
    errors, warnings, lengths, protected = checks(rows, rules)
    errors = structural + errors
    native, coverage, todo = None, [], []
    if english is not None:
        native, native_errors, _ = load_catalogue(english)
        errors += [dict(e, catalogue='english') for e in native_errors]
        for identity, source_row in native.items():
            row = rows.get(identity)
            if row is None:
                coverage.append(entry(source_row, 'missing_translation'))
            elif source_row['source'] != row['source']:
                coverage.append(entry(row, 'stale_source', current_source=source_row['source']))
        errors += coverage
    todo_paths = list(Path(translations).glob('_Todo_*.json'))
    if todo_paths:
        todo_rows, todo_errors, _ = load_catalogue(translations, todos=True)
        todo = [entry(r, 'game_todo', problem=r.get('problem', '')) for r in todo_rows.values()]
        warnings += [dict(e, catalogue='todo') for e in todo_errors]
    market_issues = []
    if market is not None:
        table = json.loads(Path(market).read_text(encoding='utf-8-sig'))
        if not isinstance(table, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in table.items()):
            raise ValueError('Table du marché invalide.')
        for source, text in table.items():
            if ' > ' in source:
                expected = ' > '.join(table.get(p, p) for p in source.split(' > '))
                if text != expected:
                    market_issues.append({'source': source, 'text': text, 'code': 'market_path', 'expected': expected})
            for name in rules['preserve_names']:
                if (contains(source, name) or (name in ('Quarry', 'Outskirts', 'Delta', 'Bunker') and contains(source, name.upper()))) and not contains(text, name, re.I):
                    market_issues.append({'source': source, 'text': text, 'code': 'market_protected_name', 'expected': name})
        errors += market_issues
    previous = json.loads(Path(baseline).read_text(encoding='utf-8-sig')) if baseline else None
    delta = changes(rows, previous['translations']) if previous else []
    english_delta = changes(native, previous['english'], False) if previous and previous.get('english') is not None and native is not None else None
    return {'schema': 1, 'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
            'summary': {'files': file_count, 'entries': len(rows), 'english_entries': len(native) if native is not None else None,
                        'errors': len(errors), 'warnings': len(warnings), 'visual_reviews': len(lengths),
                        'protected_occurrences_checked': protected, 'game_todos': len(todo),
                        'translation_changes': len(delta), 'english_changes': len(english_delta) if english_delta is not None else None},
            'errors': errors, 'warnings': warnings, 'visual_reviews': lengths, 'game_todos': todo,
            'translation_changes': delta, 'english_changes': english_delta,
            'limits': 'Contrôle statique : ni relecture exhaustive ni preuve de débordement. _English reflète le dernier lancement du jeu.',
            'snapshot': snapshot(rows, native)}


def write_report(report, directory):
    directory = Path(directory)
    data = {k: v for k, v in report.items() if k != 'snapshot'}
    dump(directory / 'audit.json', data)
    dump(directory / 'snapshot.json', report['snapshot'])
    dump(directory / 'textes-a-verifier.json', report['visual_reviews'])
    pending = []
    for row in report['errors']:
        if row.get('code') in ('missing_translation', 'stale_source'):
            pending.append({'ns': row['ns'], 'key': row['key'], 'source': row.get('current_source', row['source']),
                            'text': '', 'oldSource': row['source'], 'oldText': row['text']})
    # Fichier de travail hors de fr : ne pas le copier sans relecture et validation.
    dump(directory / 'a-traduire.json', {'texts': pending})
    summary = report['summary']
    lines = ['# Rapport de contrôle', '', *[f'- {k} : {v}' for k, v in summary.items()], '', report['limits'], '',
             'Les avertissements et propositions de glossaire demandent une relecture. Aucune traduction n’a été modifiée.', '',
             '## Textes courts à vérifier à l’écran', '', '| Source | Français | Longueurs |', '|---|---|---|']
    for row in report['visual_reviews'][:30]:
        escape = lambda s: s.replace('|', '\\|').replace('\r', '').replace('\n', ' ')
        lines.append(f"| {escape(row['source'])} | {escape(row['text'])} | {row['source_length']} → {row['text_length']} |")
    (directory / 'RAPPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--translations', type=Path, default=ROOT / 'translations/fr')
    parser.add_argument('--english', type=Path)
    parser.add_argument('--rules', type=Path, default=ROOT / 'docs/REGLES-TRADUCTION.json')
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--market', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    rules = json.loads(args.rules.read_text(encoding='utf-8-sig'))
    report = audit(args.translations, rules, args.english, args.baseline, args.market)
    write_report(report, args.output)
    print(json.dumps(report['summary'], ensure_ascii=False))
    return 1 if report['errors'] else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        print('ERREUR : ' + str(error), file=sys.stderr)
        sys.exit(2)
