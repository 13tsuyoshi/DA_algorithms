#!/usr/bin/python
#-*- encoding: utf-8 -*-
# Quantitative Economics Web: http://quant-econ.net/py/index.html

from __future__ import division
import math
from random import shuffle
import numpy as np
import time
np.set_printoptions(threshold=np.nan)


# 1対1のケースのGAアルゴリズム
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
               if host_preference[-1] == False:
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


# 1対1のケースのGAアルゴリズム
def gale_shapley2(applicant_prefers_input, host_prefers_input):

     # NumPy Arrayに変換
     applicant_preferences = np.array(applicant_prefers_input, dtype=int)

     aaa = [sorted(hp) for hp in host_prefers_input]
     host_preferences = np.array(aaa, dtype=int)

     print(host_prefers_input)
     print(aaa)

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
               if host_preference[-1] == False:
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


# 選好表を適当に作る
def random_preference_table(row, col):
     output = []
     li = list(range(col))
     for i in range(row):
          li2 = li[:]
          shuffle(li2)
          output.append(li2)

     return output


if __name__ == '__main__':
     for i in range(1):
          app_table = random_preference_table(10, 10)
          hos_table = random_preference_table(10, 10)
          print("スタート!")
          start = time.time()
          matching = gale_shapley2(app_table, hos_table)
          stop = time.time() - start
          print("ストップ！")
          #print(matching)
          print("実行時間は " + str(stop) + " 秒でした")









