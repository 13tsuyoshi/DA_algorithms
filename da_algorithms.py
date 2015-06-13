#!/usr/bin/python
#-*- encoding: utf-8 -*-
# Quantitative Economics Web: http://quant-econ.net/py/index.html

from __future__ import division
import math
import functools  #for python3
from random import uniform, normalvariate
import numpy as np
np.set_printoptions(threshold=np.nan)

# INPUT: 申し込み側の選好、受け入れ側の選好
# OUTPUT: マッチング

def gale_shapley(applicant_preferences, host_preferences):
     row, col = applicant_preferences.shape

     # 未マッチング者のリスト
     stack = list(range(row))

     # {man: woman, man: woman...}というマッチングを入れる
     matching = {}

     print("探索開始\n")

     while len(stack) > 0:
          # スタックから1人応募者を取り出す
          applicant = stack.pop(0)
          # 取り出した応募者の選好表
          applicant_preference = applicant_preferences[applicant]

          print("Man{0} さんの探索開始".format(applicant))

          for index, host in enumerate(applicant_preference):
               print("Man{0} さんの 選好順位{1}番目は Woman{2}さん".format(applicant, index, host))
               host_preference = host_preferences[host]

               # 相手が未マッチングなら
               if host_preference[-1] == 0:
                    print("Woman{0} さんは未マッチング".format(host))
                    print("Man{0} さんとWoman{1} さん仮マッチング".format(applicant, host))
                    host_preference[-1] = 1
                    applicant_preference[-1] = 1
                    matching[applicant] = host
                    break

               # 相手がマッチング済なら
               else:
                    # 既にマッチング済みの相手を代入
                    matched = [k for k, v in matching.items() if v == host][0]
                    print("Woman{0} さんは Man{1} さんとマッチング済".format(host, matched))

                    # 新しい応募者と、既にマッチング済みの相手の、受け入れ側における選好順位を比較
                    rank_matched = np.where(host_preference[:-1] == matched)[0][0]
                    rank_applicant = np.where(host_preference[:-1] == applicant)[0][0]
                    print("Woman{0} さんの選好表におけるMan{1} さんの順位は {2}番, Man{3} さんの順位は {4}番".format(host, applicant, rank_applicant, host, rank_matched))

                    # もし受け入れ側が新しい応募者の方を好むなら
                    if rank_matched > rank_applicant:
                         print("Man{0} さんとWoman{1} さんのマッチング解除".format(matched, host))
                         applicant_preference[-1] = 1
                         del matching[matched]

                         print("Man{0} さんとWoman{1} さん仮マッチング".format(applicant, host))
                         matching[applicant] = host
                         applicant_preferences[matched][-1] = 0
                         stack.append(matched)
                         break

                    print("Man{0} さんとWoman{1} さんはマッチングせず……".format(applicant, host))

          print("Man{0} さんの探索終了\n".format(applicant))

     print("\n全探索終了\nマッチングは")

     print(matching)


def is_stable_matching(matching, applicant_preferences, host_preferences):
     pass



applicant_matrix = np.array(
    [[0, 1, 2, 3, 4, False], 
     [4, 1, 2, 0, 3, False],
     [3, 0, 2, 4, 1, False],
     [4, 2, 0, 1, 3, False],
     [3, 0, 4, 1, 2, False],
    ])


host_matrix = np.array(
    [[0, 1, 2, 3, 4, False], 
     [4, 2, 0, 1, 3, False],
     [3, 0, 4, 1, 2, False],
     [4, 1, 2, 0, 3, False],
     [3, 0, 2, 4, 1, False],
    ])

gale_shapley(applicant_matrix, host_matrix)







