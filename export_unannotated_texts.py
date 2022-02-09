import os
from collections import defaultdict, Counter
import re
import pandas as pd
import spacy
import random

def create_dir(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

def remove_atsymbol_digits(text):
    new_tokens = []
    for token in text.split():
        new_token = ''.join([char for char in token if not (char.isdigit() or char == '@')])
        if new_token != '@' and new_token != '':
            new_tokens.append(new_token)
    return ' '.join(new_tokens)


def extract_dialog_texts(path):

    dialog_dir = os.listdir(path)

    no=0
    dialog_texts = []
    for diag in dialog_dir:
        tr_dir = os.listdir(path+diag)
        print(tr_dir)
        diag_path = path+diag+'/'
        tr_dir = os.listdir(diag_path)
        for tr_file in tr_dir:
            no+=1
            if '.' not in tr_file:
                continue
            dialog_id = diag + '_' + tr_file
            with open(diag_path+'/'+tr_file) as f:
                try:
                    app_doc = f.read()
                    line_texts = app_doc.split('\n')
                    dialog_texts.append([dialog_id]+line_texts)
                except:
                    print('cannot decode byte')

    print('# of text lines ', len(dialog_texts))

    return dialog_texts

def main():
    path = 'data/VerbMobil_cleaned/'
    output_path = 'data/VerbMobil_per_dialog/'
    create_dir(output_path)

    dialog_texts = extract_dialog_texts(path)

    for d, dialog in enumerate(dialog_texts):
        n_idx = 0
        # filter metadata info
        convers_text = ' '

        for convers in dialog:
            if '_' not in convers:
                n_idx+=1
                continue
            elif convers.endswith('.trl'):
                n_idx+=1
                folder_dialog_id = convers.strip()
            else:
                text_proc = re.sub('\+\/[^<]+\/\+', '', convers)
                text_proc = re.sub('[^A-Za-z0-9_,.:;?@\'\"=+/]+', ' ', text_proc)
                id_text = text_proc[:text_proc.index(':')]
                imp_text = text_proc[text_proc.index(':') + 1:]
                #imp_text_list = re.split('[#.?]', imp_text.strip())
                #print(imp_text_list)


                #new_imp_text_list = []
                #for a_str in imp_text_list:
                a_str = remove_atsymbol_digits(imp_text)
                new_imp_text = a_str.strip()
                #new_imp_text_list.append(a_str)

                convers_text += new_imp_text + '\n~# '
                #convers_text += new_imp_text_list


                #print(imp_text_list)
                #print(new_imp_text_list)

        with open(output_path+folder_dialog_id, 'w') as f:
            #for sent in convers_text:
            for tok in convers_text.split():
                f.write(tok+'\n')
            #f.write('\n')


if __name__ == "__main__":
    main()