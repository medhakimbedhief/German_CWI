import numpy as np
import re
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import torch
from wordfreq import zipf_frequency
from transformers import BertTokenizer, BertForMaskedLM


def infenrece(input_text):
    def cleaner(word):
        # Remove links
        word = re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*',
                      '', word, flags=re.MULTILINE)
        word = re.sub('[\W]', ' ', word)
        word = re.sub('[^a-zA-Z]', ' ', word)
        return word.lower().strip()

    # load word2index dictionary from file
    with open('Code/words.pkl', 'rb') as f:
        words = pickle.load(f)
    # load word2index dictionary from file
    with open('Code/word2index.pkl', 'rb') as f:
        word2index = pickle.load(f)
    with open('Code/sentences.pkl', 'rb') as f:
        sentences = pickle.load(f)

    sent_lens = [len(sentence['seq']) for sentence in sentences]
    sent_max_length = np.max(sent_lens)

    def process_input(input_text):
        input_text = cleaner(input_text)
        clean_text = []
        index_list = []
        input_token = []
        index_list_zipf = []
        for i, word in enumerate(input_text.split()):
            if word in word2index:
                clean_text.append(word)
                input_token.append(word2index[word])
            else:
                index_list.append(i)
        input_padded = pad_sequences(maxlen=sent_max_length, sequences=[input_token], padding="post", value=0)
        return input_padded, index_list, len(clean_text)

    def get_bert_candidates(input_text, numb_predictions_displayed=103):
        list_candidates_bert = []
        for word in input_text.split():
            if (zipf_frequency(word, 'de')) < 3.2:
                replace_word_mask = input_text.replace(word, '[MASK]')
                text = f'[CLS]{replace_word_mask} [SEP] {input_text} [SEP] '
                tokenized_text = tokenizer.tokenize(text)
                masked_index = [i for i, x in enumerate(tokenized_text) if x == '[MASK]'][0]
                indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
                segments_ids = [0] * len(tokenized_text)
                tokens_tensor = torch.tensor([indexed_tokens])
                segments_tensors = torch.tensor([segments_ids])
                # Predict all tokens
                with torch.no_grad():
                    outputs = model(tokens_tensor, token_type_ids=segments_tensors)
                    predictions = outputs[0][0][masked_index]
                predicted_ids = torch.argsort(predictions, descending=True)[:numb_predictions_displayed]
                predicted_tokens = tokenizer.convert_ids_to_tokens(list(predicted_ids))
                list_candidates_bert.append((word, predicted_tokens))
        return list_candidates_bert


    bert_model = 'bert-base-german-dbmdz-uncased'
    tokenizer = BertTokenizer.from_pretrained(bert_model)
    model = BertForMaskedLM.from_pretrained(bert_model)

    new_text = input_text
    bert_candidates = get_bert_candidates(input_text)
    words = []
    for word_to_replace, l_candidates in bert_candidates:
        tuples_word_zipf = []
        for w in l_candidates:
            if w.isalpha():
                tuples_word_zipf.append((w, zipf_frequency(w, 'de')))
        tuples_word_zipf = sorted(tuples_word_zipf, key=lambda x: x[1], reverse=True)
        #print('word_to_replace : ', word_to_replace)
        words.append(word_to_replace)
        new_text = re.sub(word_to_replace, tuples_word_zipf[0][0], new_text)

    #print("Original text: ", input_text)
    #print("Simplified text:", new_text.replace('Ġ', ''), "\n")

    return words , new_text.replace('Ġ', '') , input_text
