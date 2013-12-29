#!/usr/bin/python

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__date__ = "25/12/2013"

import sys
import codecs
import nltk

punctuation = [".", ",", ":", ";", "?", "!", ")", "(", '--', "''", "``"]

#http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
noun_tags = ["NN", "NNS", "NNP", "NNPS"]
verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

# Nouns, verbs, adjectives, adverbs
lex_tags = noun_tags + verb_tags + ["JJ", "JJR", "JJS", "RB", "RBR", "RBS"]

names = {
    'num_tokens': '1. il numero di token',
    'avg_token_len': '2. la lunghezza media dei token (caratteri)',
    'avg_phrase_len': '3. la lunghezza media delle frasi (token)',
    'vocabulary_size': '4. la grandezza del vocabolario del testo',
    'avg_vocabulary_token_len': '5. la lunghezza media dei token del vocabolario (caratteri)',
    'ttr': '6. la ricchezza lessicale',
    'noun_verb_bias': '7. il rapporto tra Sostantivi e Verbi',
    'lexical_density': "8. la densita' lessicale"
}

# output padding
pad = 20


def get_stat(text):
    stat = {k: 0 for k in names.iterkeys()}
    phrases = nltk.data.load('tokenizers/punkt/english.pickle').tokenize(text)
    tokens_pos = []
    for phrase in phrases:
        phrase_tokens = nltk.word_tokenize(phrase)
        phrase_tokens_pos = nltk.pos_tag(phrase_tokens)
        tokens_pos += phrase_tokens_pos

    # 1. Number of tokens
    stat['num_tokens'] = len(tokens_pos)

    t = [token for (token, pos) in tokens_pos if token not in punctuation]

    # 2. Average token length
    l = sum([len(token) for token in t])
    stat['avg_token_len'] = l*1.0/len(t)*1.0

    # 3. Average phrase length
    stat['avg_phrase_len'] = stat['num_tokens']*1.0/len(phrases)*1.0

    # 4. Vocabulary size
    vocabulary = set(t)
    stat['vocabulary_size'] = len(vocabulary)

    # 5. Average vocabulary token length
    l = sum([len(token) for token in vocabulary if token not in punctuation])
    n = len([token for token in vocabulary if token not in punctuation])
    stat['avg_vocabulary_token_len'] = l*1.0/n*1.0

    # 6. TTR
    stat['ttr'] = len(set(t[:2000]))*1.0/2000.0

    # 7. Nouns to verbs ratio
    num_nouns = len([token for (token, pos) in tokens_pos if pos in noun_tags])
    num_verbs = len([token for (token, pos) in tokens_pos if pos in verb_tags])
    stat['noun_verb_bias'] = num_nouns*1.0/(num_nouns + num_verbs)*1.0

    # 8 Lexical density
    l = [token for (token, pos) in tokens_pos if pos in lex_tags]
    tot = [token for (token, pos) in tokens_pos if pos not in [".", ","]]
    stat['lexical_density'] = len(l)*1.0/len(tot)*1.0

    return stat


def usage():
    print """
    Usage: python project_part1.py [corpus_file_1] [corpus_file_2] > [output_file]
    Calculates statistics for the both corpus and prints results to output file
    """


def read_file(file_path):
    f = codecs.open(file_path, "r", "utf-8")
    content = f.read()
    f.close()
    return content


if __name__ == "__main__":

    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    try:
        raw1 = read_file(sys.argv[1])
        raw2 = read_file(sys.argv[2])

        # Count statistics
        stat1 = get_stat(raw1)
        stat2 = get_stat(raw2)

        # Write statistical data
        print '\n', 'Statistical characteristics of the texts:'.ljust(3*pad),\
            '\t', sys.argv[1].ljust(pad), '\t', sys.argv[2].ljust(pad)
        print ''.ljust(3*pad, '_'), '\t', ''.ljust(pad, '_'), '\t', ''.ljust(pad, '_'), '\n'

        for key, value in sorted(names.items(), key=lambda x: x[1]):
            print value.ljust(3*pad), '\t', str(stat1[key]).ljust(pad), '\t', str(stat2[key]).ljust(pad)

        print ''.ljust(3*pad, '_'), '\t', ''.ljust(pad, '_'), '\t', ''.ljust(pad, '_'), '\n'

    except IOError, e:
        print e