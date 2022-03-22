import os
import pickle
import sys
import argparse
import numpy as np
sys.path.append("../..")
from all_embedding.pre_train_def.glove import gen_vocab, gen_corpus, train_glove
from gensim.models import KeyedVectors
import pickle

def read_code(path_base):
    all_code = []
    all_code_doc = []
    names = ["good", "bad"]
    for name in names:
        codedocs = pickle.load(open(path_base+name,"rb"))
        for code in codedocs:
            all_code.append(code[0])
            all_code_doc.append(code)
    return all_code, all_code_doc

def train_model(embed_arg, base, result_path, code_path, vector_size, max_length):
    cooccurrence_file = base + "cooccurrence.bin"
    cooccurrence_shuf_file = base + "cooccurrence.shuf.bin"
    build_dir = base + "build"

    pre_model_path = result_path + "model.txt"
    corpus_path = result_path + "src_corpus.txt"
    vocab_path = result_path + "src_vocab.txt"
    save_file = result_path + "src_vectors"
    glove_file = result_path + "src_vectors.txt"

    arg = dict(vocab_min_count=embed_arg["vocab_min_count"], vector_size=embed_arg["voc_size"],
               max_iter=embed_arg["max_iter"],
               window_size=embed_arg["window_size"], x_max=embed_arg["x_max"], corpus=corpus_path,
               vocab_file=vocab_path,
               cooccurrence_file=cooccurrence_file, cooccurrence_shuf_file=cooccurrence_shuf_file, build_dir=build_dir,
               save_file=save_file, memory=embed_arg["memory"], num_threads=embed_arg["num_threads"],
               verbose=embed_arg["verbose"], binary=embed_arg["binary"],
               glove_file=glove_file, w2v_file=pre_model_path)

    code_blocks, all_code_doc = read_code(code_path)

    if not os.path.isfile(pre_model_path):
        print("generating corpus...")
        gen_corpus(code_blocks, corpus_path)
        print("generating vocabulary...")
        gen_vocab(code_blocks, vocab_path)
        print("training...")
        train_glove(arg)
    print("generate embedding...")
    generate_embedding(all_code_doc, pre_model_path, vector_size, max_length, code_path)

def convert_tokens(sentence, model, vec_dim, max_length):
    vecs = []
    for word in sentence:
        if len(vecs) > max_length:
            break
        try:
            vecs.append(model[word])
        except KeyError as e:
            continue
    while (len(vecs) < max_length):
        vecs.append(np.zeros(vec_dim))
    return vecs

def generate_embedding(all_code_doc, pre_model_path, vector_size, max_length, code_path):
    model = KeyedVectors.load_word2vec_format(pre_model_path)
    index = 0
    vec_path = code_path+"vec/"
    if not os.path.isdir(vec_path):
        os.mkdir(vec_path)
    for i in range(len(all_code_doc)):
        # all_code_doc[i][0] = convert_tokens(all_code_doc[i][0], model, vector_size, max_length)
        pickle.dump([convert_tokens(all_code_doc[i][0], model, vector_size, max_length), all_code_doc[i][1]], open(vec_path+str(index)+".pkl", "wb"))
        index += 1
    # pickle.dump(all_code_doc, open(code_path+"vec.pkl", "wb"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', '-d', help='category')
    args = parser.parse_args()
    base = "/data/bugDetection/srcIRcom/all_embedding/pre_train_def/GloVe-master/"
    data = args.data
    result_path = "/data/yyx/high_level_code_vulnerability/embed_model/glove/" + data + "/"
    code_path = "/data/yyx/high_level_code_vulnerability/vul_data/" + data + "/"

    memory = [4.0]
    num_threads = [8]
    verbose = [2]
    binary = [2]
    vocab_min_count = [5]
    vector_size = [50]
    max_iter = [15]
    window_size = [15]
    x_max = [10]
    max_length = 900

    embed_arg = dict(memory=memory[0], num_threads=num_threads[0], verbose=verbose[0], binary=binary[0],
                     vocab_min_count=vocab_min_count[0], voc_size=vector_size[0], max_iter=max_iter[0],
                     window_size=window_size[0], x_max=x_max[0])
    train_model(embed_arg, base, result_path, code_path, vector_size, max_length, )
    # generate_embedding()
