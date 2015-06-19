#!/usr/bin/python
#-*- encoding: utf-8 -*-
# Quantitative Economics Web: http://quant-econ.net/py/index.html

from __future__ import division
import math
from random import shuffle
import numpy as np
import time
np.set_printoptions(threshold=np.nan)


def gale_shapley(applicant_prefers_input, host_prefers_input, **kwargs):
     start1 = time.time()
     unmatch = kwargs.get('unmatch', True)

     start3 = time.time()
     # 選好表の型チェック
     # listならnumpyへ変換
     if isinstance(applicant_prefers_input, list):
          applicant_preferences = np.array(applicant_prefers_input, dtype=int)

     elif isinstance(applicant_prefers_input, np.ndarray):
          applicant_preferences = applicant_prefers_input

     else:
          print("入力はlist型かnumpy.ndarray型にしてください")
          return False

     if isinstance(host_prefers_input, list):
          host_preferences = np.array(host_prefers_input, dtype=int)

     elif isinstance(host_prefers_input, np.ndarray):
          host_preferences = host_prefers_input

     else:
          print("入力はlist型かnumpy.ndarray型にしてください")
          return False

     stop3 = time.time() - start3
     print("変換は " + str(stop3) + " 秒でした")

     # unmatchマークが入力されていない時は、選好表の列の最後にunmatch列をつくる
     if not unmatch:
          dummy_host = np.array(np.arange(app_row, 1))
          applicant_preferences = np.c_[applicant_preferences, dummy_host]
          dummy_applicant = np.array(np.arange(hos_row, 1))
          host_preferences = np.c_[host_preferences, dummy_applicant]

     # 選好表の行列数をチェック
     app_row, app_col = applicant_preferences.shape
     host_row, host_col = host_preferences.shape

     if (app_row != host_col-1) or (host_row != app_col-1):
          print("ERROR: 2つの選好表のサイズが不適切です")
          return False

     applicant_unmatched_mark = app_col-1
     host_unmatched_mark = host_col-1

     # ソート
     start3 = time.time()
     host_preferences = np.argsort(host_preferences, axis=-1)
     stop3 = time.time() - start3
     print("ソートは " + str(stop3) + " 秒でした")

     # 未マッチング者のリスト
     stack = list(range(app_row))

     # マッチングを入れる（初期値は未マッチングflag）
     applicant_matchings = np.zeros(app_row, dtype=int) + applicant_unmatched_mark
     host_matchings = np.zeros(host_row, dtype=int) + host_unmatched_mark

     # メインループ
     start2 = time.time()
     while len(stack) > 0:
          # スタックから1人応募者を取り出す
          applicant = stack.pop()

          # 取り出した応募者の選好表
          applicant_preference = applicant_preferences[applicant]

          # 選好表の上から順番にプロポーズ
          for host in applicant_preference:
               #print(applicant, host)
               # unmatched_markまでapplicantがマッチングできなければ、アンマッチ
               if host == applicant_unmatched_mark:
                    break

               # プロポーズする相手の選好表
               host_preference = host_preferences[host]

               # 相手の選好表で、応募者と現在のマッチング相手のどちらが順位が高いのか比較する
               rank_applicant = host_preference[applicant]
               matched = host_matchings[host]
               rank_matched = host_preference[matched]
               
               # もし受け入れ側が新しい応募者の方を好むなら
               if rank_matched > rank_applicant:
                    applicant_matchings[applicant] = host
                    host_matchings[host] = applicant

                    # 既にマッチしていた相手がダミーでなければ、マッチングを解除する
                    if matched != host_unmatched_mark:
                         applicant_matchings[matched] = applicant_unmatched_mark
                         stack.append(matched)

                    break

     stop2 = time.time() - start2
     print("LOOPは " + str(stop2) + " 秒でした")
     return applicant_matchings, host_matchings


