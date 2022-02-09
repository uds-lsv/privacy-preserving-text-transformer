import os
import sys
import pandas as pd
import string
import numpy as np

def split_sentences_by_period(data_list, dir, output_dir):
    for f_file in data_list:
        t_data = []
        with open(dir + f_file) as f:
            file_text = f.readlines()

        for k, line in enumerate(file_text):
            word = line.strip()

            if word == '~#' or word == '.' or word == '#':
                t_data.append('')
            else:
                t_data.append(word)

        with open(output_dir + f_file[:-4]+'.txt', 'w') as f:
            for token in t_data:
                f.write(token+'\n')

    print('# dialogs and sentences', len(data_list))

def extract_tag_sentence(docs):
    sentences = []
    sent = []
    for i, line in enumerate(docs):
        if len(line) < 3:
            if len(sent) > 0:
                sentences.append(sent)
            sent = []
        else:
            # print(i, line)
            token, ne = line.strip().split(' ')
            sent.append(ne)
    return sentences

def extract_word_sentence(docs):
    sentences = []
    sent = []
    for i, line in enumerate(docs):
        if len(line) < 1:
            if len(sent) > 0:
                sentences.append(sent)
            sent = []
        else:
            token = line.strip()
            sent.append(token)
    return sentences

def extract_sentences(word_file, tag_file):

    with open(word_file) as fw, open(tag_file) as ft:
        word_doc = fw.read().splitlines()
        tag_doc = ft.read().splitlines()

    #if len(word_doc)!=len(tag_doc):
    #    return []
    #else:
    #    print(word_file, tag_file)
    sent_words = extract_word_sentence(word_doc)
    sent_tags = extract_tag_sentence(tag_doc)

    if len(sent_words) != len(sent_tags):
        return []

    word_tags = []
    for s, sent in enumerate(sent_words):
        tag_sent = sent_tags[s]
        if len(sent)!=len(tag_sent):
            return []
        for w, word in enumerate(sent):
            word_tags.append([word, tag_sent[w]])
        word_tags.append([' ', ' '])
    return word_tags

def export_verbmobil_words(output_dir):
    raw_dir = 'data/VerbMobil_per_dialog/'
    dir_files = os.listdir(raw_dir)
    split_sentences_by_period(dir_files, raw_dir, output_dir)


def export_sentence(output_dir, filename, sentences):
    with open(output_dir+filename, 'w') as f:
        for tok, tag in sentences:
            f.write(tok+' '+tag+'\n')

def auto_annotate(output_dir):
    word_dir = 'data/verbmobil_words/'
    tags_dir = 'data/verbmobil-tags/'

    word_files = sorted(os.listdir(word_dir))
    tag_files = sorted(os.listdir(tags_dir))

    for i, word_file in enumerate(word_files):
        sentences = extract_sentences(word_dir+word_file, tags_dir+tag_files[i])
        if len(sentences) >0:
            export_sentence(output_dir, word_file[:-4]+'.txt', sentences)


def create_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

if __name__ == '__main__':
    output_dir = 'data/verbmobil_words/'
    create_dir(output_dir)
    export_verbmobil_words(output_dir)

    output_dir = 'data/verbmobil-ner/'
    create_dir(output_dir)
    auto_annotate(output_dir)
