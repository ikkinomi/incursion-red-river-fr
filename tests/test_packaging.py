import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from maintenance.package_assistants import verified_images
from installation import fr_manager


class PublicationPrivacyTests(unittest.TestCase):
    def test_distributed_json_matches_installer_manifest(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'installation/manifest.json').read_text(encoding='utf-8'))
        actual = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (root / 'translations/fr').glob('*.json') if not p.name.startswith('_')}
        self.assertEqual(actual, manifest['json_files'])
        self.assertEqual(hashlib.sha256((root / 'patch/Test_C/Content/Paks' / fr_manager.PAK).read_bytes()).hexdigest(), manifest['market_sha256'])

    def test_added_or_changed_capture_requires_new_review(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            approved = folder / 'assistant-fr-installation.jpg'
            approved.write_bytes(b'reviewed demo image')
            (folder / 'PRIVACY.json').write_text(json.dumps({'files': {approved.name: hashlib.sha256(approved.read_bytes()).hexdigest()}}))
            self.assertEqual(verified_images(folder, 'assistant-fr-'), [approved])
            extra = folder / 'assistant-fr-unknown.jpg'
            extra.write_bytes(b'not reviewed')
            with self.assertRaisesRegex(ValueError, 'non approuvée'):
                verified_images(folder, 'assistant-fr-')
            extra.unlink()
            approved.write_bytes(b'changed after review')
            with self.assertRaisesRegex(ValueError, 'non approuvée'):
                verified_images(folder, 'assistant-fr-')
