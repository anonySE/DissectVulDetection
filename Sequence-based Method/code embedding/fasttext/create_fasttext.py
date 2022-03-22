## coding: utf-8
'''
This python file is used to tranfer the words in corpus to vector, and save the word2vec model under the path 'w2v_model'.
'''


from gensim.models import FastText
import pickle
import os
import gc

import datetime

'''
DirofCorpus class
-----------------------------
This class is used to make a generator to produce sentence for word2vec training

# Arguments
    dirname: The src of corpus files 
    
'''

class DirofCorpus(object):
    def __init__(self, dirname):
        self.dirname = dirname
    
    def __iter__(self):
        for d in self.dirname:
            for fn in os.listdir(d):
                print(fn)
                for filename in os.listdir(os.path.join(d, fn)):
                    samples = pickle.load(open(os.path.join(d, fn, filename), 'rb'))[0]
                    # print(samples)
                    for sample in samples:
                        # print(sample)
                        yield sample
                    del samples
                    gc.collect()

'''
generate_w2vmodel function
-----------------------------
This function is used to learning vectors from corpus, and save the model

# Arguments
    decTokenFlawPath: String type, the src of corpus file 
    w2vModelPath: String type, the src of model file 
    
'''

def generate_fasttext_Model(decTokenFlawPath, fasttext_ModelPath):
    print("training...")
    model = FastText(sentences= DirofCorpus(decTokenFlawPath), size=30, alpha=0.01, window=5, min_count=0, max_vocab_size=None, word_ngrams=1, min_n=3, max_n=6, sample=0.001, seed=1, workers=1, min_alpha=0.0001, sg=1, hs=1, negative=5, iter=10)
    model.save(fasttext_ModelPath)

def evaluate_w2vModel(fasttext_ModelPath):
    print("\nevaluating...")
    model = FastText.load(fasttext_ModelPath)
    for sign in ['(', '+', '-', '*', 'func_1']:
        print(sign, ":")
        print(model.most_similar_cosmul(positive=[sign], topn=10))
    
def main():
    startTime = datetime.datetime.now()
    dec_tokenFlaw_path = ['./corpus/']
    fasttext_model_path = "./fasttext_model"
    generate_fasttext_Model(dec_tokenFlaw_path, fasttext_model_path)
    evaluate_w2vModel(fasttext_model_path)
    endTime = datetime.datetime.now()
    print("success!")
    print("Cost Time:", endTime - startTime)

 
if __name__ == "__main__":
    main()


