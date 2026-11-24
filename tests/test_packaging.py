import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from maintenance.package_assistants import verified_images


class PublicationPrivacyTests(unittest.TestCase):
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
