## -*- coding: utf-8 -*-i
'''
This python file is used to train four class focus data in blstm models

'''

from keras.preprocessing import sequence
# from keras.optimizers import SGD, RMSprop, Adagrad, Adam, Adadelta
from keras.models import Sequential, load_model
from keras.layers.core import Masking, Dense, Dropout, Activation
from keras.layers.recurrent import LSTM, GRU
from preprocess_dl_Input_version5 import *
from keras.layers.wrappers import Bidirectional
from collections import Counter
import numpy as np
import keras
import pickle
import random
import time
import math
import os
import argparse

RANDOMSEED = 2021  # for reproducibility
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def build_model(maxlen, vector_dim, layers, dropout, unit, use_bias):
    print('Build models...')
    model = Sequential()

    model.add(Masking(mask_value=0.0, input_shape=(maxlen, vector_dim)))

    for i in range(1, layers):
        model.add(
            GRU(units=unit, activation='tanh', recurrent_activation='hard_sigmoid', return_sequences=True,
            use_bias=use_bias))
        model.add(Dropout(dropout))

    model.add(GRU(units=unit, activation='tanh', recurrent_activation='hard_sigmoid', use_bias=use_bias))
    model.add(Dropout(dropout))

    model.add(Dense(1, activation='sigmoid'))

    """model.compile(loss='binary_crossentropy', optimizer='adamax',
                  metrics=['TP_count', 'FP_count', 'FN_count', 'precision', 'recall', 'fbeta_score'])"""

    model.compile(loss='binary_crossentropy', optimizer='adamax',
                  metrics=[keras.metrics.TruePositives(),
                           keras.metrics.FalsePositives(),
                           keras.metrics.FalseNegatives(),
                           keras.metrics.Precision(),
                           keras.metrics.Recall(),
                           'accuracy'])

    model.summary()

    return model


