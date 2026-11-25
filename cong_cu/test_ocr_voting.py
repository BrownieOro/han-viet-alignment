import unittest
from ocr_voting import vote_ocr


class VotingTests(unittest.TestCase):
    def test_majority_and_tie_choose_gemini(self):
        self.assertEqual(vote_ocr('天地入', '天地人', '天地人')['text'], '天地人')
        result = vote_ocr('天地人', '天地入', '天地大')
        self.assertEqual(result['text'], '天地人')
        self.assertEqual(len(result['disagreements']), 1)

    def test_missing_and_added_characters_keep_alignment(self):
        result = vote_ocr('天地人', '天地人民', '天地人民')
        self.assertEqual(result['text'], '天地人民')
        self.assertEqual(result['disagreements'][0]['kind'], 'insertion')
        self.assertEqual(vote_ocr('天地人物', '天地物', '天地物')['text'], '天地物')
        self.assertEqual(vote_ocr('天地人', '天地人民', '天地人')['text'], '天地人')

    def test_engine_failure_is_not_silently_counted(self):
        with self.assertRaises(ValueError):
            vote_ocr('天地', '', '天地')


if __name__ == '__main__':
    unittest.main()
