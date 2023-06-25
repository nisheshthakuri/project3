# coding = utf8
import numpy as np
import tokenizer
import ranker
import sys, getopt

inputfile = "sample.txt"
outputfile = "output.txt"
force_use_purnabiram_model = False
use_imputed_text = False
stop_words = open("stopwords.txt",'r',encoding="utf-8").read()
word_endings = open("word_endings.txt",'r',encoding='utf-8').read() 
kriyapads = open("minimal_kriyapad.txt",'r',encoding="utf-8").read().split("\n")
samyojaks = open("samyojak.txt",'r',encoding="utf-8").read().split("\n")

def get_summary_from_text(text,force_use_purnabiram_model):
    global stop_words, word_endings, kriyapads, samyojaks
    print(f"Input Text: \n{text}")
    
    is_complete_sentence = True
    purnabiram_count = text.count("।") 
    if not force_use_purnabiram_model:
        if purnabiram_count*100 < len(text):
            is_complete_sentence = False
    else:
        is_complete_sentence = False
    valid_characters = tokenizer.get_valid_chars()
      
    if not is_complete_sentence:
        text = tokenizer.add_purnabiram(text,kriyapads,samyojaks)
    print(f"Sentence after adding purnabirams: \n{text}")  
    sentences = tokenizer.get_sentences_as_arr(text)
    text = tokenizer.remove_useless_characters(text,valid_characters)


    sentences = tokenizer.remove_repeating_sentences(sentences)
    
    if len(sentences) == 0:
        return "It is not a valid text. Please try again with a valid text."
    elif len(sentences) == 1:
        return sentences
    words_arr = tokenizer.get_words_as_arr(sentences)    
    words_arr = tokenizer.remove_stop_words_and_filter_word_arr(words_arr,word_endings, stop_words)
    sentences, words_arr = tokenizer.remove_empty_sentences(sentences, words_arr)
    tokens, token_dict = tokenizer.tokenize(words_arr)
    association_matrix, counter_vector = ranker.create_association_matrix(tokens,No_of_unique_chars= len(token_dict))
    word_influence_vector = ranker.calculate_word_ranks(association_matrix, counter_vector)
    sentence_influence = ranker.calculate_sentence_influence(tokens,word_influence_vector)
    summary_sentences = ranker.get_n_influencial_sentence(sentences,sentence_influence,n=np.ceil(len(sentences)*0.33))
    summarized_text = ranker.get_summarized_text(summary_sentences)
    
    print(f"generated summary: \n{summarized_text}")
    
    with open(outputfile, 'w',encoding="utf-8") as f:
        f.write(summarized_text)
    return summarized_text
    
def get_summary_from_text_file(file_path,force_use_purnabiram_model):
    text = open(file_path,'r',encoding="utf-8").read()
    return get_summary_from_text(text,force_use_purnabiram_model)

def get_summary_from_input_text(force_use_purnabiram_model):
    text = input("Enter the text to summarize: \n")
    return get_summary_from_text(text,force_use_purnabiram_model)

get_summary_from_text_file('test.txt',force_use_purnabiram_model)
