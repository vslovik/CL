#!/usr/bin/python

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__date__ = "25/12/2013"

import sys
import codecs
import nltk
from nltk import bigrams
from nltk import trigrams
import math
from collections import defaultdict

# http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# Alphabetical list of part-of-speech tags used in the Penn Treebank Project:
punctuation = [".", ",", ":", ";", "?", "!", ")", "(", '--', "''", "``", "'", "%", "$", "#"]


names = {
    "top_tokens": "1. i 20 token piu' frequenti",
    "top_pos": "2. le 10 PoS piu' frequenti",
    "top_trigrams": "3. i 10 trigrammi di token piu' frequenti",
    "top_bigrams_joint_prob": "4. 10 bigrammi con probabilita' congiunta massima",
    "top_bigrams_cond_prob": "5. 10 bigrammi con probabilita' condizionata massima",
    "top_collocations": "6. 10 bigrammi con forza associativa massima",
    "top_person_proper_names": "7. i 20 nomi propri di persona piu' frequenti",
    "top_location_proper_names": "8. i 20 nomi propri di luogo piu' frequenti",
}

pad = 24


def get_top_tokens(tokens_pos, n):
    top_tokens = []
    token_list = [token for (token, pos) in tokens_pos if token not in punctuation]
    c = len(token_list)
    dist = nltk.FreqDist(token_list)
    for token in dist.keys()[:n]:
        top_tokens.append(''.join([token.ljust(pad, ' '), str(dist[token]*1.0/c*1.0).ljust(pad, ' ')]))
    return top_tokens


def get_top_pos(tokens_pos, n):
    top_pos = []
    pos_list = [pos for (token, pos) in tokens_pos if token not in punctuation]
    c = len(pos_list)
    dist = nltk.FreqDist(pos_list)
    for pos in dist.keys()[:n]:
        top_pos.append(''.join([pos.ljust(pad, ' '), str(dist[pos]*1.0/c*1.0).ljust(pad, ' ')]))
    return top_pos


def is_valid_top_trigram(trigram, token_dist):
    for (token, pos) in trigram:
        if token in punctuation:
            return False
        if pos == 'CC':
            return False
        if token_dist[token] < 2:
            return False

    return True


def get_top_trigrams(dist, c, n):
    top_trigrams = []
    for trigram in dist.keys()[:n]:
        s = ' '.join([token for (token, pos) in trigram])
        top_trigrams.append(''.join([s.ljust(pad, ' '), str(dist[trigram]*1.0/c*1.0).ljust(pad, ' ')]))
    return top_trigrams


def get_top(str_list, n):
    top_list = []
    c = len(str_list)
    dist = nltk.FreqDist(str_list)
    for item in dist.keys()[:n]:
        top_list.append(''.join([item.ljust(pad, ' '), str(dist[item]*1.0/c*1.0).ljust(pad, ' ')]))
    return top_list


def is_valid_top_bigram(bigram, token_dist):
    for (token, pos) in bigram:
        if token in punctuation:
            return False
        if pos in ['CC', 'IN', 'TO']:
            return False
        if token_dist[token] < 2:
            return False
    return True


def get_top_bigrams_joint_prob(dist, c, n):
    top_bigrams = []
    for bigram, f in sorted(dist.iteritems(), key=lambda x: x[1], reverse=True)[:n]:
        s = ' '.join([token for (token, pos) in bigram])
        top_bigrams.append(''.join([s.ljust(pad, ' '), str(dist[bigram]*1.0/c*1.0).ljust(pad, ' ')]))
    return top_bigrams


def get_top_bigrams_cond_prob(bigram_dist, token_dist, n):
    top_bigrams = []
    prob_dist = {}
    for bigram, f in bigram_dist.iteritems():
        prob_dist[bigram] = f*1.0/token_dist[bigram[1][0]]*1.0
    for bigram, prob in sorted(prob_dist.iteritems(), key=lambda x: x[1], reverse=True)[:n]:
        s = ' '.join([token for (token, pos) in bigram])
        top_bigrams.append(''.join([s.ljust(pad, ' '), str(prob).ljust(pad, ' ')]))
    return top_bigrams


