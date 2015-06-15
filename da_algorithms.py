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
                         #print(applicant, matched, newhost, newhost_matched)
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


# 可能なマッチングを全出力する
def all_matching(size):
     if size > 7:
          print("sizeが大きすぎます")
          return False

     li = list(range(size))


     def __matching_list(li):
          if len(li) == 1:
               return [li]

          output = []
          for index, element in enumerate(li):
               li2 = li[:]
               li2.pop(index)
               m = __matching_list(li2)
               for x in m:
                    output.append([element] + x)

          return output


     def __make_dict(pattern):
          size = len(li)
          outdict = {}
          for i in range(size):
               outdict[i] = pattern[i]
          return outdict

     output = []

     for pattern in __matching_list(li):
          output.append(__make_dict(pattern))

     return output


# 可能な安定マッチングを全出力する
def all_stable_matching(applicant_prefers_input, host_prefers_input):
     # NumPy Arrayに変換
     applicant_preferences = np.array(applicant_prefers_input, dtype=int)
     host_preferences = np.array(host_prefers_input, dtype=int)

     # 選好表の行列数をチェック
     row, col = applicant_preferences.shape
     row_host, col_host = host_preferences.shape
     if row != col_host or col != row_host:
          exit(-1)

     if row > 7 or col > 7:
          print("sizeが大きすぎます")
          return False

     matchings = all_matching(row)

     output = []
     for matching in matchings:
          if is_stable_matching(matching, applicant_preferences, host_preferences):
               output.append(matching)

     return output


# マッチングのスコアを、申し込み側 / 受け入れ側それぞれについて求める
# 一番良い相手とペアになった時のスコアが(相手側の人数)ポイント、一番悪い相手とペアになった時のスコアが0ポイント
def matching_score(matching, applicant_prefers_input, host_prefers_input):
     # NumPy Arrayに変換
     applicant_preferences = np.array(applicant_prefers_input, dtype=int)
     host_preferences = np.array(host_prefers_input, dtype=int)

     # 選好表の行列数をチェック
     row, col = applicant_preferences.shape
     row_host, col_host = host_preferences.shape
     if row != col_host or col != row_host:
          exit(-1)

     applicants_score = 0
     hosts_score = 0

     for applicant, host in matching.items():
          applicant_preference = applicant_preferences[applicant]
          host_preference = host_preferences[host]

          rank_host = np.where(applicant_preference == host)[0][0]
          rank_applicant = np.where(host_preference == applicant)[0][0]

          applicants_score += (col-1) - rank_host
          hosts_score += (row-1) - rank_applicant

     return [applicants_score, hosts_score]


if __name__ == '__main__':

     for i in range(10):
          print("\n+-------------------------------------+\n")
          print("{0}回目".format(i))
          app_table = random_preference_table(5, 5)
          hos_table = random_preference_table(5, 5)
          matching = gale_shapley(app_table, hos_table)
          is_stable = is_stable_matching(matching, app_table, hos_table)
          app_score, hos_score = matching_score(matching, app_table, hos_table)
          all_match = all_stable_matching(app_table, hos_table)
          score_match = []

          for m in all_match:
               score_match.append(matching_score(m, app_table, hos_table))

          print("申し込み側の選好は: {0}".format(app_table))
          print("受け入れ側の選好は: {0}".format(hos_table))
          print("マッチングは: {0}".format(matching))
          print("安定マッチングが得られたか? {0}".format(is_stable))
          print("マッチングのスコアは: 申し込み側 {0}ポイント, 受け入れ側 {1}ポイント".format(app_score, hos_score))

          print("\n全マッチングとスコアは、")
          for i in range(len(score_match)):
               print(all_match[i], ": ", score_match[i])

          print("です。")



     """
     print(matching_score(
          {0: 4, 1: 1, 2: 3, 3: 2, 4: 0},
          [[2, 4, 3, 1, 0], [1, 0, 3, 4, 2], [1, 3, 2, 0, 4], [2, 4, 1, 3, 0], [4, 0, 2, 3, 1]],
          [[0, 2, 1, 3, 4], [1, 4, 3, 0, 2], [4, 3, 2, 0, 1], [4, 2, 1, 0, 3], [1, 0, 3, 4, 2]]
          ))
     """

     """
     print(all_stable_matching(
          [[2, 4, 3, 1, 0], [1, 0, 3, 4, 2], [1, 3, 2, 0, 4], [2, 4, 1, 3, 0], [4, 0, 2, 3, 1]],
          [[0, 2, 1, 3, 4], [1, 4, 3, 0, 2], [4, 3, 2, 0, 1], [4, 2, 1, 0, 3], [1, 0, 3, 4, 2]]
          ))
     """









