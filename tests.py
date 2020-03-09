import unittest

from word_counter import remove_punctuation, generate_word_bucket, generate_sorted_word_counts, generate_sentence_concordance


class TestUnits(unittest.TestCase):

    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation('What?'), 'What ')
        self.assertEqual(remove_punctuation('What!? is   this?'), 'What   is   this ')

    def test_generate_word_bucket(self):
        self.assertEqual(['what', 'is', 'this'], generate_word_bucket('What!? is   this?'))

    def test_generate_sorted_word_counts(self):
        self.assertEqual([('what', 3), ('is', 2), ('this', 1)],
                         generate_sorted_word_counts({'this': 1, 'is': 2, 'what': 3})
                         )


class TestConcordance(unittest.TestCase):
    def test_simple_concordance(self):
        sentence = 'What!? is   this?'
        concordance = {'what': sentence, 'is': sentence, 'this': sentence}
        self.assertDictEqual(concordance, generate_sentence_concordance(sentence))

    def test_duplicate_word_concordance(self):
        sentence = 'What!? is   this? What this?'
        concordance = {'what': sentence, 'is': sentence, 'this': sentence}
        self.assertDictEqual(concordance, generate_sentence_concordance(sentence))
