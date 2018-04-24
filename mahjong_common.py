#-*- coding:utf-8 -*-
import random
import copy

M1 = 0
M2 = 1
M3 = 2
M4 = 3
M5 = 4
M6 = 5
M7 = 6
M8 = 7
M9 = 8
P1 = 9
P2 = 10
P3 = 11
P4 = 12
P5 = 13
P6 = 14
P7 = 15
P8 = 16
P9 = 17
S1 = 18
S2 = 19
S3 = 20
S4 = 21
S5 = 22
S6 = 23
S7 = 24
S8 = 25
S9 = 26
TON = 27
NAN = 28
SHA = 29
PEI = 30
HAKU = 31
HATSU = 32
CHUN = 33

yama = None

class AgariInfo:

    MENZEN_TSUMO = 0x01
    YAKU_TON = 0x02
    YAKU_NAN = 0x04
    YAKU_SHA = 0x08
    YAKU_PEI = 0x10
    YAKU_HAKU = 0x20
    YAKU_HATSU = 0x40
    YAKU_CHUN = 0x80
    TANYAO = 0x100
    PINHU = 0x200
    IPEIKO = 0x400
    SANSYOKU_DOUJYUN = 0x800
    SANSYOKU_DOUKOU = 0x1000
    IKKITSUKAN = 0x2000
    CHITOITSU = 0x4000
    TOITOI = 0x8000
    CHANTA = 0x10000
    SANANKO = 0x20000
    SANKANTSU = 0x40000
    RYANPEIKO = 0x80000
    JYUNCHAN = 0x100000
    HONITSU = 0x200000
    SYOUSANGEN = 0x400000
    HONROUTOU = 0x800000
    CHINITSU = 0x1000000
    SUANKO = 0x2000000
    DAISANGEN = 0x4000000
    KOKUSIMUSOU = 0x8000000
    RYUISOU = 0x10000000
    TUISOU = 0x20000000
    CHINROUTOU = 0x40000000
    SUKANTSU = 0x80000000
    SYOUSUSI = 0x100000000
    DAISUSI = 0x200000000
    CHURENPOTO = 0x400000000
    CHIHOU = 0x800000000
    TENHOU = 0x1000000000

    yaku_dic = {MENZEN_TSUMO:["門前自摸", 1],
                YAKU_TON:["東", 1],
                YAKU_NAN:["南", 1],
                YAKU_SHA:["西", 1],
                YAKU_PEI:["北", 1],
                YAKU_HAKU:["白", 1],
                YAKU_HATSU:["発", 1],
                YAKU_CHUN:["中", 1],
                TANYAO:["断么", 1],
                PINHU:["平和", 1],
                IPEIKO:["一盃口", 1],
                SANSYOKU_DOUJYUN:["三色同順", 2],
                SANSYOKU_DOUKOU:["三色同刻", 2],
                IKKITSUKAN:["一気通貫", 2],
                CHITOITSU:["七対子", 2],
                TOITOI:["トイトイ", 2],
                CHANTA:["チャンタ", 2],
                SANANKO:["三暗刻", 2],
                SANKANTSU:["三槓子", 2],
                RYANPEIKO:["二盃口", 3],
                JYUNCHAN:["純チャン", 3],
                HONITSU:["混一色", 2],
                SYOUSANGEN:["小三元", 2],
                HONROUTOU:["混老頭", 2],
                CHINITSU:["清一色", 6],
                SUANKO:["四暗刻", 13],
                DAISANGEN:["大三元", 13],
                KOKUSIMUSOU:["国士無双", 13],
                RYUISOU:["緑一色", 13],
                TUISOU:["字一色",13],
                CHINROUTOU:["清老頭", 13],
                SUKANTSU:["四槓子", 13],
                SYOUSUSI:["小四喜", 13],
                DAISUSI:["大四喜", 26],
                CHURENPOTO:["九連宝灯", 13],
                CHIHOU:["地和", 13],
                TENHOU:["天和", 13]
                }

    def __init__(self, tehai, tsumo):
        self.agari = False
        self.yaku_flags = 0
        changed = True

        for i in range(M1, CHUN+1):
            if changed == True:
                t = copy.deepcopy(tehai)
                t[tsumo] += 1

            #雀頭を決める
            if t[i] >= 2:
                self.hu = 20
                changed = True
                shuntsu_only = True
                chanta = True
                jyunchan = True
                ton = False
                nan = False
                haku = False
                hatsu = False
                chun = False

                if self.is_19(i) == False:
                    jyunchan = False
                    if self.is_jihai(i) == False:
                        chanta = False
                #頭が役牌なら2符がつく
                if i in [TON, NAN, HAKU, HATSU, CHUN]:
                    self.hu += 2

                t[i] -= 2

                #刻子の判定
                shabo = False
                num_anko = 0
                koutsu_count = [0 for i in range(M1, CHUN+1)]    
                for j in range(M1, CHUN+1):
                    if t[j] >= 3:
                        t[j] -= 3
                        shuntsu_only = False
                        num_anko += 1
                        if j == tsumo:
                            shabo = True
                        koutsu_count[j] += 1
                        if j  == TON:
                            ton = True
                        elif j == NAN:
                            nan = True
                        elif j == HAKU:
                            haku = True
                        elif j == HATSU:
                            hatsu = True
                        elif j == CHUN:
                            chun = True

                        if self.is_19(j) == False:
                            jyunchan = False
                            if self.is_jihai(j) == False:
                                chanta = False
                        
                        #ヤオチュー牌なら8符、それ以外は4符
                        if self.is_yaochu(j):
                            self.hu += 8
                        else:
                            self.hu += 4
            
                #順子の判定
                ryanmen = False
                shuntsu_count = [0 for i in range(M1, S8)] 
                for j in range(M1, S8):
                    while is_shuntsu(t, j):
                        t[j] -= 1
                        t[j+1] -= 1
                        t[j+2] -= 1
                        shuntsu_count[j] += 1
                        
                        if j not in [M1, M7, P1, P7, S1, S7]:
                            jyunchan = False
                            chanta = False

                        if j == tsumo and j not in [M7, P7, S7]:
                            ryanmen = True
                        elif j+2 == tsumo and j+2 not in [M3, P3, S3]:
                            ryanmen = True

                if sum(t) == 0:
                    self.agari = True
                    #リャンメンでもシャボでもなければ2符つく
                    if ryanmen == False and shabo == False:
                        self.hu += 2
                    if self.is_tanyao(tehai, tsumo):
                        self.yaku_flags |= AgariInfo.TANYAO
                    if self.check_pinhu_jihai(tehai, tsumo) == True and shuntsu_only == True and ryanmen == True:
                        self.yaku_flags |= AgariInfo.PINHU
                    else:
                        #ツモあがりなので基本的には2符つくが、平和ツモのときはつかない
                        self.hu += 2
                    if self.is_ikkitsukan(shuntsu_count):
                        self.yaku_flags |= AgariInfo.IKKITSUKAN
                    if self.is_sansyoku_doujyun(shuntsu_count):
                        self.yaku_flags |= AgariInfo.SANSYOKU_DOUJYUN
                    if self.is_sansyoku_doukou(koutsu_count):
                        self.yaku_flags |= AgariInfo.SANSYOKU_DOUKOU
                    shuntsu_pair = [i for i in range(M1, S8) if shuntsu_count[i] == 2]
                    if len(shuntsu_pair) == 1:
                        self.yaku_flags |= AgariInfo.IPEIKO
                    elif len(shuntsu_pair) == 2:
                        self.yaku_flags |= AgariInfo.RYANPEIKO

                    if ton == True:
                        self.yaku_flags |= AgariInfo.YAKU_TON
                    if nan == True:
                        self.yaku_flags |= AgariInfo.YAKU_NAN
                    if haku == True:
                        self.yaku_flags |= AgariInfo.YAKU_HAKU
                    if hatsu == True:
                        self.yaku_flags |= AgariInfo.YAKU_HATSU
                    if chun == True:
                        self.yaku_flags |= AgariInfo.YAKU_CHUN

                    if num_anko == 3:
                        self.yaku_flags |= AgariInfo.SANANKO
                    elif num_anko == 4:
                        self.yaku_flags |= AgariInfo.SUANKO                    

                    somete = self.check_somete(tehai, tsumo)
                    if somete == 2:
                        self.yaku_flags |= AgariInfo.CHINITSU
                    elif somete == 1:
                        self.yaku_flags |= AgariInfo.HONITSU

                    if jyunchan == True:
                        self.yaku_flags |= AgariInfo.JYUNCHAN
                    elif chanta == True:
                        self.yaku_flags |= AgariInfo.CHANTA

                    if self.is_daisangen(koutsu_count):
                        self.yaku_flags |= AgariInfo.DAISANGEN
                    elif self.is_syousangen(koutsu_count, i):
                        self.yaku_flags |= AgariInfo.SYOUSANGEN

                    chinroutou_tsuisou = self.check_chinroutou_tsuisou(tehai, tsumo)
                    if chinroutou_tsuisou == 1:
                        self.yaku_flags |= AgariInfo.CHINROUTOU
                    elif chinroutou_tsuisou == 2:
                        self.yaku_flags |= AgariInfo.TUISOU
                    #混老頭はチェックしない(門前ならどうせ四暗刻がつくので)

                    if self.yaku_flags >= AgariInfo.SUANKO:
                        #役満なら役満以外の役をクリア
                        yakuman_mask = ~(AgariInfo.SUANKO - 1)
                        self.yaku_flags &= yakuman_mask
                    
                    #符の切り上げ
                    if self.hu % 10 > 0:
                        self.hu = self.hu // 10 * 10 + 10

                    return
                    
            else:
                changed = False

        #七対子のチェック
        self.check_chitoitsu(tehai, tsumo)
        if self.agari == False:
            #国士無双のチェック
            self.check_kokushimusou(tehai, tsumo)
 
    def is_tanyao(self, tehai, tsumo):
        yaochu = [M1, M9, P1, P9, S1, S9, TON, NAN, SHA, PEI, HAKU, HATSU, CHUN]
        for i in yaochu:
            if tehai[i] > 0:
                return False
        if tsumo in yaochu:
            return False
        return True

    def is_ikkitsukan(self, shuntsu_count):
        if shuntsu_count[M1] > 0 and shuntsu_count[M4] > 0 and shuntsu_count[M7] > 0:
            return True
        if shuntsu_count[P1] > 0 and shuntsu_count[P4] > 0 and shuntsu_count[P7] > 0:
            return True
        if shuntsu_count[S1] > 0 and shuntsu_count[S4] > 0 and shuntsu_count[S7] > 0:
            return True
        return False

    def is_sansyoku_doujyun(self, shuntsu_count):
        for i in range(M1, M8):
            if shuntsu_count[i] > 0 and shuntsu_count[i+9] > 0 and shuntsu_count[i+18] > 0:
                return True
        return False
    
    def is_sansyoku_doukou(self, koutsu_count):
        for i in range(M1, P1):
            if koutsu_count[i] > 0 and koutsu_count[i+9] > 0 and koutsu_count[i+18] > 0:
                return True
        return False

    def is_daisangen(self, koutsu_count):
        if koutsu_count[HAKU] == 1 and koutsu_count[HATSU] == 1 and koutsu_count[CHUN] == 1:
            return True
        return False

    def is_syousangen(self, koutsu_count, atama):
        if atama in [HAKU, HATSU, CHUN]:
            if (koutsu_count[HAKU] == 1 and koutsu_count[HATSU] == 1) or (koutsu_count[HAKU] == 1 and koutsu_count[CHUN] == 1) or (koutsu_count[HATSU] == 1 and koutsu_count[CHUN] == 1):
               return True
        return False 

    def check_pinhu_jihai(self, tehai, tsumo):
        yakuhai = [TON, HAKU, HATSU, CHUN]
        for i in yakuhai:
            if tehai[i] > 0:
                return False
        if tsumo in yakuhai:
            return False
        return True
    
    #混一色なら1、清一色なら2を返す
    def check_somete(self, tehai, tsumo):
        t = copy.deepcopy(tehai)
        t[tsumo] += 1
        
        num_manzu = 0
        for i in range(M1, M9+1):
            num_manzu += t[i]
        
        num_pinzu = 0
        for i in range(P1, P9+1):
            num_pinzu += t[i]

        num_souzu = 0
        for i in range(S1, S9+1):
            num_souzu += t[i]
        
        num_jihai = 0
        for i in range(TON, CHUN+1):
            num_jihai += t[i]
        
        if (num_manzu == 0 and num_pinzu == 0) or (num_manzu ==0 and num_souzu == 0) or (num_pinzu == 0 and num_souzu == 0):
            if num_jihai == 0:
                return 2
            else:
                return 1
        else:
            return 0

    #チンロウトウなら1、字一色なら2、ホンロートーなら3を返す
    def check_chinroutou_tsuisou(self, tehai, tsumo):
        num_chunchan = 0
        num_19 = 0
        num_jihai = 0

        for i in range(M1, CHUN+1):
            if self.is_chunchan(i):
                num_chunchan += tehai[i]
            elif self.is_19(i):
                num_19 += tehai[i]
            elif self.is_jihai(i):
                num_jihai += tehai[i]
        
        for i in range(M1, CHUN+1):
            if self.is_chunchan(tsumo):
                num_chunchan += 1
            elif self.is_19(tsumo):
                num_19 += tsumo
            elif self.is_jihai(tsumo):
                num_jihai += tsumo
        
        if num_chunchan == 0:
            if num_19 > 0 and num_jihai == 0:
                return 1
            elif num_19 == 0 and num_jihai > 0:
                return 2
            else:
                return 3

    def is_chunchan(self, i):
        if i in [M2, M3, M4, M5, M6, M7, M8, P2, P3, P4, P5, P6, P7, P8, S2, S3, S4, S5, S6, S7, S8]:
            return True
        else:
            return False
    
    def is_yaochu(self, i):
        if i in [M1, M9, P1, P9, S1, S9, TON, NAN, SHA, PEI, HAKU, HATSU, CHUN]:
            return True
        else:
            return False
    
    def is_19(self, i):
        if i in [M1, M9, P1, P9, S1, S9]:
            return True
        else:
            return False
    
    def is_jihai(self, i):
        if i in [TON, NAN, SHA, PEI, HAKU, HATSU, CHUN]:
            return True
        else:
            return False
    
    def check_chitoitsu(self, tehai, tsumo):
        t = copy.deepcopy(tehai)
        t[tsumo] += 1
        if is_agari_chitoitsu(t):
            self.agari = True
            self.yaku_flags |= AgariInfo.CHITOITSU
            self.hu = 25 #七対子は25符固定
            somete = self.check_somete(tehai, tsumo)
            if somete == 2:
                self.yaku_flags |= AgariInfo.CHINITSU
            elif somete == 1:
                self.yaku_flags |= AgariInfo.HONITSU
            chinroutou_tsuisou = self.check_chinroutou_tsuisou(tehai, tsumo)
            if chinroutou_tsuisou == 1:
                self.yaku_flags |= AgariInfo.CHINROUTOU
            elif chinroutou_tsuisou == 2:
                self.yaku_flags |= AgariInfo.TUISOU
            elif chinroutou_tsuisou == 3:
                self.yaku_flags |= AgariInfo.HONROUTOU
            
            if self.yaku_flags >= AgariInfo.SUANKO:
                #役満なら役満以外の役をクリア
                yakuman_mask = ~(AgariInfo.SUANKO - 1)
                self.yaku_flags &= yakuman_mask
    
    def check_kokushimusou(self, tehai, tsumo):
        t = copy.deepcopy(tehai)
        t[tsumo] += 1
        if is_agari_kokushi(t):
            self.agari = True
            self.yaku_flags |= AgariInfo.KOKUSIMUSOU

    def is_agari(self):
        return self.agari

    def get_yaku_strings(self):
        str_list = []
        for shift in range(64):
            flag = 1 << shift
            if self.yaku_flags & flag != 0:
                str_list.append(AgariInfo.yaku_dic[flag][0])
        return str_list
    
    def get_han(self):
        #門前ツモで1ハン
        han = 1
        for shift in range(64):
            flag = 1 << shift
            if self.yaku_flags & flag != 0:
                han += AgariInfo.yaku_dic[flag][1]
        return han

    def calc_point(self, han):
        point = self.hu * 4 * pow(2, han+2)
        if point % 100 == 0:
            return point
        else:
            return (point // 100 + 1) * 100

    def get_point(self):
        han = self.get_han()
        if han <= 2:
            return self.calc_point(han)
        if han == 3:
            if(self.hu <= 60):
                return self.calc_point(han)
            else:
                #70符以上は満貫
                return 8000
        if han == 4:
            if(self.hu <= 30):
                return self.calc_point(han)
            else:
                #40符以上は満貫
                return 8000
        elif han == 5:
            return 8000
        elif han >= 6 and han <= 7:
            return 12000
        elif han >= 8 and han <= 10:
            return 16000
        elif han >=11 and han <= 12:
            return 24000
        elif han >= 13:
            return (han // 13) * 32000
        

def is_tenpai(tehai):
    waiting = get_waiting(tehai)
    if len(waiting) > 0:
        return True
    else:
        return False

def get_waiting(tehai):
    waiting = []
    for i in range(M1, CHUN+1):
        tehai[i] += 1
        if is_agari(tehai):
            waiting.append(i)
        tehai[i] -= 1
    return waiting

def is_agari(tehai):
    changed = True
    for i in range(M1, CHUN+1):
        if changed == True:
            t = copy.deepcopy(tehai)

        #雀頭を決める
        if t[i] >= 2:
            changed = True
            t[i] -= 2

            #刻子の判定    
            for j in range(M1, CHUN+1):
                if t[j] >= 3:
                    t[j] -= 3
            
            #順子の判定
            for j in range(M1, S8):
                while is_shuntsu(t, j):
                    t[j] -= 1
                    t[j+1] -= 1
                    t[j+2] -= 1

            if sum(t) == 0:
                return True
        else:
            changed = False
    
    #七対子のチェック
    if is_agari_chitoitsu(tehai):
        return True
    
    #国士無双のチェック
    if is_agari_kokushi(tehai):
        return True

    return False

def is_agari_chitoitsu(tehai):
    for i in range(M1, CHUN+1):
        if(tehai[i] == 1 or tehai[i] == 3):
            return False
    return True

def is_agari_kokushi(tehai):
    for i in [M1, M9, P1, P9, S1, S9, TON, NAN, SHA, PEI, HAKU, HATSU, CHUN]:
        if tehai[i] == 0:
            return False
    
    for i in range(M2, M9):
        if tehai[i] > 0:
            return False

    for i in range(P2, P9):
        if tehai[i] > 0:
            return False

    for i in range(S2, S9):
        if tehai[i] > 0:
            return False

    return True    

def is_shuntsu(tehai, i):
    if i in [M8, M9, P8, P9, S8, S9, TON, NAN, SHA, PEI, HAKU, HATSU, CHUN]:
        return False
    else:
        if tehai[i] >= 1 and tehai[i+1] >= 1 and tehai[i+2] >= 1:
            return True
        else:
            return False

def init_yama():
    global yama
    yama = []
    for h in range(CHUN+1):
        for _ in range(4):
            yama.append(h)
    random.shuffle(yama)

def get_tsumo():
    if len(yama) > 0:
        return yama.pop()
    else:
        return -1

def get_haipai():
    haipai = [0 for i in range(CHUN+1)]
    for _ in range(13):
        h = get_tsumo()
        haipai[h] += 1
    return haipai    

def get_hai_string(num):
    table = ["1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m",
             "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",
             "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
             "東", "南", "西", "北", "白", "発", "中"]
    if num >= M1 and num <= CHUN:
        return table[num]
    else:
        return "Invalid"
        

def get_hai_number(hai_str):
    dic = {"1m":M1, "2m":M2, "3m":M3, "4m":M4, "5m":M5, "6m":M6, "7m":M7, "8m":M8, "9m":M9,
           "1p":P1, "2p":P2, "3p":P3, "4p":P4, "5p":P5, "6p":P6, "7p":P7, "8p":P8, "9p":P9,
           "1s":S1, "2s":S2, "3s":S3, "4s":S4, "5s":S5, "6s":S6, "7s":S7, "8s":S8, "9s":S9,
           "5M":M5, "5P":P5, "5S":S5,
           "東":TON, "南":NAN, "西":SHA, "北":PEI, "白":HAKU, "発":HATSU, "中":CHUN}
    if hai_str in dic:
        return dic[hai_str]
    else:
        return -1

def get_tehai_from_string(tehai_str):
    tehai = [0 for i in range(CHUN+1)]
    for i in range(len(tehai_str)):
        n = tehai_str[i]
        if n in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            if i < len(tehai_str) - 1:
                mps = tehai_str[i+1]
                if mps in ["m", "p", "s"]:
                    tehai[get_hai_number(n+mps)] += 1
        elif n in ["東", "南", "西", "北", "白", "発", "中"]:
            tehai[get_hai_number(n)] += 1
    return tehai

def get_string_from_tehai(tehai):
    tehai_str = ""
    for i in range(CHUN+1):
        num = tehai[i]
        for _ in range(num):
            tehai_str += get_hai_string(i)
    return tehai_str   

if __name__ == '__main__':
    info = AgariInfo(get_tehai_from_string("1p1p5p5p6p6p3s3s4s4s中中東"), TON)
    print(info.is_agari())
    print(info.get_yaku_strings())
    print(info.get_point())
    