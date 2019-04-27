#!/usr/bin/env python
import json
import sys
from urllib.request import urlopen
import random
import chardet

import attr
import nltk
import spacy
import re

from collections import OrderedDict
from functools import partial
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from pywsd.lesk import simple_lesk as disambiguate

from lexrank import STOPWORDS, LexRank

nlp = spacy.load('en_vectors_web_lg')
print("function is called")
# Penn TreeBank POS tags:
# http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
supported_pos_tags = [
    # 'CC',   # coordinating conjunction
    # 'CD',   # Cardinal number
    # 'DT',   # Determiner
    # 'EX',   # Existential there
    # 'FW',   # Foreign word
    # 'IN',   # Preposition or subordinating conjunction
    'JJ',   # Adjective
    # 'JJR',  # Adjective, comparative
    # 'JJS',  # Adjective, superlative
    # 'LS',   # List item marker
    # 'MD',   # Modal
    'NN',   # Noun, singular or mass
    'NNS',  # Noun, plural
    'NNP',  # Proper noun, singular
    'NNPS', # Proper noun, plural
    # 'PDT',  # Predeterminer
    # 'POS',  # Possessive ending
    # 'PRP',  # Personal pronoun
    # 'PRP$', # Possessive pronoun
    'RB',   # Adverb
    # 'RBR',  # Adverb, comparative
    # 'RBS',  # Adverb, superlative
    # 'RP',   # Particle
    # 'SYM',  # Symbol
    # 'TO',   # to
    # 'UH',   # Interjection
    'VB',   # Verb, base form
    'VBD',  # Verb, past tense
    'VBG',  # Verb, gerund or present participle
    'VBN',  # Verb, past participle
    'VBP',  # Verb, non-3rd person singular present
    'VBZ',  # Verb, 3rd person singular present
    # 'WDT',  # Wh-determiner
    # 'WP',   # Wh-pronoun
    # 'WP$',  # Possessive wh-pronoun
    # 'WRB',  # Wh-adverb
]

@attr.s
class SubstitutionCandidate:
    token_position = attr.ib()
    similarity_rank = attr.ib()
    original_token = attr.ib()
    candidate_word = attr.ib()


def vsm_similarity(doc, original, synonym):

    window_size = 3
    start = max(0, original.i - window_size)
    return doc[start: original.i + window_size].similarity(synonym)


def _get_wordnet_pos(spacy_token):

    pos = spacy_token.tag_[0].lower()
    if pos in ['a', 'n', 'v']:
        return pos


def _synonym_prefilter_fn(token, synonym):

    if (len(synonym.text.split()) > 2) or \
        (synonym.lemma == token.lemma) or \
        (synonym.tag != token.tag) or \
            (token.text.lower() == 'be'):
        return False
    else:
        return True


def _generate_synonym_candidates(doc, disambiguate=False, rank_fn=None):

    if rank_fn is None:
        rank_fn=vsm_similarity

    candidates = []
    for position, token in enumerate(doc):
        if token.tag_ in supported_pos_tags:
            wordnet_pos = _get_wordnet_pos(token)
            wordnet_synonyms = []
            if disambiguate:
                try:
                    synset = disambiguate(
                           doc.text, token.text, pos=wordnet_pos)
                    wordnet_synonyms = synset.lemmas()
                except:
                    continue
            else:
                synsets = wn.synsets(token.text, pos=wordnet_pos)
                for synset in synsets:
                    wordnet_synonyms.extend(synset.lemmas())

            synonyms = []
            for wordnet_synonym in wordnet_synonyms:
                spacy_synonym = nlp(wordnet_synonym.name().replace('_', ' '))[0]
                synonyms.append(spacy_synonym)

            synonyms = filter(partial(_synonym_prefilter_fn, token),
                              synonyms)
            synonyms = reversed(sorted(synonyms,
                                key=partial(rank_fn, doc, token)))

            for rank, synonym in enumerate(synonyms):
                candidate_word = synonym.text
                candidate = SubstitutionCandidate(
                        token_position=position,
                        similarity_rank=rank,
                        original_token=token,
                        candidate_word=candidate_word)
                candidates.append(candidate)

        return candidates