def main(traindataSet_path, testdataSet_path, realtestpath, weightpath, resultpath, batch_size, maxlen, vector_dim,
         layers, dropout, unit, use_bias):
    print("Loading data...")

    model = build_model(maxlen, vector_dim, layers, dropout, unit, use_bias)

    # model.load_weights(weightpath)  #load weights of trained models

    print("Train...")
    dataset = []
    labels = []
    funcs = []
    linetokens = []
    testcases = []
    vpointers = []
    for filename in os.listdir(traindataSet_path):
        if filename.endswith(".pkl") is False:
            continue
        print(filename)
        #   for filename in os.listdir(os.path.join(traindataSet_path,filename)):
        # print(filename)
        f = open(os.path.join(traindataSet_path, filename), "rb")
        # 分别是样本向量、句子拆分点、漏洞点、goodbad函数表、testcase切片名
        dataset_file, linetokens_file, vpointers_file, func_file, filename_file = pickle.load(f)
        # ret = pickle.load(f)
        # print(ret)
        f.close()
        dataset += dataset_file
        linetokens += linetokens_file
        vpointers += vpointers_file
        funcs += func_file
    print(len(dataset), len(vpointers))
    train_dataset = len(dataset)

    # 按照漏洞点和所属函数生成0/1标签
    m = 0
    n = 0
    for vp in range(len(vpointers)):
        if vpointers[vp] != []:
            label = 1
            m += 1
            for func in funcs[vp]:
                # 如果是good函数中提的切片实际上无漏洞
                if "good" in func:
                    label = 0
                    vpointers[vp] = []
                    break
        else:
            label = 0
            n += 1
        labels.append(label)

    print("vul: ", m, "non_vul: ", n)
    train_vul = m
    train_nonvul = n

    bin_labels = []
    for label in labels:
        bin_labels.append(multi_labels_to_two(label))
    labels = np.array(bin_labels)

    np.random.seed(RANDOMSEED)
    np.random.shuffle(dataset)
    np.random.seed(RANDOMSEED)
    np.random.shuffle(labels)

    train_generator = generator_of_data(dataset, labels, batch_size, maxlen, vector_dim)
    all_train_samples = len(dataset)
    steps_epoch = int(all_train_samples / batch_size)
    cp_callback = keras.callbacks.ModelCheckpoint(
                filepath=weightpath, 
                    verbose=1, 
                        save_weights_only=True,
                            save_freq= steps_epoch)
    print("start")
    t1 = time.time()
    model.fit_generator(train_generator, steps_per_epoch=steps_epoch, epochs=10,callbacks=[cp_callback])
    t2 = time.time()
    train_time = t2 - t1

    model.save_weights(weightpath)

    # models.load_weights(weightpath)
    # print("Test...")
    # dataset = []
    # labels = []
    # linetokens = []
    # vpointers = []
    # testcases = []
    # filenames = []
    # funcs = []
    # for filename in os.listdir(testdataSet_path):
    #     if filename.endswith(".pkl") is False:
    #         continue
    #     print(filename)
    #     #   for filename in os.listdir(os.path.join(testdataSet_path,filename)):
    #     # print(filename)
    #     f = open(os.path.join(testdataSet_path, filename), "rb")
    #     # 分别是样本向量、句子拆分点、漏洞点、goodbad函数表、句子语料、testcase切片名
    #     dataset_file, linetokens_file, vpointers_file, funcs_file, filename_file = pickle.load(f)
    #     f.close()
    #     dataset += dataset_file
    #     linetokens += linetokens_file
    #     vpointers += vpointers_file
    #     funcs += funcs_file
    #     filenames += filename_file
    # print(len(dataset), len(filenames))
    #
    # # 按照漏洞点和所属函数生成0/1标签
    # m = 0
    # n = 0
    # for vp in range(len(vpointers)):
    #     if vpointers[vp] != []:
    #         label = 1
    #         m += 1
    #         for func in funcs[vp]:
    #             # 如果是good函数中提的切片实际上无漏洞
    #             if "good" in func:
    #                 label = 0
    #                 vpointers[vp] = []
    #                 break
    #     else:
    #         label = 0
    #         n += 1
    #     labels.append(label)
    #
    # print("vul: ", m, "non_vul: ", n)
    # test_vul = m
    # test_nonvul = n
    #
    # bin_labels = []
    # for label in labels:
    #     bin_labels.append(multi_labels_to_two(label))
    # labels = np.array(bin_labels)
    #
    # batch_size = 1
    # test_generator = generator_of_data(dataset, labels, batch_size, maxlen, vector_dim)
    # all_test_samples = len(dataset)
    # steps_epoch = int(math.ceil(all_test_samples / batch_size))
    #
    # t1 = time.time()
    # result = model.evaluate_generator(test_generator, steps=steps_epoch)
    # t2 = time.time()
    # test_time = t2 - t1
    # loss, TP, FP, FN, precision, recall, accuracy = result
    # f = open("TP_index_gru.pkl", 'wb')
    # pickle.dump(result[1], f)
    # f.close()
    #
    # """f_TP = open("./result_analyze/BGRU/TP_filenames.txt", "ab+")
    # for i in range(len(result[1])):
    #     TP_index = result[1][i]
    #     f_TP.write(str(filenames[TP_index]) + '\n')
    #
    # f_FP = open("./result_analyze/BGRU/FP_filenames.txt", "ab+")
    # for j in range(len(result[2])):
    #     FP_index = result[2][j]
    #     f_FP.write(str(filenames[FP_index]) + '\n')
    #
    # f_FN = open("./result_analyze/BGRU/FN_filenames.txt", "a+")
    # for k in range(len(result[3])):
    #     FN_index = result[3][k]
    #     f_FN.write(str(filenames[FN_index]) + '\n')"""
    #
    # TN = all_test_samples - TP - FP - FN
    # fwrite = open(resultpath, 'a')
    # fwrite.write('train_samples_sum: ' + ' ' + str(train_dataset) + '\n')
    # print('train_samples_sum: ' + ' ' + str(train_dataset))
    # fwrite.write('train_sample_vul: ' + str(train_vul) + '    ' + 'train_sample_non_vul: ' + str(train_nonvul) + '\n')
    # print('train_sample_vul: ' + str(train_vul) + '    ' + 'train_sample_non_vul: ' + str(train_nonvul))
    # fwrite.write(
    #     'BatchSize:' + str(batchSize) + ' Layers:' + str(layers) + ' DropOut:' + str(dropout) + ' Epoch:10' + '\n')
    # print('BatchSize:' + str(batchSize) + ' Layers:' + str(layers) + ' DropOut:' + str(dropout) + ' Epoch:10')
    # fwrite.write('test_samples_sum: ' + ' ' + str(all_test_samples) + '\n')
    # print('test_samples_sum: ' + ' ' + str(all_test_samples))
    # fwrite.write('test_sample_vul: ' + str(test_vul) + '    ' + 'test_sample_non_vul: ' + str(test_nonvul) + '\n')
    # print('test_sample_vul: ' + str(test_vul) + '    ' + 'test_sample_non_vul: ' + str(test_nonvul))
    # fwrite.write("TP:" + str(TP) + ' FP:' + str(FP) + ' FN:' + str(FN) + ' TN:' + str(TN) + '\n')
    # print("TP:" + str(TP) + ' FP:' + str(FP) + ' FN:' + str(FN) + ' TN:' + str(TN))
    # FPR = 0.0
    # if FP + TN != 0:
    #     FPR = float(FP) / (FP + TN)
    # fwrite.write('FPR: ' + str(FPR) + '\n')
    # print('FPR: ' + str(FPR))
    # FNR = 0.0
    # if TP + FN != 0:
    #     FNR = float(FN) / (TP + FN)
    # fwrite.write('FNR: ' + str(FNR) + '\n')
    # print('FNR: ' + str(FNR))
    # Accuracy = float(TP + TN) / (all_test_samples)
    # fwrite.write('Accuracy: ' + str(Accuracy) + '\n')
    # print('Accuracy: ' + str(Accuracy))
    # fwrite.write('accuracy_inner: ' + str(accuracy) + '\n')
    # print('accuracy_inner: ' + str(accuracy))
    # precision = 0
    # if TP + FP != 0:
    #     precision = float(TP) / (TP + FP)
    # fwrite.write('precision: ' + str(precision) + '\n')
    # print('precision: ' + str(precision))
    # recall = 0
    # if TP + FN != 0:
    #     recall = float(TP) / (TP + FN)
    # fwrite.write('recall: ' + str(recall) + '\n')
    # print('recall: ' + str(recall))
    # f_score = 0
    # if precision + recall != 0:
    #     f_score = (2 * precision * recall) / (precision + recall)
    # fwrite.write('fbeta_score: ' + str(f_score) + '\n')
    # print('fbeta_score: ' + str(f_score))
    # fwrite.write('train_time:' + str(train_time) + '  ' + 'test_time:' + str(test_time) + '\n')
    # print('train_time:' + str(train_time) + '  ' + 'test_time:' + str(test_time))
    # fwrite.write('--------------------\n')
    # print('--------------------\n')
    # fwrite.close()

    """dict_testcase2func = {}
    for i in testcases:
        if not i in dict_testcase2func:
            dict_testcase2func[i] = {}
    TP_indexs = result[1]
    for i in TP_indexs:
        if funcs[i] == []:
            continue
        for func in funcs[i]:
            if func in dict_testcase2func[testcases[i]].keys():
                dict_testcase2func[testcases[i]][func].append("TP")
            else:
                dict_testcase2func[testcases[i]][func] = ["TP"]
    FP_indexs = result[1]
    for i in FP_indexs:
        if funcs[i] == []:
            continue
        for func in funcs[i]:
            if func in dict_testcase2func[testcases[i]].keys():
                dict_testcase2func[testcases[i]][func].append("FP")
            else:
                dict_testcase2func[testcases[i]][func] = ["FP"]
    f = open(resultpath + "_dict_testcase2func.pkl", 'wb')
    pickle.dump(dict_testcase2func, f)
    f.close()"""


