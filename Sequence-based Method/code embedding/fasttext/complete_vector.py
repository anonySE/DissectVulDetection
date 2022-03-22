import pickle
import numpy as np
import torch
import math
import datetime

def get_array(content):
    word_count = []
    array_index = {}
    for key,value in content[2].items():
        word_count += value
        for i in range(1, len(value)):
            value[i] = value[i] + value[i - 1]
        array_index[key] = [0] + value
    return word_count,array_index

def number_op(x):
    if x != 0:
        x = int(x * 1000000) / 1000000
    return x

def batch_complete(batch_data,batch_array_slice,batch_time,max_len):
    complete_data = []
    # fill_array = np.zeros(30,dtype='float32')
    fill_list = [0] * 30
    for i in range(0,len(batch_data)):
        array_slice = batch_array_slice[i]
        for j in range(0,len(array_slice)-1):
            startIndex = array_slice[j]
            endIndex = array_slice[j+1]
            non_complete_line_vector = batch_data[i][startIndex:endIndex]
            temp_list = []
            for k in non_complete_line_vector:
                temp_list += k.tolist()

            # 补全
            if len(non_complete_line_vector) < max_len:
                fill_length = max_len - len(non_complete_line_vector)
                temp_list += fill_length * fill_list

            # 截断
            if len(non_complete_line_vector) > max_len:
                cut_index = max_len * 30
                temp_list = temp_list[:cut_index]

            temp_list = list(map(number_op,temp_list))
            complete_data.append(temp_list)

    node_labels_path = './batch_vector/NVD_node_labels_' + str(batch_time) + '.pkl'
    complete_vector = open(node_labels_path,'wb')
    pickle.dump(complete_data,complete_vector,protocol=pickle.HIGHEST_PROTOCOL)
    complete_vector.close()

    print('batch %d has been processed!' % (batch_time))

def main():
    startTime = datetime.datetime.now()

    source_vector = open(r'./vector/nvd/NVD_process_file_5.pkl', 'rb')
    content = pickle.load(source_vector)
    source_vector.close()

    word_count,array_index = get_array(content)
    # print("word_count: ",word_count)
    # print("array_index: ",array_index)
    word_count.sort()
    # max_len_index = math.ceil(len(word_count) * 0.95) - 1   # “向上取整”
    # max_len = word_count[max_len_index]  # 每行保留的最大长度，覆盖95%以上的数据
    max_len = 20
    array_slice = [value for value in array_index.values()]
    
    data = content[0]
    batch_times = 20
    batch_size = math.ceil(len(data)/batch_times)
    # 分批处理数据
    for batch_time in range(0,batch_times):
        batch_data = data[batch_time*batch_size:(batch_time+1)*batch_size]
        batch_array_slice = array_slice[batch_time*batch_size:(batch_time+1)*batch_size]
        batch_complete(batch_data,batch_array_slice,batch_time,max_len)

    # 合并数据
    tensor_list = []
    for file_indicator in range(0,batch_times):
        file_name = './batch_vector/NVD_node_labels_' + str(file_indicator) + '.pkl'
        file_reader = open(file_name, 'rb')
        batch_list = pickle.load(file_reader)
        file_reader.close()
        tensor_list += batch_list

    tensor_data_writer = open(r'./SAGPool_Data_5/NVD_node_attributes.txt','w')

    for line_list in tensor_list:
        format_line_vector = str(line_list).replace('[','').replace(']','') + '\n'
        # print(format_line_vector)
        tensor_data_writer.write(format_line_vector)

    tensor_data_writer.close()

    endTime = datetime.datetime.now()
    print('Complete finished!')
    print("Cost Time:", endTime - startTime)
    

if __name__ == '__main__':
    main()