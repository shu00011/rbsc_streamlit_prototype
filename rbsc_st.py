#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Random sampling without replacement: random.sample()

import numpy as np
import random
import datetime
import pickle
import time
import plotly.figure_factory as ff
import scipy
import pandas as pd

# MAXITER: counter　n回まで
# NBINS: 階級数．ヒストグラムの棒の数？

def get_rbsc(score1, score2):  # score1が高いとrhoが高くなると仮説を立てている
    favor, unfavor = 0, 0
    for d1 in score1:
        for d2 in score2:
            if (d1) > (d2):
                favor += 1
            else:
                unfavor += 1
            rbsc = (favor - unfavor) / (favor + unfavor)
    return rbsc


# 標準偏差
def my_snippet(l, s, rho_star, e, elements, MAXITER):

    """
    全体集合xの中から大きさsのyを取り出して2等分する
    →この繰り返しがcounter
    """
    y = elements.sample(n=s)
    y_index = y.index
    y1 = y[:int(len(y) * 0.5)]  # AとBそのもの．indexでなくて値そのもの．
    y2 = y[int(len(y) * 0.5):]
    rho = get_rbsc(y1, y2)

    counter = 0

    z = elements.drop(y_index)

    # z=すでに選んだ値をelementsから除外したもの
    while not (rho_star - e <= rho and rho <= rho_star + e) and (counter < MAXITER):

        if rho < rho_star - e:  # 求めたいpより低い時→y1の集合を高くしたい
            counter1 = 0
            while counter1 < MAXITER:
                counter1 += 1
                w = z.sample() # w: 配列=zのなかから1こずつランダムに選ぶ
                """
                wがy1より大きければy1にwを加える→y1の平均値をどんどん高くする
                """
                wf=w.iloc[-1]
                w_index=w.index
                if (np.mean(y1) < wf):  # meanは引数の平均．
                    y1 = pd.concat([y1, w])
                    z = z.drop(w_index)
                    break

            counter2 = 0
            while counter2 < MAXITER:
                counter2 += 1
                w = y1.sample()  # w = y1から1こずつランダムに選ぶ
                wf=w.iloc[-1]
                w_index=w.index
                if (np.mean(y1) > wf):  # y1のAVGよりもwが小さい→wを抜く
                    y1 = y1.drop(w_index)
                    z = pd.concat([z, w])
                    break

            # counter3-4：y2を低くする
            counter3 = 0
            while counter3 < MAXITER:
                counter3 += 1
                w = z.sample()
                wf=w.iloc[-1]
                w_index=w.index
                if (np.mean(y2) > wf):
                    y2 = pd.concat([y2, w])
                    z=z.drop(w_index)
                    break

            counter4 = 0
            while counter4 < MAXITER:
                counter4 += 1
                w = y2.sample()
                wf=w.iloc[-1]
                w_index=w.index
                if (np.mean(y2) < wf):
                    y2=y2.drop(w_index)
                    z = pd.concat([z, w])
                    break

        if rho > rho_star + e:  # y1を低くしてy2を高くしたい
            counter5 = 0
            while counter5 < MAXITER:
                counter5 += 1
                w = z.sample()
                wf=w.iloc[-1]
                w_index=w.index
                if (np.mean(y2) < wf):
                    y2 = pd.concat([y2, w])
                    z=z.drop(w_index)
                    break

            counter6 = 0
            while counter6 < MAXITER:
                counter6 += 1
                w = y2.sample()
                wf=w.iloc[-1]
                w_index=w.index
                if (np.mean(y2) > w):
                    y2=y2.drop(w_index)
                    z = pd.concat([z, w])
                    break

            counter7 = 0
            while counter7 < MAXITER:
                counter7 += 1
                w = z.sample()
                wf=w.iloc[-1]
                w_index=w.index
                if (np.mean(y1) > wf):
                    y1 = pd.concat([y1, w])
                    z=z.drop(w_index)
                    break

            counter8 = 0
            while counter8 < MAXITER:
                counter8 += 1
                w = y1.sample()
                wf=w.iloc[-1]
                w_index=w.index
                if (np.mean(y1) < wf):
                    y1=y1.drop(w_index)
                    z = pd.concat([z, w])
                    break

        rho = get_rbsc(y1, y2)
        counter += 1

    return y1, y2, rho

    """
    ハイパーパラメータ4つ．
    LISTSIZE：数の集合
    SELECTLIST：LISTSIZEから取り出す部分集合の大きさ
    （実行不可能なのはLISTSIZE<SELECTLISTのとき．
    RHO_STAR：RBSC係数p*
        RBSC_SubGenは求めたいpに近づける仕組み．
        RBSC係数p
            総当たり．仮説に反する証拠が多ければpは低くなる．
    EPS：誤差e．大きければアルゴリズムはすぐに収束する．
    """

def rbsc(LISTSIZE, SELECTLIST, RHO_STAR, EPS, elements, MAXITER):

    # NBINS:階級数．ヒストグラムの棒の数？

    if LISTSIZE <= SELECTLIST:
        return

    A, B, rho = my_snippet( \
        LISTSIZE, \
        SELECTLIST, \
        RHO_STAR, \
        EPS, \
        elements, \
        MAXITER)

    return A, B, rho

