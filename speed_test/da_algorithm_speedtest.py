# !/usr/bin/python
# -*- encoding: utf-8 -*-
# Quantitative Economics Web: http://quant-econ.net/py/index.html

from __future__ import division
import math
import functools  #for python3
from random import uniform, normalvariate, shuffle
import numpy as np
import time
np.set_printoptions(threshold=np.nan)


class CustomConditionError(Exception):
    def __init__(self, message):
        self.message = message


def gale_shapley(applicant_prefers_input, host_prefers_input, **kwargs):
    unmatch = kwargs.get('unmatch', True)

    # 選好表の型チェック。listならnumpyへ変換
    applicant_preferences = np.asarray(applicant_prefers_input, dtype=int)
    host_preferences = np.asarray(host_prefers_input, dtype=int)

    # 選好表の行列数をチェック
    app_row, app_col = applicant_preferences.shape
    host_row, host_col = host_preferences.shape

    # unmatchマークが入力されていない時は、選好表の列の最後にunmatch列をつくる
    if not unmatch:
        dummy_host = np.repeat(app_col+1, app_row)
        dummy_applicant = np.repeat(host_col+1, host_row)
        applicant_preferences = np.c_[applicant_preferences, dummy_host]
        host_preferences = np.c_[host_preferences, dummy_applicant]
        app_col += 1
        host_col += 1


    if (app_row != host_col-1) or (host_row != app_col-1):
        raise CustomConditionError("選好表の行列数が不正です")

    applicant_unmatched_mark = app_col - 1
    host_unmatched_mark = host_col - 1

    # ソート
    host_preferences = np.argsort(host_preferences, axis=-1)

    # 未マッチング者のリスト
    stack = list(range(app_row))

    # マッチングを入れる（初期値は未マッチングflag）
    applicant_matchings = np.repeat(applicant_unmatched_mark, app_row)
    host_matchings = np.repeat(host_unmatched_mark, host_row)


    # メインループ
    next_start = np.zeros(app_row, dtype=int)
    while len(stack) > 0:
        # スタックから1人応募者を取り出す
        applicant = stack.pop()

        # 取り出した応募者の選好表
        applicant_preference = applicant_preferences[applicant]

        # 選好表の上から順番にプロポーズ
        for index, host in enumerate(applicant_preference[next_start[applicant]:]):
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
    #app_table = [[3, 1, 4, 0, 2], [3, 2, 4, 0, 1]]
    #hos_table = [[0, 2, 1], [2, 0, 1], [0, 1, 2], [0, 1, 2]]
    #app_table = [[0, 2, 1, 3], [2, 1, 3, 0], [3, 1, 0, 2]]
    #hos_table = [[3, 0, 2, 1], [2, 0, 1, 3], [2, 0, 3, 1]]

    start = time.time()
    app_table = pseudo_random_preference_table(1000, 1000)
    hos_table = random_preference_table(1000, 1000)
    stop = time.time() - start
    print("選好表生成は " + str(stop) + " 秒でした\n")


    print("DAアルゴリズム スタート!")
    start = time.time()
    matching = gale_shapley(app_table, hos_table)
    stop = time.time() - start
    print("ストップ！")
    print("実行時間は " + str(stop) + " 秒でした\n")

    #print(matching[0], "\n")
    #print(matching[1])


















