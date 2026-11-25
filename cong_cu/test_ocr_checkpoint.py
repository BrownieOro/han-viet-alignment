import argparse
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import ocr_checkpoint as checkpoint


class CheckpointTest(unittest.TestCase):
    def test_resume_and_failed_quota_switch(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'book.pdf'
            pdf.write_bytes(b'dummy pdf')
            keys = root / 'keys'
            keys.write_text('first ' + 'a' * 25 + '\nsecond ' + 'b' * 25 + '\n')
            args = argparse.Namespace(pdf=str(pdf), output=str(root/'out'), start=1, end=2,
                                      work='CPO_05', section='test', keys=str(keys))
            def subprocess_run(command, **kwargs):
                return argparse.Namespace(stdout='Pages: 2\n' if command[0]=='pdfinfo' else b'image')
            replies = [(429, {'error': 'quota', 'retryable': False}),
                       (200, {'text': 'một'}), (200, {'text': 'hai'})]
            with patch.object(checkpoint.subprocess, 'run', side_effect=subprocess_run), \
                 patch.object(checkpoint, 'recognize', side_effect=replies) as ocr:
                self.assertEqual(checkpoint.run(args), 0)
                self.assertEqual(ocr.call_count, 3)
                self.assertEqual(checkpoint.run(args), 0)
                self.assertEqual(ocr.call_count, 3)
            self.assertEqual((root/'out/02_ocr_tho/0001.txt').read_text(), 'một\n')
            self.assertEqual((root/'out/02_ocr_tho/0002.txt').read_text(), 'hai\n')
            args.end = 1
            with self.assertRaises(RuntimeError):
                checkpoint.run(args)

    def test_failure_preserves_completed_page_for_resume(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'book.pdf'; pdf.write_bytes(b'pdf')
            keys = root / 'keys'; keys.write_text('a' * 25 + '\n')
            args = argparse.Namespace(pdf=str(pdf), output=str(root/'out'), start=1, end=2,
                                      work='CPO_03', section='test', keys=str(keys))
            def run_command(command, **kwargs):
                return argparse.Namespace(stdout='Pages: 2\n' if command[0]=='pdfinfo' else b'image')
            with patch.object(checkpoint.subprocess, 'run', side_effect=run_command), \
                 patch.object(checkpoint, 'recognize', side_effect=[(200, {'text':'trang một'}),
                                                                   (422, {'error':'không rõ'})]):
                self.assertEqual(checkpoint.run(args), 1)
            self.assertTrue((root/'out/02_ocr_tho/0001.txt').is_file())
            self.assertFalse((root/'out/02_ocr_tho/0002.txt').exists())
            with patch.object(checkpoint.subprocess, 'run', side_effect=run_command), \
                 patch.object(checkpoint, 'recognize', return_value=(200, {'text':'trang hai'})) as ocr:
                self.assertEqual(checkpoint.run(args), 0)
                self.assertEqual(ocr.call_count, 1)

    def test_selected_pages_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root/'book.pdf'; pdf.write_bytes(b'pdf')
            keys = root/'keys'; keys.write_text('a'*25+'\n')
            args = argparse.Namespace(pdf=str(pdf), output=str(root/'out'), start=1, end=2,
                                      work='CPO_05', section='test', keys=str(keys), skip=[1])
            def run_command(command, **kwargs):
                return argparse.Namespace(stdout='Pages: 2\n' if command[0]=='pdfinfo' else b'image')
            with patch.object(checkpoint.subprocess, 'run', side_effect=run_command), \
                 patch.object(checkpoint, 'recognize', return_value=(200, {'text':'trang hai'})) as ocr:
                self.assertEqual(checkpoint.run(args), 0)
                self.assertEqual(ocr.call_count, 1)
            self.assertFalse((root/'out/01_nguon/0001.png').exists())
            self.assertTrue((root/'out/02_ocr_tho/0002.txt').exists())


if __name__ == '__main__':
    unittest.main()
