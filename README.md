# rbsc_streamlit_prototype

## 概要
RBSCアルゴリズムをWebアプリケーション上で利用できるようにしました．

## 使用技術
- Python 3.9.5
- streamlit 1.10.0

## 入力
- ユーザーが指定したLISTSIZE
- ユーザーが指定したSELECTLIST
- ユーザーが指定したRHO_STAR
- ユーザーが指定したEPS
- ユーザーが指定したNumber of bins
- ユーザーからの1行のCSVデータ（全体集合）

## 出力
- 部分集合Aの分布のグラフ
- 部分集合Bの分布のグラフ
- A, Bの値のCSVデータ
- 処理にかかった時間

## demo

![0](https://user-images.githubusercontent.com/68161620/175230781-cdc007be-50ce-43c8-90e5-a02ba526d360.PNG)
![1](https://user-images.githubusercontent.com/68161620/175230791-7ab88802-621b-48af-b8a6-74f78fb95614.PNG)
![2](https://user-images.githubusercontent.com/68161620/175230794-3b9cc42d-a163-4172-91e1-341a7fd6d907.PNG)

## 今後
構成を変えます．

現在はstreamlit+Pythonで全てPythonで実装していますが，

- フロントエンド：Next
- データベース：firebase
- バックエンド（処理）：Python

で実装していきます．

まずはこのプロトタイプを元にPythonのプログラムを作っていきます．
