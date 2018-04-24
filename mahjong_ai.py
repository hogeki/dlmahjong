#-*- coding:utf-8 -*-
import sys
import io
import argparse
import time
import tensorflow as tf
import mahjong_common as mjc
import mahjong_loader as mjl

NUM_HAI = 34
NUM_HIDDEN_LAYERS = 3
H_SIZE = 200

sess = None
out = None
train_step = None
accuracy = None
x = None
y = None

def make_model():
    global x
    global y
    global train_labels
    global train_predictions
    global test_labels
    global test_predictions

    global train_step
    global out
    global train_accuracy
    global train_update_op
    global test_accuracy
    global test_update_op

    #入力データを定義
    x = tf.placeholder(tf.float32, [None, NUM_HAI])

    #重み
    w = []
    #バイアス
    b = []
    #隠れ層
    h = []

    #1層目の隠れ層
    w.append(tf.Variable(tf.truncated_normal([NUM_HAI, H_SIZE], stddev=0.1)))
    b.append(tf.Variable(tf.zeros([H_SIZE])))
    h.append(tf.nn.sigmoid(tf.matmul(x, w[0]) + b[0]))
    #h.append(tf.nn.relu(tf.matmul(x, w[0]) + b[0]))

    #2層目以降の隠れ層
    for i in range(1, NUM_HIDDEN_LAYERS):
        w.append(tf.Variable(tf.truncated_normal([H_SIZE, H_SIZE], stddev=0.1)))
        b.append(tf.Variable(tf.zeros([H_SIZE])))
        h.append(tf.nn.sigmoid(tf.matmul(h[i-1], w[i]) + b[i]))
        #h.append(tf.nn.relu(tf.matmul(h[i-1], w[i]) + b[i]))

    #出力層
    w.append(tf.Variable(tf.truncated_normal([H_SIZE, NUM_HAI], stddev=0.1)))
    b.append(tf.Variable(tf.zeros([NUM_HAI])))
    out = tf.nn.softmax(tf.matmul(h[NUM_HIDDEN_LAYERS-1], w[NUM_HIDDEN_LAYERS]) + b[NUM_HIDDEN_LAYERS])

    #正解データの型を定義
    y = tf.placeholder(tf.float32, [None, NUM_HAI])
    #誤差関数（クロスエントロピー）
    loss = tf.reduce_mean(-tf.reduce_sum(y * tf.log(out + 1e-5), axis=[1]))

    #訓練
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(loss)

    #評価
    #訓練データでの精度
    train_labels = tf.placeholder(tf.float32, [None, NUM_HAI])
    train_predictions = tf.placeholder(tf.float32, [None, NUM_HAI])
    train_accuracy, train_update_op = tf.metrics.accuracy(tf.argmax(train_labels, 1), tf.argmax(train_predictions, 1))
    #テストデータでの精度
    test_labels = tf.placeholder(tf.float32, [None, NUM_HAI])
    test_predictions = tf.placeholder(tf.float32, [None, NUM_HAI])
    test_accuracy, test_update_op = tf.metrics.accuracy(tf.argmax(test_labels, 1), tf.argmax(test_predictions, 1))


def train_ai(filename, num_of_epochs):
    mjl.load_dahai_data(filename)
    num_of_train_batches = mjl.get_num_of_train_batches()
    num_of_test_batches = mjl.get_num_of_test_batches()
    start_time = time.time()
    for i in range(num_of_epochs):
        for n in range(num_of_train_batches):
            #訓練
            batch_train_tehai = mjl.get_batch_train_tehai(n)
            batch_train_dahai = mjl.get_batch_train_dahai(n)
            sess.run(train_step, feed_dict={x:batch_train_tehai, y:batch_train_dahai})

        for n in range(num_of_train_batches):
            #訓練データに対する精度
            batch_train_tehai = mjl.get_batch_train_tehai(n)
            batch_train_dahai = mjl.get_batch_train_dahai(n)
            ai_outs = sess.run(out, feed_dict={x:batch_train_tehai})
            sess.run(train_update_op, feed_dict={train_labels:batch_train_dahai, train_predictions:ai_outs})

        for n in range(num_of_test_batches):
            #テストデータに対する精度
            batch_test_tehai = mjl.get_batch_test_tehai(n)
            batch_test_dahai = mjl.get_batch_test_dahai(n)
            ai_outs = sess.run(out, feed_dict={x:batch_test_tehai})
            sess.run(test_update_op, feed_dict={test_labels:batch_test_dahai, test_predictions:ai_outs})

        acc_val = sess.run(train_accuracy)
        print("Epoch {0}: train accuracy = {1}".format(i+1, acc_val))
        acc_val = sess.run(test_accuracy)
        print("Epoch {0}: test accuracy = {1}".format(i+1, acc_val))

    end_time = time.time()
    print("学習にかかった時間:{}秒".format(end_time-start_time))

