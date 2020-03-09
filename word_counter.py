from collections import Counter, defaultdict
from typing import Mapping

from textblob import TextBlob

SHOW_TOP_WORDS = 40

COLUMN_WIDTH = 20
SHOW_HIGHLIGHTED_SENTENCE = 40
INTERESTING_CUTOFF = 0.2  # 0-1
NUMBER_DOCUMENTS = 6


def generate_filename(file_number: int):
    """
    >>>generate_filename(4)
    'data/doc4.txt'
    """
    return f'data/doc{file_number}.txt'


def generate_sorted_word_counts(counter: Mapping):
    """
    Given a mapping (dict or Counter say): return a list of tuples
    where the tuple is: ( key, value) sorted in value order
    """
    c: list[tuple] = [(k, counter[k]) for k in counter]
    c.sort(reverse=True, key=lambda ele: ele[1])
    return c


def generate_sentence_concordance(sentence):
    """
    Put all the words in the sentence as keys.
    The dict value is the sentence.

    generate_sentence_concordance('The word is word')
    >>>{
        'The':'The word is word',
        'word':'The word is word',
        'is':'The word is word'
        }
    """
    words = set(TextBlob(sentence).words)
    r = {word: sentence for word in words}
    return r


def generate_word_and_count_concordance():
    """
    Generate:
    * a sorted list of words & frequencies
    * & a concordance (what words are found where)
    for the documents specified
    """
    total_counter = Counter()
    concordance = defaultdict(list)
    for file_number in range(1, NUMBER_DOCUMENTS + 1):
        generate_document_counter(total_counter, file_number)
        generate_document_concordance(concordance, file_number)
    word_counts = generate_sorted_word_counts(total_counter)
    return word_counts, concordance


def generate_document_counter(counter, file_number):
    with open(generate_filename(file_number)) as doc:
        for line in doc.readlines():
            wordlist = TextBlob(line)
            doc_count = Counter(wordlist.words)
            counter.update(doc_count)
    return counter


def generate_document_concordance(concordance, file_number):
    filename = generate_filename(file_number)
    with open(filename) as doc:
        for line in doc.readlines():
            lineconcordance = generate_sentence_concordance(line)
            for key in lineconcordance:
                concordance[key].append({'fn': filename,
                                         'no': file_number,
                                         'line': lineconcordance[key]}
                                        )
        return concordance


def is_interesting(word, sentences):
    """
    'interesting' is a feature of the word and the sentences the word appears in.
    this takes the average of the sentence sentiment + the word sentiment
    if it's larger enough, it's an interesting word.
    """
    sentences_avg = sum([interesting_fragment(sentence['line']) for sentence in sentences]) / len(sentences)
    return (interesting_fragment(word) * sentences_avg) > INTERESTING_CUTOFF


def interesting_fragment(blob):
    return abs(TextBlob(blob).sentiment.polarity)


def output_interesting_words(lim=SHOW_TOP_WORDS):
    word_freqs, concordance = generate_word_and_count_concordance()
    lines_outputted = 0
    for word, qty in word_freqs:
        sentences = concordance[word]
        if is_interesting(word, sentences):
            output_line(sentences, word, qty)
            lines_outputted += 1
        if lines_outputted > lim:
            break


def sentence_fragment(word, sentence):
    sentence = pad_sentence(sentence)
    loc = sentence.find(word)
    startfrom = max(0, loc - SHOW_HIGHLIGHTED_SENTENCE)
    end = min(len(sentence), loc + SHOW_HIGHLIGHTED_SENTENCE)
    frag = sentence[startfrom:end]
    pre_ellision = '' if startfrom < SHOW_HIGHLIGHTED_SENTENCE else '...'
    end_ellision = '' if end > len(sentence) - SHOW_HIGHLIGHTED_SENTENCE else '...'
    return f'{pre_ellision}{frag}{end_ellision}'


def pad_sentence(sentence):
    sentence = (' ' * SHOW_HIGHLIGHTED_SENTENCE) + sentence + (' ' * SHOW_HIGHLIGHTED_SENTENCE)
    return sentence


def output_line(sentences, word, qty):
    locations = ','.join(sorted(list({str(sentence['no']) for sentence in sentences})))
    sentence_highlights = sorted([sentence_fragment(word, s['line']) for s in sentences])
    print(f"{word} ({qty})".ljust(COLUMN_WIDTH) + f"| {locations}".ljust(COLUMN_WIDTH) + "|")
    for highlights in sentence_highlights:
        print(" ".ljust(COLUMN_WIDTH) + "| ".ljust(COLUMN_WIDTH) + f"| {highlights}".ljust(10))


if __name__ == '__main__':
    output_interesting_words()