def get_top_collocations(bigram_dist, token_dist, token_len, n):
    top_bigrams = []
    mi_dist = {}
    for bigram, f in bigram_dist.iteritems():
        mi_dist[bigram] = f*math.log(f*token_len*1.0/token_dist[bigram[0][0]]*token_dist[bigram[1][0]]*1.0, 2)
    for bigram, mi in sorted(mi_dist.iteritems(), key=lambda x: x[1], reverse=True)[:n]:
        s = ' '.join([token for (token, pos) in bigram])
        top_bigrams.append(''.join([s.ljust(pad, ' '), str(mi).ljust(pad, ' ')]))
    return top_bigrams


def get_top_ne(dist, n):
    top_ne = []
    c = sum(dist.values())
    for ne, f in sorted(dist.iteritems(), key=lambda x: x[1], reverse=True)[:n]:
        top_ne.append(''.join([ne.ljust(pad, ' '), str(dist[ne]*1.0/c*1.0).ljust(pad, ' ')]))
    return top_ne


def get_data(text):
    data = {k: 0 for k in names.iterkeys()}
    phrases = nltk.data.load('tokenizers/punkt/english.pickle').tokenize(text)
    tokens_pos = []
    person_dist = defaultdict(int)
    location_dist = defaultdict(int)
    for phrase in phrases:
        phrase_tokens = nltk.word_tokenize(phrase)
        phrase_tokens_pos = nltk.pos_tag(phrase_tokens)
        tokens_pos += phrase_tokens_pos
        analyzed = nltk.ne_chunk(phrase_tokens_pos)
        for node in analyzed:
            if hasattr(node, 'node'):
                if "PERSON" == node.node:
                    p = ' '.join([part_ne[0] for part_ne in node.leaves()])
                    person_dist[p] += 1
                elif "GPE" == node.node:
                    l = ' '.join([part_ne[0] for part_ne in node.leaves()])
                    location_dist[l] += 1

    c = len(tokens_pos)
    token_dist = nltk.FreqDist([token for (token, pos) in tokens_pos])
    bigram_dist = nltk.FreqDist([bigram for bigram in bigrams(tokens_pos)
                                if is_valid_top_bigram(bigram, token_dist)])
    trigram_dist = nltk.FreqDist([trigram for trigram in trigrams(tokens_pos)
                                 if is_valid_top_trigram(trigram, token_dist)])

    # The most frequent tokens tokens
    data['top_tokens'] = get_top_tokens(tokens_pos, 20)

    # The most frequent PoS tags
    data['top_pos'] = get_top_pos(tokens_pos, 10)

    del tokens_pos

    # The most frequent trigrams
    data['top_trigrams'] = get_top_trigrams(trigram_dist, c, 10)

    # Bigrams with max joint probability
    data['top_bigrams_joint_prob'] = get_top_bigrams_joint_prob(bigram_dist, c, 10)

    # Bigrams with max conditional probability
    data['top_bigrams_cond_prob'] = get_top_bigrams_cond_prob(bigram_dist, token_dist, 10)

    # Collocations
    data['top_collocations'] = get_top_collocations(bigram_dist, token_dist, c,  10)

    # The most frequent person and location proper names
    data['top_person_proper_names'] = get_top_ne(person_dist, 20)

    # The most frequent person and location proper names
    data['top_location_proper_names'] = get_top_ne(location_dist, 20)

    return data


def usage():
    print """
    Usage: python project_part2.py [corpus_file_1] [corpus_file_2] > [output_file]
    Extracts linguistic data for the both corpus and prints results to output file
    """


def read_file(filepath):
    f = codecs.open(filepath, "r", "utf-8")
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
        data1 = get_data(raw1)
        data2 = get_data(raw2)

        # Write linguistic data

        pad *= 2
        print '\n', 'Linguistic data for the texts:'.ljust(pad), '\n', sys.argv[1].ljust(pad), '\t', sys.argv[2].ljust(pad)
        print ''.ljust(pad, '_'), '\t', ''.ljust(pad, '_'), '\n'

        for key, value in sorted(names.items(), key=lambda x: x[1]):
            print "\n", value, "\n"
            for i in range(len(data1[key])-1):
                print str(data1[key][i]).ljust(pad), '\t', str(data2[key][i]).ljust(pad)

        print ''.ljust(pad, '_'), '\t', ''.ljust(pad, '_'), '\n'

    except IOError, e:
        print e