# ループする際、前回誰までプロポーズしたかを覚えておく
def gale_shapley2(applicant_prefers_input, host_prefers_input, **kwargs):
     start1 = time.time()
     unmatch = kwargs.get('unmatch', True)

     start3 = time.time()
     # 選好表の型チェック
     # listならnumpyへ変換
     if isinstance(applicant_prefers_input, list):
          applicant_preferences = np.array(applicant_prefers_input, dtype=int)

     elif isinstance(applicant_prefers_input, np.ndarray):
          applicant_preferences = applicant_prefers_input

     else:
          print("入力はlist型かnumpy.ndarray型にしてください")
          return False

     if isinstance(host_prefers_input, list):
          host_preferences = np.array(host_prefers_input, dtype=int)

     elif isinstance(host_prefers_input, np.ndarray):
          host_preferences = host_prefers_input

     else:
          print("入力はlist型かnumpy.ndarray型にしてください")
          return False

     # unmatchマークが入力されていない時は、選好表の列の最後にunmatch列をつくる
     if not unmatch:
          dummy_host = np.array(np.arange(app_row, 1))
          applicant_preferences = np.c_[applicant_preferences, dummy_host]
          dummy_applicant = np.array(np.arange(hos_row, 1))
          host_preferences = np.c_[host_preferences, dummy_applicant]


     # 選好表の行列数をチェック
     app_row, app_col = applicant_preferences.shape
     host_row, host_col = host_preferences.shape

     if (app_row != host_col-1) or (host_row != app_col-1):
          print("ERROR")
          return False

     applicant_unmatched_mark = app_col-1
     host_unmatched_mark = host_col-1

     stop3 = time.time() - start3
     print("変換は " + str(stop3) + " 秒でした")

     # ソート
     start4 = time.time()
     host_preferences = np.argsort(host_preferences, axis=-1)
     stop4 = time.time() - start4
     print("ソートは " + str(stop4) + " 秒でした")

     # 未マッチング者のリスト
     stack = list(range(app_row))

     # マッチングを入れる（初期値は未マッチングflag）
     applicant_matchings = np.zeros(app_row, dtype=int) + applicant_unmatched_mark
     host_matchings = np.zeros(host_row, dtype=int) + host_unmatched_mark

     # メインループ
     start2 = time.time()
     next_start = np.zeros(app_row, dtype=int)
     while len(stack) > 0:
          # スタックから1人応募者を取り出す
          applicant = stack.pop()

          # 取り出した応募者の選好表
          applicant_preference = applicant_preferences[applicant]

          # 選好表の上から順番にプロポーズ
          for index, host in enumerate(applicant_preference[next_start[applicant]:]):
               #print(applicant, host)
               # unmatched_markまでapplicantがマッチングできなければ、アンマッチ
               if host == applicant_unmatched_mark:
                    break

               # プロポーズする相手の選好表
               host_preference = host_preferences[host]

               # 相手の選好表で、応募者と現在のマッチング相手のどちらが順位が高いのか比較する
               rank_applicant = host_preference[applicant]
               matched = host_matchings[host]
               rank_matched = host_preference[matched]
               
               # もし受け入れ側が新しい応募者の方を好むなら
               if rank_matched > rank_applicant:
                    applicant_matchings[applicant] = host
                    host_matchings[host] = applicant

                    # 既にマッチしていた相手がダミーでなければ、マッチングを解除する
                    if matched != host_unmatched_mark:
                         applicant_matchings[matched] = applicant_unmatched_mark
                         stack.append(matched)

                    next_start[applicant] = index
                    break

     stop2 = time.time() - start2
     print("LOOPは " + str(stop2) + " 秒でした")
     return applicant_matchings, host_matchings


# 選好表をランダムに作る
def random_preference_table(row, col, **kwargs):
     unmatch = kwargs.get('unmatch', True)
     numpy = kwargs.get('numpy', False)

     if numpy:
          li = np.tile(np.arange(col+1, dtype=int), (row, 1))
          stop = None if unmatch else -1
          for i in li:
               np.random.shuffle(i[:stop])
          
          return li

     else:     
          def __sshuffle(li):
               shuffle(li)
               return li

          if unmatch:
               return [__sshuffle(list(range(col+1))) for i in range(row)]
          else:
               return [__sshuffle(list(range(col))) + [col+1] for i in range(row)]


# 巨大な選好表をきちんとランダムに作るのは大変時間がかかる
# そこで、選好のパターンをn個用意し、その中から選ぶようにする
def pseudo_random_preference_table(row, col, n=1000, **kwargs):
     unmatch = kwargs.get('unmatch', True)

     if n > row:
          n = row

     size = col+1 if unmatch else col
     sample = np.tile(np.arange(size, dtype=int), (n, 1))
     for i in sample:
          np.random.shuffle(i)

     index = np.random.randint(0, n, row)
     li = np.empty((row, size))
     li += sample[index]

     return li


if __name__ == '__main__':
     #app_table = [[3, 1, 0, 4, 2], [3, 4, 2, 0, 1]]
     #hos_table = [[2, 0, 1], [0, 1, 2], [0, 2, 1], [0, 2, 1]]
     #app_table = [[0, 2, 1, 3], [2, 1, 3, 0], [3, 1, 0, 2]]
     #hos_table = [[3, 0, 2, 1], [2, 0, 1, 3], [2, 0, 3, 1]]
     

     start = time.time()
     app_table = pseudo_random_preference_table(2000, 2000)
     hos_table = pseudo_random_preference_table(2000, 2000)
     stop = time.time() - start
     print("選好表生成は " + str(stop) + " 秒でした\n")


     print("GSアルゴリズム2 スタート!")
     start = time.time()
     matching = gale_shapley2(app_table, hos_table)
     stop = time.time() - start
     print("ストップ！")
     print("実行時間は " + str(stop) + " 秒でした\n")

     #print(matching[0], "\n")
     #print(matching[1])

     print("GSアルゴリズム3 スタート!")
     start = time.time()
     matching = gale_shapley3(app_table, hos_table)
     stop = time.time() - start
     print("ストップ！")
     print("実行時間は " + str(stop) + " 秒でした\n")

     #print(matching[0], "\n")
     #print(matching[1])










