###############################################################
# clean verbmobil dialog corpus for COMPRISE project
# by David Adelani, May 20 - 22, 2019
###############################################################
import re
import os

# cleans the text, not elegant but it works
def clean_text_one_line_per_dialogue(dialog_sections):
    new_text = ''
    for diag_sec in dialog_sections[1:]:
        # for some some reasons, the metadata information & the last line (EOF) do not contain '_',
        # we can write the lines out without processing
        if '_' not in diag_sec:
            new_text += diag_sec.strip() + '\n'
        # The section of the dialog with transcription must have at least one named entity
        # (PER, ORG or LOC which often starts with '~') or (a time or date information which starts with '#')
        if '_' in diag_sec and ('#' in diag_sec or '~' in diag_sec):
            # the speaker or responder id is separated from the dialog transcription with ':',
            # it is natural to split the dialog with ':'.
            # However, ':' can also be in the transcription which makes things complicated
            sections = diag_sec.split(':')
            s = 0
            # we loop through the different sections separated by ':' with possibility of
            # jumping indexes with that are not full dialog of the speaker i.e the dialog has ':'
            while s <= len(sections) - 1:
                sec = sections[s]
                # how do we detect if the speaker's message has multiple colon?
                # provided the previous section and the current section have a speaker ID
                # (identified with having at least 3 '_')
                n_lines_sec = sec.split('_')
                if s > 0:
                    n_lines_prev = sections[s - 1].split('_')
                else:
                    n_lines_prev = n_lines_sec

                # we treat 3 cases where ':' can occur, because of this split,
                # the next speaker id is appended at the end of the previous colon-separated-transcription/ section[i]
                # case 1: the last section, we extract the id from the previous section & append the last section to it
                # case 2: the speaker's message has only one ':' separator, we detect this by ensuring that
                #  the section and the previous section have the speaker id (i.e possess at least 3 '_' in the section)
                # case 3: the speaker's message has multiple ':', we don't know how many colons are present,
                #  it could be 10. We have to look forward to get these sections and skip indexes we have have processed
                if s == len(sections) - 1:
                    dialog_message = sections[s - 1][-23:] + ' : ' + sec
                elif len(n_lines_sec) > 2 and len(n_lines_prev) > 2:
                    if s > 0:
                        # get the id from the previous section, but skip the last 23 characters of the current section
                        # it contains the speaker ID for the next speaker's message.
                        dialog_message = sections[s - 1][-23:] + ' : ' + sec[:-23] + '\n'
                    else:
                        # the first section has only the speaker's id,
                        # we can get this information in the second iteration over the second section
                        dialog_message = ''
                else:
                    t = s
                    prev_id = sections[s - 1][-23:]
                    dialog_message = prev_id + ' : '
                    while t < len(sections) - 1:
                        cur_section = sections[t].split('_')
                        if len(cur_section) > 2:
                            # extract the remaining information of the speaker's message except the
                            # ID of the next speaker
                            dialog_message += sections[t][:-23] + '\n'
                            break
                        else:
                            # append the speaker's information separated by colon
                            dialog_message += sections[t] + ' '
                        t += 1
                    s = t
                s += 1
                new_text += dialog_message
    return new_text


#########################################################################################################################
# specify the path for the VerbMobil dialog
# Each dialog has a number of folders containing the dialog files
########################################################################################################################
def preprocess(path, output_path):

    dialog_dir = os.listdir(path)
    print(dialog_dir)

    id_len = 23  # this is the length of the ID of either the person seeking for an appointment or responding to a user
    all_tokens = set()  # vocabulary of the Language dialog corpus
    no=0  # the number of dialogs in the Language corpus, e.g for English, there are 737

    tilde_named_entities = set() # named entities that begin with '~' symbol e.g ~London, ~Smith

    list_of_files = ''
    for diag in dialog_dir:
        tr_dir = os.listdir(path+diag)
        # I'm saving the cleaned_dialogs in the same directory as the original dialog,
        # the only difference is: the uncleaned transcription has length of 3 i.e trl or tr2 while
        # the cleaned dialog folder has a suffix '_cleaned',
        # To skip the program processing the dialog files with '_cleaned', consider folder names with length 3
        diag_path = path+diag+'/'+tr_dir[0][:3]

        tr_dir = os.listdir(diag_path)
        clean_tr_dir = output_path+diag

        if not os.path.exists(clean_tr_dir):
            os.makedirs(clean_tr_dir)

        for tr_file in tr_dir:
            no+=1

            with open(diag_path+'/'+tr_file) as f:
                new_text = ''
                try:
                    app_doc = f.read()
                    # remove HTML Tags from the dialong transription
                    text2 = re.sub('<[^<]+?>', '', app_doc)
                    # remove special characters except the patterns specified in the '[^]'
                    #text = re.sub('\+\/[^<]=\/\+', ' ', text2)
                    text = re.sub('[^A-Za-z0-9_,.:;?~#\'\"=@+/]+', ' ', text2)
                    # ';' distinguish the metadata dialog information from the dialog transcription
                    dialog_sections = text.split(';')
                    # pass the dialog list to the subroutine performing the cleaning
                    new_text = clean_text_one_line_per_dialogue(dialog_sections)

                    # Print an example of the cleaned dialog transcription and compare it to the original dialog
                    if tr_file == 'q001nx.trl':
                        print(app_doc)
                        print(new_text)

                    tokens = text2.split() # why? To get the number of unique tokens in the corpus

                    for word in tokens:
                        if '~' in word:
                            #ne_word = re.sub('[^A-Za-z0-9_~#\'\"]+', ' ', word)
                            ne_word = re.sub('[^A-Za-z0-9_\'\"]+', ' ', word)
                            tilde_named_entities.add(ne_word.strip())

                    all_tokens = all_tokens | set(tokens)

                except:
                    print('cannot decode byte')

                file_name = clean_tr_dir + '/' + 'cleaned_' + tr_file
                with open(file_name, 'w') as f:
                    f.write(new_text)


    print('# of unique tokens ', len(all_tokens))
    print('# of dialog conversations: ', no)
    print(tilde_named_entities)
    print('# of ~ named entities',  len(tilde_named_entities))

if __name__ == "__main__":
    path = 'VERBMOBIL/trs/' # change this, replace it with the path of the data you bought
    output_path = 'data/VerbMobil_cleaned/'
    preprocess(path, output_path)