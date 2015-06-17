#!/usr/bin/python
#-*- encoding: utf-8 -*-
# Quantitative Economics Web: http://quant-econ.net/py/index.html

from __future__ import division
import math
from random import shuffle
import numpy as np
import time
np.set_printoptions(threshold=np.nan)


# 1対1のケースのDAアルゴリズム
def gale_shapley(applicant_prefers_input, host_prefers_input):

     # NumPy Arrayに変換
     applicant_preferences = np.array(applicant_prefers_input, dtype=int)
     host_preferences = np.array(host_prefers_input, dtype=int)

     # 選好表の行列数をチェック
     row, col = applicant_preferences.shape
     row_host, col_host = host_preferences.shape
     if row != col_host or col != row_host:
          exit(-1)

     # 選好表の各行の末尾に0（マッチング済みかどうかのflag）を追加
     zeros = np.zeros((row, 1), dtype=int)
     applicant_preferences = np.c_[applicant_preferences, zeros]
     host_preferences = np.c_[host_preferences, zeros]

     # 未マッチング者のリスト
     stack = list(range(row))

     # {man0: woman3, man1, woman0,...}というマッチングを入れる
     matching = {}

     while len(stack) > 0:
          # スタックから1人応募者を取り出す
          applicant = stack.pop()

          # 取り出した応募者の選好表
          applicant_preference = applicant_preferences[applicant]

          for host in applicant_preference:
               host_preference = host_preferences[host]

               # 相手が未マッチングなら
               if host_preference[-1] == 0:
                    host_preference[-1] = 1
                    applicant_preference[-1] = 1
                    matching[applicant] = host
                    break

               # 相手がマッチング済なら
               else:
                    # 既にマッチング済みの相手を代入
                    matched = [k for k, v in matching.items() if v == host][0]

                    # 新しい応募者と、既にマッチング済みの相手の、受け入れ側における選好順位を比較
                    rank_matched = np.where(host_preference[:-1] == matched)[0][0]
                    rank_applicant = np.where(host_preference[:-1] == applicant)[0][0]
                    
                    # もし受け入れ側が新しい応募者の方を好むなら
                    if rank_matched > rank_applicant:
                         applicant_preference[-1] = 1
                         del matching[matched]

                         matching[applicant] = host
                         applicant_preferences[matched][-1] = 0
                         stack.append(matched)
                         break

     return matching


# 1対1のケースのDAアルゴリズム
# host側の選好表を[1位の番号, 2位の番号,...]ではなく、[app1番の順位, app2番の順位,...]と変更してからやってみる
def gale_shapley2(applicant_prefers_input, host_prefers_input):
     start1 = time.time()

     # NumPy Arrayに変換
     applicant_preferences = np.array(applicant_prefers_input, dtype=int)
     host_preferences = np.array(applicant_prefers_input, dtype=int)

     # ソート
     host_preferences = np.argsort(host_preferences, axis=-1)

     # 選好表の行列数をチェック
     row, col = applicant_preferences.shape
     row_host, col_host = host_preferences.shape
     if row != col_host or col != row_host:
          exit(-1)

     # 選好表の各行の末尾に0（マッチング済みかどうかのflag）を追加
     zeros = np.zeros((row, 1), dtype=int)
     applicant_preferences = np.c_[applicant_preferences, zeros]
     host_preferences = np.c_[host_preferences, zeros]

     # 未マッチング者のリスト
     stack = list(range(row))

     # {man0: woman3, man1, woman0,...}というマッチングを入れる
     matching = {}

     stop1 = time.time() - start1
     print("準備は " + str(stop1) + " 秒でした")
     start2 = time.time()
     while len(stack) > 0:
          # スタックから1人応募者を取り出す
          applicant = stack.pop()

          # 取り出した応募者の選好表
          applicant_preference = applicant_preferences[applicant]

          for host in applicant_preference:
               host_preference = host_preferences[host]

               # 相手が未マッチングなら
               if host_preference[-1] == 0:
                    host_preference[-1] = 1
                    applicant_preference[-1] = 1
                    matching[applicant] = host
                    break

               # 相手がマッチング済なら
               else:
                    # 既にマッチング済みの相手を代入
                    matched = [k for k, v in matching.items() if v == host][0]

                    # 新しい応募者と、既にマッチング済みの相手の、受け入れ側における選好順位を比較
                    rank_matched = host_preference[matched]
                    rank_applicant = host_preference[applicant]
                    
                    # もし受け入れ側が新しい応募者の方を好むなら
                    if rank_matched > rank_applicant:
                         applicant_preference[-1] = 1
                         del matching[matched]

                         matching[applicant] = host
                         applicant_preferences[matched][-1] = 0
                         stack.append(matched)
                         break

     stop2 = time.time() - start2
     print("LOOPは " + str(stop2) + " 秒でした")
     return matching


