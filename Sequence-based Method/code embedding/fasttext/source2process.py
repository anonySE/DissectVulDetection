import collections
from mapping import *
import datetime

startTime = datetime.datetime.now()

graph_indicate_reader = open("./SAGPool_Data_5/NVD_graph_indicator.txt","r")
lines = graph_indicate_reader.read().splitlines()
graph_indict_count = collections.Counter(lines)
graph_indict_count = dict(graph_indict_count)

attr_code_reader = open("./SAGPool_Data_5/NVD_attributes_code.txt","r")
code_lines = attr_code_reader.read().splitlines()

valueList = [int(value) for key,value in graph_indict_count.items()]

startIndex = 0
def compute_index(step):
    global startIndex
    nextIndex = startIndex + step
    startIndex = nextIndex
    return nextIndex

# slice for graph
file_dict = {}
for i,j in zip(graph_indict_count.keys(),valueList):
    pre_position = startIndex
    endIndex = compute_index(j)
    file_dict[i] = code_lines[pre_position:endIndex]

print(file_dict)
slicefile_corpus = []
slicefile_func = []
sentence_word_count = []

for value in file_dict.values():
    slice_corpus = []
    for sentence in value:
        sentence = sentence.strip()
        list_tokens = create_tokens(sentence)
        slice_corpus.append(list_tokens)

    # print(slice_corpus)
    sentence_len = []
    for i in slice_corpus:
        sentence_len.append(len(i))
    # print(sentence_len)
    sentence_word_count.append(sentence_len)

    # mapping
    slice_corpus, slice_func = mapping(slice_corpus)
    # print(slice_corpus)
    slice_func = list(set(slice_func))
    if slice_func == []:
        slice_func = ['main']
    sample_corpus = []
    for sentence in slice_corpus:
        list_tokens = create_tokens(sentence)
        sample_corpus = sample_corpus + list_tokens
    slicefile_corpus.append(sample_corpus)
    slicefile_func.append(slice_func)
    # print(slicefile_func)

line_word_count = {}
for i,j in zip(graph_indict_count.keys(),sentence_word_count):
    line_word_count[i] = j

process_file = open("./corpus/nvd/NVD_process_file_5.pkl","wb")
pickle.dump([slicefile_corpus, slicefile_func, line_word_count], process_file)
graph_indicate_reader.close()
attr_code_reader.close()
process_file.close()

endTime = datetime.datetime.now()
print("process finished!")
print("Cost Time:", endTime - startTime)
