ディープラーニングによる麻雀の何切るAI

14枚の手牌から切る牌を選ぶだけの簡易的な麻雀のAIです。
Python3.6.5とTensorFlowの1.7.0を使っています。

python mahjong_ai.py

を実行すると教師データ(dahai_data.txt)から学習を行い、その後テストを行います。

python mahjong_ai.py --train --save

を実行すると学習のみを行い、学習したパラメータを保存します。

python mahjong_ai.py --run

を実行するとテストのみを行います。

python mahjong_generator.py

を実行すると天鳳の牌譜から教師データを生成します。
(※天鳳の牌譜の文字コードはUTF8に変換しておいてください。)