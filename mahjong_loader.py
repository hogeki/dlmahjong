#-*- coding:utf-8 -*-

import random
import mahjong_common as mjc

BATCH_SIZE = 50
TEST_DATA_RATIO = 0.1

train_tehai_list = None
train_dahai_list = None
test_tehai_list = None
test_dahai_list = None

def load_dahai_data(filename):
    global train_tehai_list
    global train_dahai_list
    global test_tehai_list
    global test_dahai_list

    tehai_dahai_list = []

    with open(filename, mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            d = line.split(" ")
            tehai = mjc.get_tehai_from_string(d[0])
            dahai = [0 for i in range(34)]
            dahai[mjc.get_hai_number(d[1])] = 1
            tehai_dahai_list.append([tehai, dahai])
    
    random.shuffle(tehai_dahai_list)
    train_data_size = int(len(tehai_dahai_list) * (1.0 - TEST_DATA_RATIO))
    train_tehai_list = [tehai_dahai[0] for tehai_dahai in tehai_dahai_list[:train_data_size]]
    train_dahai_list = [tehai_dahai[1] for tehai_dahai in tehai_dahai_list[:train_data_size]]
    test_tehai_list = [tehai_dahai[0] for tehai_dahai in tehai_dahai_list[train_data_size:]]
    test_dahai_list = [tehai_dahai[1] for tehai_dahai in tehai_dahai_list[train_data_size:]]

def get_train_tehai():
    return train_tehai_list

def get_train_dahai():
    return train_dahai_list

def get_test_tehai():
    return test_tehai_list

def get_test_dahai():
    return test_dahai_list

def get_num_of_train_batches():
    return len(train_tehai_list) // BATCH_SIZE - 1

def get_num_of_test_batches():
    return len(test_tehai_list) // BATCH_SIZE - 1

def get_batch_train_tehai(n):
    idx = n * BATCH_SIZE
    return train_tehai_list[idx : idx+BATCH_SIZE]

def get_batch_train_dahai(n):
    idx = n * BATCH_SIZE
    return train_dahai_list[idx : idx+BATCH_SIZE]

def get_batch_test_tehai(n):
    idx = n * BATCH_SIZE
    return test_tehai_list[idx : idx+BATCH_SIZE]

def get_batch_test_dahai(n):
    idx = n * BATCH_SIZE
    return test_dahai_list[idx : idx+BATCH_SIZE]

if __name__ == "__main__":
    pass