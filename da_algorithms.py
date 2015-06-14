#!/usr/bin/python
#-*- encoding: utf-8 -*-
# Quantitative Economics Web: http://quant-econ.net/py/index.html

from __future__ import division
import math
import functools  #for python3
from random import uniform, normalvariate, shuffle
import numpy as np
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
          applicant = stack.pop(0)

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


# Stable Matchingになっているかを調べる
def is_stable_matching(matching, applicant_prefers_input, host_prefers_input):

     # NumPy Arrayに変換
     applicant_preferences = np.array(applicant_prefers_input, dtype=int)
     host_preferences = np.array(host_prefers_input, dtype=int)

     # 選好表の行列数をチェック
     row, col = applicant_preferences.shape
     row_host, col_host = host_preferences.shape
     if row != col_host or col != row_host:
          exit(-1)

     for applicant in range(row):
          # applicantの選好表
          applicant_preference = applicant_preferences[applicant]

          # applicantの現在のマッチング相手を代入。いなければ-1
          matched = matching.get(applicant, -1)

          # applicantが未マッチングならapplicantの選好表の全ての人に対して
          # マッチング済みなら現在のマッチング相手よりもランクが高い人に対して
          # 駆け落ちできないかを提案する
          if matched >= 0:
               rank_matched = np.where(applicant_preference == matched)[0][0]
          else:
               rank_matched = -1

          for newhost in applicant_preference[:rank_matched]:
               newhost_preference = host_preferences[newhost]
               newhost_matched_list = [k for k, v in matching.items() if v == newhost]

               # 新しいhostが未マッチングなら、applicantはこの人とマッチングした方が良いので、入力はstable matchingでない
               if len(newhost_matched_list) == 0:
                    return False

               # 新しいhostがマッチング済みなら、その人の現在のマッチング相手の順位と自分の順位を比べて、
               # 自分のほうが高ければ、駆け落ちするのが良いので、入力はstable matchingではない
               else:
                    newhost_matched = newhost_matched_list[0]

                    rank_applicant = np.where(newhost_preference == applicant)[0][0]
                    rank_newhost_matched = np.where(newhost_preference == newhost_matched)[0][0]

                    if rank_applicant < rank_newhost_matched:
                         print(applicant, matched, newhost, newhost_matched)
                         return False 

     return True


# 選好表を適当に作る
def random_preference_table(row, col):
     output = []
     li = list(range(col))
     for i in range(row):
          li2 = li[:]
          shuffle(li2)
          output.append(li2)

     return output



for i in range(100):
     print("\n+-------------------------------------+\n")
     print("{0}回目".format(i))
     app_table = random_preference_table(5, 5)
     hos_table = random_preference_table(5, 5)
     matching = gale_shapley(app_table, hos_table)
     is_stable = is_stable_matching(matching, app_table, hos_table)

     print("申し込み側の選好は: {0}".format(app_table))
     print("受け入れ側の選好は: {0}".format(hos_table))
     print("マッチングは: {0}".format(matching))
     print("安定マッチングが得られたか? {0}".format(is_stable))