# host側の選好表を[1位の番号, 2位の番号,...]ではなく、[app1番の順位, app2番の順位,...]と変更してからやってみる
def gale_shapley3(applicant_prefers_input, host_prefers_input):
     start1 = time.time()

     # NumPy Arrayに変換
     applicant_preferences = np.array(applicant_prefers_input, dtype=int)
     host_preferences = np.array(applicant_prefers_input, dtype=int)

     # ソート
     host_preferences = np.argsort(host_preferences, axis=-1)

     # 選好表の行列数をチェック
     row, col = applicant_preferences.shape
     row_host, col_host = host_preferences.shape
     if row != col_host or col != row_host:
          exit(-1)

     # 未マッチング者のリスト
     stack = list(range(row))

     # マッチングを入れる
     applicant_matchings = np.zeros(row, dtype=int) - 1
     host_matchings = np.zeros(row, dtype=int) - 1

     stop1 = time.time() - start1
     print("準備は " + str(stop1) + " 秒でした")
     start2 = time.time()
     while len(stack) > 0:
          # スタックから1人応募者を取り出す
          applicant = stack.pop()

          # 取り出した応募者の選好表
          applicant_preference = applicant_preferences[applicant]

          for host in applicant_preference:
               host_preference = host_preferences[host]

               # 既にマッチング済みの相手を代入
               matched = host_matchings[host]

               # 相手が未マッチングなら
               if matched == -1:
                    applicant_matchings[applicant] = host
                    host_matchings[host] = applicant
                    break

               # 相手がマッチング済なら
               else:
                    # 新しい応募者と、既にマッチング済みの相手の、受け入れ側における選好順位を比較
                    rank_matched = host_preference[matched]
                    rank_applicant = host_preference[applicant]
                    
                    # もし受け入れ側が新しい応募者の方を好むなら
                    if rank_matched > rank_applicant:
                         applicant_matchings[applicant] = host
                         host_matchings[host] = applicant
                         applicant_matchings[matched] = -1
                         stack.append(matched)
                         break

     stop2 = time.time() - start2
     print("LOOPは " + str(stop2) + " 秒でした")
     return [applicant_matchings]



# 選好表を適当に作る
def random_preference_table(row, col):

     def __sshuffle(li):
          shuffle(li)
          return li

     return [__sshuffle(list(range(col))) for i in range(row)]


if __name__ == '__main__':
     app_table = random_preference_table(2000, 2000)
     hos_table = random_preference_table(2000, 2000)


     print("gale-shapley2 スタート!")
     start = time.time()
     matching = gale_shapley2(app_table, hos_table)
     stop = time.time() - start
     print("ストップ！")
     print("実行時間は " + str(stop) + " 秒でした\n")
     #print(matching)

     print("gale-shapley3 スタート!")
     start = time.time()
     matching = gale_shapley3(app_table, hos_table)
     stop = time.time() - start
     print("ストップ！")
     print("実行時間は " + str(stop) + " 秒でした\n")
     #print(matching)
     
     """
     print("gale-shapley スタート!")
     start = time.time()
     matching = gale_shapley(app_table, hos_table)
     stop = time.time() - start
     print("ストップ！")
     print("実行時間は " + str(stop) + " 秒でした\n")

     print("gale-shapley2 スタート!")
     start = time.time()
     matching = gale_shapley2(app_table, hos_table)
     stop = time.time() - start
     print("ストップ！")
     print("実行時間は " + str(stop) + " 秒でした")
     """