def _compile_perturbed_tokens(doc, accepted_candidates):

    candidate_by_position = {}
    for candidate in accepted_candidates:
        candidate_by_position[candidate.token_position] = candidate

    final_tokens = []
    for position, token in enumerate(doc):
        word = token.text
        if position in candidate_by_position:
            candidate = candidate_by_position[position]
            word = candidate.candidate_word.replace('_', ' ')
        final_tokens.append(word)

    return final_tokens


def perturb_text(doc, use_typos=False, rank_fn=None, heuristic_fn=None, halt_condition_fn=None, verbose=False):

    heuristic_fn = heuristic_fn or (lambda _, candidate: candidate.similarity_rank)
    halt_condition_fn = halt_condition_fn or (lambda perturbed_text: False)
    candidates = _generate_synonym_candidates(doc, rank_fn=rank_fn)

    perturbed_positions = set()
    accepted_candidates = []
    perturbed_text = doc.text
    # if verbose:
    #     print('Got {} candidates'.format(len(candidates)))

    sorted_candidates = zip(
            map(partial(heuristic_fn, perturbed_text), candidates),
            candidates)
    sorted_candidates = list(sorted(sorted_candidates,
            key=lambda t: t[0]))

    while len(sorted_candidates) > 0 and not halt_condition_fn(perturbed_text):
        score, candidate = sorted_candidates.pop()
        if score < 0:
            continue
        if candidate.token_position not in perturbed_positions:
            perturbed_positions.add(candidate.token_position)
            accepted_candidates.append(candidate)
            # if verbose:
            #     print('Candidate:', candidate)
            #     print('Candidate score:', heuristic_fn(perturbed_text, candidate))
            #     print('Candidate accepted.')
            perturbed_text = ' '.join(
                    _compile_perturbed_tokens(doc, accepted_candidates))

            if len(sorted_candidates) > 0:
                _, candidates = zip(*sorted_candidates)
                sorted_candidates = zip(
                        map(partial(heuristic_fn, perturbed_text),
                            candidates),
                        candidates)
                sorted_candidates = list(sorted(sorted_candidates,
                        key=lambda t: t[0]))
    return perturbed_text


def print_paraphrase(text):
    # print('Original text:', text)
    doc = nlp(text)
    if len(doc) == 0:
        return
    perturbed_text = perturb_text(doc, verbose=False)
    return perturbed_text
    # print('Perturbed text:', perturbed_text)


def get_filler_sentences(path):
    fillers = open(path, "r", encoding='utf-8')
    filler_sentences = fillers.readlines()
    return filler_sentences


with open('../db/tmp.json') as json_file:
    data = json.load(json_file)
    url = data['url']
    romance_rating = data['romance']
    boring_rating = data['boring']
    cliche_rating = data['cliche']
    horror_rating = data['horror']
    violence_rating = data['violence']

story_data_bytes = urlopen(url)
story_data = story_data_bytes.read().decode('utf-8')
story_data = story_data.splitlines()

paraphrase_summary = []
for sentence in story_data:
    paraphrase_sentence = print_paraphrase(sentence)
    paraphrase_summary.append(paraphrase_sentence)

boring_sentences = get_filler_sentences('backend/boring_sentences.txt')
cliche_sentences = get_filler_sentences('backend/cliche_sentences.txt')
horror_sentences = get_filler_sentences('backend/horror_sentences.txt')
romance_sentences = get_filler_sentences('backend/romance_sentences.txt')
violence_sentences = get_filler_sentences('backend/violence_sentences.txt')