def run_ai():
    test_count = 10000
    agari_count = 0
    tenpai_count = 0
    total_point = 0
    tenpai_kuzusi_count = 0
    yaku_count = {}
    for _ in range(test_count):
        result, yaku_strings, tenpai_kuzusi = test_ai()
        if result > 0:
            agari_count += 1
            total_point += result
            for yaku in yaku_strings:
                if yaku in yaku_count:
                    yaku_count[yaku] += 1
                else:
                    yaku_count[yaku] = 1
        elif result == 0:
            tenpai_count += 1
        elif result == -1:
            if tenpai_kuzusi == True:
                tenpai_kuzusi_count += 1
        
    print("和了:" + str(agari_count))
    print("和了時の平均点数:" + str(total_point / agari_count))
    print("役:" + str(yaku_count))        
    print("流局時聴牌:" + str(tenpai_count))
    print("聴牌崩し:" + str(tenpai_kuzusi_count))

def test_ai():
    mjc.init_yama()
    tehai = mjc.get_haipai()
    tsumo = -1
    tsumo_count = 0
    tenpai = False

    print("--------麻雀AIのテスト--------")
    while tsumo_count < 18:
        tstr = mjc.get_string_from_tehai(tehai)
        print("手牌:" + tstr)

        tsumo = mjc.get_tsumo()
        if tsumo == -1:
            break
        tsumo_count += 1
        print("自摸:" + mjc.get_hai_string(tsumo))
        tehai[tsumo] += 1
        if mjc.is_agari(tehai):
            print("和了")
            tehai[tsumo] -= 1
            info = mjc.AgariInfo(tehai, tsumo)
            print(info.get_yaku_strings())
            return (info.get_point(), info.get_yaku_strings(), False)
        
        ai_outs = sess.run(out, feed_dict={x:[tehai]})
        dahai = get_ai_dahai(tehai, ai_outs[0])
        print("打:" + mjc.get_hai_string(dahai))
        tehai[dahai] -= 1
        #一度でも聴牌したらフラグを立てる
        if tenpai == False and mjc.is_tenpai(tehai):
            tenpai = True

    if mjc.is_tenpai(tehai):
        print("流局(聴牌)")
        return (0, [], False)
    else:
        if tenpai == True:
            #聴牌を崩した
            print("流局(聴牌崩し)")
            return (-1, [], True)
        else:
            print("流局")
            return (-1, [], False)
    
def get_ai_dahai(ai_in, ai_out):
    eval_idx = 0
    eval_max = 0
    while True:
        for i in range(len(ai_out)):
            if eval_max < ai_out[i]:
                eval_max = ai_out[i]
                eval_idx = i
        if ai_in[eval_idx] > 0:
            return eval_idx
        else:
            ai_out[eval_idx] = 0
            eval_max = 0


if __name__ == "__main__":
    #for windows
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    arg_parser = argparse.ArgumentParser(prog = "mahjong_ai", add_help = True)
    arg_parser.add_argument("-r", "--run", help = "run AI", action = "store_true", default=False)
    arg_parser.add_argument("-t", "--train", help = "train AI", action = "store_true", default=False)
    arg_parser.add_argument("-e", "--epochs", help = "number of epochs", type=int, default=5)
    arg_parser.add_argument("-s", "--save", help="save model after training", action="store_true", default=False)
    arg_parser.add_argument("-m", "--model", help = "specify model", default="ckpt/my_model")
    arg_parser.add_argument("-d", "--datafile", help="specify train data file", default = "dahai_data.txt")
    args = arg_parser.parse_args()

    do_train = True
    do_run = True

    if args.run == True and args.train == False:
        do_train = False
    elif args.run == False and args.train == True:
        do_run = False
   
    make_model()
    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())
    if do_train == True:
        train_ai(args.datafile, args.epochs)
        if args.save == True:
            saver.save(sess, args.model)
    else:
        saver.restore(sess, args.model)
    if do_run == True:
        run_ai()

    

