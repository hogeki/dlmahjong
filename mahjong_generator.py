#-*- coding:utf-8 -*-
import copy
import argparse
import mahjong_common as mjc

class DahaiRecord:

    def __init__(self):
        self.haipai = None
        self.tehai = None
        self.tsumo = []
        self.dahai = []
        self.menzen = True
        self.tenpai = False
    
    def read_haipai(self, haipai_str):
        self.haipai = mjc.get_tehai_from_string(haipai_str)
        self.tehai = copy.deepcopy(self.haipai)
    
    def append_tsumo(self, hai):
        #print("ツモ:" + str(hai))
        if self.tenpai == True or self.menzen == False:
            return
        self.tsumo.append(hai)
        self.tehai[hai] += 1
    
    def append_dahai(self, hai):
        #print("打:" + str(hai))
        if self.tenpai == True or self.menzen == False:
            return
        self.dahai.append(hai)
        self.tehai[hai] -= 1
        self.check_tenpai()
    
    def check_tenpai(self):
        self.tenpai = mjc.is_tenpai(self.tehai)
    
    def naki(self):
        self.menzen = False

    def is_need_to_be_saved(self):
        #メンゼンで聴牌した記録のみ保存
        if self.menzen == True and self.tenpai == True:
            return True
        else:
            return False

    def write_to_file(self, f):
        tehai = copy.deepcopy(self.haipai)
        for i in range(0, len(self.tsumo)):
            t = self.tsumo[i]
            d = self.dahai[i]
            tehai[t] += 1
            f.write("{0} {1}\n".format(mjc.get_string_from_tehai(tehai), mjc.get_hai_string(d)))
            tehai[d] -= 1

class GameRecord:

    def __init__(self):
        self.dahai_records = [None for i in range(4)]
        self.saved_records = []        
        for i in range(4):
            self.dahai_records[i] = DahaiRecord()

    def read_record(self, filename, limit):
        num_of_games = 0
        with open(filename, "r", encoding="utf-8") as f:
            state = 1
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line[0] == "*":
                    state = 2
            
                if state == 1:
                    for p in [1, 2, 3, 4]:
                        if line.startswith("[" + str(p)):
                            self.dahai_records[p-1].read_haipai(line[4:])
                elif state == 2:
                    if line[0] != "*":
                        state = 1
                        for i in range(4):
                            #必要なデータのみ保存
                            if self.dahai_records[i].is_need_to_be_saved() == True:
                                self.saved_records.append(self.dahai_records[i])
                            #初期化
                            self.dahai_records[i] = DahaiRecord()
                        num_of_games += 1
                        print("number of games:" + str(num_of_games))
                        if num_of_games >= limit:
                            break
                        else:
                            continue
                    rec = line[1:].split(" ")
                    for r in rec:
                        r = r.strip()
                        if len(r) >= 2:
                            p = -1

                            if r[0] == "1":
                                p = 0
                            elif r[0] == "2":
                                p = 1
                            elif r[0] == "3":
                                p = 2
                            elif r[0] == "4":
                                p = 3

                            if p == -1:
                                continue

                            if r[1] == "G":
                                if len(r) >= 3:
                                    self.dahai_records[p].append_tsumo(mjc.get_hai_number(r[2:]))
                            elif r[1] == "D" or r[1] == "d":
                                if len(r) >= 3:
                                    self.dahai_records[p].append_dahai(mjc.get_hai_number(r[2:]))
                            elif r[1] == "K" or r[1] == "N" or r[1] == "C":
                                #ポン、チーをしてメンゼンを崩したらそのデータは捨てる
                                #カンはアンカンかもしれないが面倒なので捨てる
                                self.dahai_records[p].naki()
    
    def write_to_file(self, filename):
        with open(filename, mode="w", encoding="utf-8") as f:
            for r in self.saved_records:
                r.write_to_file(f)

    def print_saved(self):
        for r in self.saved_records:
            r.debug_print()
       
if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(prog = "mahjong_generator", add_help = True)
    arg_parser.add_argument("-i", "--input", help = "input file", default="houton2015.txt")
    arg_parser.add_argument("-o", "--output", help = "output file", default="dahai_data.txt")
    arg_parser.add_argument("-l", "--limit", help = "limit of number of games", type=int, default=40000)
    args = arg_parser.parse_args()

    game_record = GameRecord()
    game_record.read_record(args.input, args.limit)
    game_record.write_to_file(args.output)
