#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Random sampling without replacement: random.sample()

import streamlit as st
import numpy as np
import random
import datetime
import pickle
import time
import plotly.figure_factory as ff
import scipy

MAXITER = 30  # counter　n回まで
EXPERIMENT_NUMBER = 30
NBINS = 10 # 階級数．ヒストグラムの棒の数？

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
def my_snippet(l, s, rho_star, e, counters, rho_accuracy):
    # TODO: 31-36どれが効率がいいか？
    # TODO: なぜこの基準にするのか？
    # TODO: パラメータはどの範囲の条件がいいとかの結果はあるか？→論文を見直す．
    # x = np.random.rand(l)
    # 正規分布に従った乱数の生成
    # normal（平均，標準偏差，出力配列のサイズ）
    # 平均が0で標準偏差が1→標準正規分布
    x = np.random.normal(loc=0, scale=1, size=l)
    # x = np.random.exponential(scale = 1, size = l)
    # x = np.random.uniform(low = 1, high = 5, size = l)
    # x = np.random.vonmises(mu = 0, kappa = np.pi/10, size = l)
    # x = np.random.lognormal(mean = 0.0, sigma = 1.0, size = l)

    xs=np.sort(x) # xを昇順にsort

    """
    全体集合xの中から大きさsのyを取り出して2等分する
    →この繰り返しがcounter
    """
    y = random.sample(list(x), s)
    y1 = y[:int(len(y) * 0.5)]  # AとBそのもの．indexでなくて値そのもの．
    y2 = y[int(len(y) * 0.5):]
    rho = get_rbsc(y1, y2)

    counter = 0

    z = list(set(x) - set(y))  # z=すでに選んだ値をxから除外したもの

    while not (rho_star - e <= rho and rho <= rho_star + e) and (counter < MAXITER):

        if rho < rho_star - e:  # 求めたいpより低い時→y1の集合を高くしたい
            counter1 = 0
            while counter1 < MAXITER:
                counter1 += 1
                w = np.random.choice(z, 1)[0]  # w: 配列=zのなかから1こずつランダムに選ぶ
                """
                wがy1より大きければy1にwを加える→y1の平均値をどんどん高くする
                """
                if (np.mean(y1) < w):  # meanは引数の平均．
                    y1.append(w)
                    z.remove(w)
                    break

            counter2 = 0
            while counter2 < MAXITER:
                counter2 += 1
                w = np.random.choice(y1, 1)[0]  # w = y1から1こずつランダムに選ぶ
                if (np.mean(y1) > w):  # y1のAVGよりもwが小さい→wを抜く
                    y1.remove(w)
                    z.append(w)
                    break

            # counter3-4：y2を低くする
            counter3 = 0
            while counter3 < MAXITER:
                counter3 += 1
                w = np.random.choice(z, 1)[0]
                if (np.mean(y2) > w):
                    y2.append(w)
                    z.remove(w)
                    break

            counter4 = 0
            while counter4 < MAXITER:
                counter4 += 1
                w = np.random.choice(y2, 1)[0]
                if (np.mean(y2) < w):
                    y2.remove(w)
                    z.append(w)
                    break

        if rho > rho_star + e:  # y1を低くしてy2を高くしたい
            counter5 = 0
            while counter5 < MAXITER:
                counter5 += 1
                w = np.random.choice(z, 1)[0]
                if (np.mean(y2) < w):
                    y2.append(w)
                    z.remove(w)
                    break

            counter6 = 0
            while counter6 < MAXITER:
                counter6 += 1
                w = np.random.choice(y2, 1)[0]
                if (np.mean(y2) > w):
                    y2.remove(w)
                    z.append(w)
                    break

            counter7 = 0
            while counter7 < MAXITER:
                counter7 += 1
                w = np.random.choice(z, 1)[0]
                if (np.mean(y1) > w):
                    y1.append(w)
                    z.remove(w)
                    break

            counter8 = 0
            while counter8 < MAXITER:
                counter8 += 1
                w = np.random.choice(y1, 1)[0]
                if (np.mean(y1) < w):
                    y1.remove(w)
                    z.append(w)
                    break

        rho = get_rbsc(y1, y2)
        counter += 1

    counters[l][s][rho_star][e].append(counter)
    rho_accuracy[l][s][rho_star][e].append(np.abs(rho - rho_star))

    return counters, rho_accuracy, y1, y2


def init(userListsize, userSelectlist, userRhostar, userEps):
    """
    ハイパーパラメータ4つ．
    LISTSIZE：数の集合
    SELECTLIST：LISTSIZEから取り出す部分集合の大きさ
    （実行不可能なのはLISTSIZE<SELECTLISTのとき．
    RHO_STAR：RSBC係数p*
        RSBC_SubGenは求めたいpに近づける仕組み．
        RSBC係数p
            総当たり．仮説に反する証拠が多ければpは低くなる．
    EPS：誤差e．大きければアルゴリズムはすぐに収束する．
    """
