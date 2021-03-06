
import gensim
import pandas as pd
import os
import Settings
import time
import warnings

import LoadIMDB 

warnings.simplefilter(action='ignore', category=FutureWarning)

DEFAULT_EMBEDDING_SIZE = Settings.EMB_DIM
PRINT_DEBUG = True
NUM_CPU = 4

def get_lines(df_list):
    ''' 
    Get all the reviews from all the data samples
    params:
        df_list -- list of dataframes with 'review' column.
    return
        word2vec training corpus which is a list of all reviews from df_list
    '''
    train_corpus = []
    for df in df_list:
        for review in df['review'].values:
            train_corpus.append(review.split())
    return train_corpus

def get_embedding_matrix(which_embedding):
    ''' Returns the numpy matrix of the embedding we wish to find'''
    return (get_wordvec(which_embedding)).syn0

def get_embedding(which_embedding):
    ''' Return the wv model '''

    # String of the model we should try to load.
#    trained_embedding = "w2v_m%s" % which_embedding

    # Check if we should train new embeddings
    if (os.path.isfile(
        "../data/word2vec_models/w2v_m%s.model" % which_embedding)):

        if (PRINT_DEBUG):
            print('loading ../data/word2vec_models/w2v_m%s' % which_embedding)
        return gensim.models.KeyedVectors.load(
            "../data/word2vec_models/w2v_m%s.model" % which_embedding)

    print("\nTraining w2v_m%s" % which_embedding)

    # Load in the datasets.
    train_pos = LoadIMDB.get_IMDB(train=True, positive=True)
    train_neg = LoadIMDB.get_IMDB(train=True, positive=False)
    test_pos = LoadIMDB.get_IMDB(train=False, positive=True)
    test_neg = LoadIMDB.get_IMDB(train=False, positive=False)

    my_lines = get_lines([train_pos, train_neg, test_pos, test_neg])

    print('Number of reviews for training:', len(my_lines))

    if which_embedding == 1:
        window_size = 5 
    if which_embedding == 2:
        window_size = 3 
    if which_embedding == 3:
        window_size = 7 

    start_time = time.time()
    model = gensim.models.Word2Vec(my_lines, size=DEFAULT_EMBEDDING_SIZE,
            window=window_size, workers=NUM_CPU, min_count=1)

    print("--- %s seconds to train word2vec_m%s---" % 
            ((time.time()-start_time), which_embedding))
    print("Saved --- w2v_m%s --- in ../data/word2vec_models/w2v_m%s.model" %
            (which_embedding, which_embedding))

    model.wv.save("../data/word2vec_models/w2v_m%s.model" % which_embedding)
    return model

def get_wordvec(wv_loc):
    ''' Load a word vec given the location saved'''
    return gensim.models.KeyedVectors.load(wv_loc, mmap='r')

if __name__ == "__main__":
    # Train 3 default w2v models.
    get_embedding(1)
    get_embedding(2)
    get_embedding(3)

    LoadIMDB.get_emb_IMDB(train=True, positive=True)
    LoadIMDB.get_emb_IMDB(train=True, positive=False)
    LoadIMDB.get_emb_IMDB(train=False, positive=True)
    LoadIMDB.get_emb_IMDB(train=False, positive=False)