def testrealdata(realtestpath, weightpath, batch_size, maxlen, vector_dim, layers, dropout):
    model = build_model(maxlen, vector_dim, layers, dropout)
    model.load_weights(weightpath)

    print("Loading data...")
    for filename in os.listdir(realtestpath):
        print(filename)
        f = open(realtestpath + filename, "rb")
        realdata = pickle.load(f, encoding="latin1")
        f.close()

        labels = model.predict(x=realdata[0], batch_size=1)
        for i in range(len(labels)):
            if labels[i][0] >= 0.5:
                print(realdata[1][i])


if __name__ == "__main__":
    batchSize = 32
    vectorDim = 30
    maxLen = 900
    layers = 2
    dropout = 0.1
    use_bias = True
    unit = 512
    traindataSetPath = "./dl_input/vul_data/sard/vec"
    testdataSetPath = "./dl_input/test_nvd_1/"
    realtestdataSetPath = "data/"
    weightPath = './model_gen'
    resultPath = "./result"
    print(traindataSetPath)
    if not os.path.exists(weightPath):
        os.mkdir(weightPath)
    if not os.path.exists(resultPath):
        os.mkdir(resultPath)
    weightPath = './model_gen'
    resultPath = "./result"
    #if not os.path.exists(weightPath):
    #    os.mkdir(weightPath)
    #if not os.path.exists(resultPath):
    #    os.mkdir(resultPath)
    print(f"layers:{layers}, dropout:{dropout}, use_bias:{use_bias}, unit:{unit}")
    main(traindataSetPath, testdataSetPath, realtestdataSetPath, weightPath, resultPath, batchSize, maxLen, vectorDim,
         layers, dropout, unit, use_bias)
    # testrealdata(realtestdataSetPath, weightPath, batchSize, maxLen, vectorDim, layers, dropout)