#     LISTSIZE = np.arange(100, 901, 50)  # [100, 300, 500 ,700, 900]
#     SELECTLIST = np.arange(100, 501, 50)  # [100, 200, 300, 400, 500]
#     RHO_STAR = np.arange(0.3, 0.71, 0.04)  # [0.3, 0.5, 0.7]
#     EPS = np.arange(0.05, 0.16, 0.01)  # [0.05, 0.1, 0.15]

    LISTSIZE = userListsize
    SELECTLIST = userSelectlist
    RHO_STAR = userRhostar
    EPS = userEps

    """
    デフォルト値を設定．
    2つを固定して残り2つを比較する．（2次元で）
    出力は6つになる．
    """

    # 表を表示するためのコード
    counters, rho_accuracy = {}, {}
    counters[LISTSIZE], rho_accuracy[LISTSIZE] = {}, {}
    counters[LISTSIZE][SELECTLIST], rho_accuracy[LISTSIZE][SELECTLIST] = {}, {}
    counters[LISTSIZE][SELECTLIST][RHO_STAR], rho_accuracy[LISTSIZE][SELECTLIST][RHO_STAR] = {}, {}
    counters[LISTSIZE][SELECTLIST][RHO_STAR][EPS], rho_accuracy[LISTSIZE][SELECTLIST][RHO_STAR][EPS] = [], []

    return \
        MAXITER, \
        EXPERIMENT_NUMBER, \
        LISTSIZE, \
        SELECTLIST, \
        RHO_STAR, \
        EPS, \
        counters, \
        rho_accuracy

# 恐らくmain関数．
def rsbc(userListsize, userSelectlist, userRhostar, userEps):
    start_time = time.time()

    NBINS = 20  # 階級数．ヒストグラムの棒の数？

    MAXITER, \
    EXPERIMENT_NUMBER, \
    LISTSIZE, \
    SELECTLIST, \
    RHO_STAR, \
    EPS, \
    counters, \
    rho_accuracy = \
        init(userListsize, userSelectlist, userRhostar, userEps)

    # np.count_nonzero()→引数の条件に合う要素の個数
#     if np.count_nonzero(LISTSIZE) <= np.count_nonzero(SELECTLIST):
#         return

    if LISTSIZE <= SELECTLIST:
        return

    counters, rho_accuracy, A, B= my_snippet( \
        LISTSIZE, \
        SELECTLIST, \
        RHO_STAR, \
        EPS, \
        counters, \
        rho_accuracy)

#     group_labels=['1','2','3','4','5','6','7','8','9','10']

    A_hist, bin_edges = np.histogram(A, bins = NBINS, density=True)
    st.bar_chart(A_hist)

    # PlotlyError: Oops! Your data lists or ndarrays should be the same length.
#     A_hist_list=[]
#     A_hist_list.append(A_hist)
#     figA=ff.create_distplot(A_hist_list, group_labels,bin_size=10)
#     st.plotly_chart(figA, use_container_width=true)

    B_hist, bin_edges = np.histogram(B, bins = NBINS, density=True)
    st.bar_chart(B_hist)
#     figB=ff.create_distplot(B_hist, group_labels,bin_size=10)
#     st.plotly_chart(figB, use_container_width=true)

    st.write('-------------------------')
    st.write('Results:\t niter: {0:0.2f}\t  rho_accuracy: {1:0.2f}\t'.format( \
        np.mean(counters[LISTSIZE][SELECTLIST][RHO_STAR][EPS]), \
        np.mean(rho_accuracy[LISTSIZE][SELECTLIST][RHO_STAR][EPS])))
        # meanは引数の平均
        # 出力結果は反復回数の平均値

    # histogram(ヒストグラムを計算するための入力データ,bins,density)
    # bins 整数，文字列，またはスカラーのシーケンス．ビンの数を表す．ビンは範囲のようなもの．
    # binsが整数の場合は等間隔に配置されたビンの数を表す．
    # densityがtrueのときは重みが正規化される．
    # 戻り値は2つの配列．
    # histはヒストログラムの値．
    #bin_edgesはビンエッジ．bin_edgesのサイズは常に1+histのサイズ．つまりlength(hist)+1
#     A_hist, bin_edges = np.histogram(A, bins = NBINS, density=True)
#     print(A_hist)
#     print(bin_edges)
#     print(bin_edges[:-1])
#
#     B_hist, bin_edges = np.histogram(B, bins = NBINS, density=True)
#     print(B_hist)
#     print(bin_edges)
#     print(bin_edges[:-1])

#     now = datetime.datetime.now()
#     fpath = str(now.year) + '_' + \
#             str(now.month).zfill(2) + '_' + \
#             str(now.day).zfill(2) + '_' + \
#             str(now.hour).zfill(2) + '_' + \
#             str(now.minute).zfill(2) + '_' + \
#             str(now.second).zfill(2) + '_' + \
#             'input_normal_counters_rho_acc_briefs.pkl'
#
#     with open(fpath, 'wb') as handle:
#         pickle.dump([counters, rho_accuracy], \
#                     handle, \
#                     protocol=pickle.HIGHEST_PROTOCOL)

    # Time elapsed 4412.87 sec
    elapsed_time = time.time() - start_time
    st.success('Time elapsed %2.2f sec' % elapsed_time)
