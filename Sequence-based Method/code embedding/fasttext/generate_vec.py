## coding: utf-8

from gensim.models import FastText
import pickle
import os
import numpy as np
import random
import gc
import shutil

import datetime

'''
generate_corpus function
-----------------------------
This function is used to create input of deep learning model

# Arguments
    w2vModelPath: the path saves word2vec model
    samples: the list of sample

'''


def generate_vector(fasttext_ModelPath, samples):
    model = FastText.load(fasttext_ModelPath)
    print("begin generate input...")
    dl_corpus = [[model[word] for word in sample] for sample in samples]
    print("generate input success...")
    return dl_corpus


if __name__ == "__main__":
    startTime = datetime.datetime.now()

    CORPUSPATH = "./corpus/"
    VECTORPATH = "./vector/"
    FastTextPATH = "./fasttext_model"
    print("turn the corpus into vectors...")
    for corpusfiles in os.listdir(CORPUSPATH):
        print(corpusfiles)
        if corpusfiles not in os.listdir(VECTORPATH):
            folder_path = os.path.join(VECTORPATH, corpusfiles)
            os.mkdir(folder_path)
        for corpusfile in os.listdir(CORPUSPATH + corpusfiles):
            corpus_path = os.path.join(CORPUSPATH, corpusfiles, corpusfile)
            f_corpus = open(corpus_path, 'rb')
            data = pickle.load(f_corpus)
            f_corpus.close()
            data[0] = generate_vector(FastTextPATH, data[0])
            vector_path = os.path.join(VECTORPATH, corpusfiles, corpusfile)
            f_vector = open(vector_path, 'wb')
            pickle.dump(data, f_vector, protocol=pickle.HIGHEST_PROTOCOL)
            f_vector.close()

    endTime = datetime.datetime.now()
    print("fasttext over...")
    print("success!")
    print("Cost Time:", endTime - startTime)