num_boring = (((int(boring_rating)/5)*50)/100) * len(boring_sentences)
num_cliche = (((int(cliche_rating)/5)*50)/100) * len(boring_sentences)
num_horror = (((int(horror_rating)/5)*50)/100) * len(boring_sentences)
num_romance = (((int(romance_rating)/5)*50)/100) * len(boring_sentences)
num_violence = (((int(violence_rating)/5)*50)/100) * len(boring_sentences)

try:
    lxr = LexRank(paraphrase_summary, stopwords=STOPWORDS['en'])
    boring_scores_cont = lxr.rank_sentences(boring_sentences, threshold=None, fast_power_method=True)
    cliche_scores_cont = lxr.rank_sentences(cliche_sentences, threshold=None, fast_power_method=True)
    horror_scores_cont = lxr.rank_sentences(horror_sentences, threshold=None, fast_power_method=True)
    romance_scores_cont = lxr.rank_sentences(romance_sentences, threshold=None, fast_power_method=True)
    violence_scores_cont = lxr.rank_sentences(violence_sentences, threshold=None, fast_power_method=True)


    boring_index = sorted(range(len(boring_scores_cont)), key=lambda i: boring_scores_cont[i])[-int(num_boring):]
    cliche_index = sorted(range(len(cliche_scores_cont)), key=lambda i: cliche_scores_cont[i])[-int(num_cliche):]
    horror_index = sorted(range(len(horror_scores_cont)), key=lambda i: horror_scores_cont[i])[-int(num_horror):]
    romance_index = sorted(range(len(romance_scores_cont)), key=lambda i: romance_scores_cont[i])[-int(num_romance):]
    violence_index = sorted(range(len(violence_scores_cont)), key=lambda i: violence_scores_cont[i])[-int(num_violence):]

    add_boring_sentence = []
    add_cliche_sentence = []
    add_horror_sentence = []
    add_romance_sentence = []
    add_violence_sentence = []


    def prepare_sentences(list_of_sentence, index, sentence_type):
        for value in index:
            if sentence_type == 'boring':
                add_boring_sentence.append("%%SB%%"+str(list_of_sentence[value].rstrip())+"%%EB%%")
            elif sentence_type == 'cliche':
                add_cliche_sentence.append("%%SC%%"+str(list_of_sentence[value].rstrip())+"%%EC%%")
            elif sentence_type == 'horror':
                add_horror_sentence.append("%%SH%%"+str(list_of_sentence[value].rstrip())+"%%EH%%")
            elif sentence_type == 'romance':
                add_romance_sentence.append("%%SR%%"+str(list_of_sentence[value].rstrip())+"%%ER%%")
            elif sentence_type == 'violence':
                add_violence_sentence.append("%%SV%%"+str(list_of_sentence[value].rstrip())+"%%EV%%")


    prepare_sentences(boring_sentences, boring_index, 'boring')
    prepare_sentences(cliche_sentences, cliche_index, 'cliche')
    prepare_sentences(horror_sentences, horror_index, 'horror')
    prepare_sentences(romance_sentences, romance_index, 'romance')
    prepare_sentences(violence_sentences, violence_index, 'violence')


    def add_final_sentences(sentence_list):
        summary_length = len(paraphrase_summary)
        for i in range(len(sentence_list)):
            paraphrase_summary.insert(random.randint(0, summary_length), sentence_list[i])


    add_final_sentences(add_boring_sentence)
    add_final_sentences(add_cliche_sentence)
    add_final_sentences(add_horror_sentence)
    add_final_sentences(add_romance_sentence)
    add_final_sentences(add_violence_sentence)

    with open('../db/output.txt', 'w', encoding='utf-8') as final_story:
        final_story.write(' '.join(paraphrase_summary))
    final_story.close()

except ValueError:
    with open('../db/output.txt', 'w', encoding='utf-8') as final_story:
        final_story.write(' '.join(paraphrase_summary))
    final_story.close()
