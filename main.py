import streamlit as st
import streamlit_ext as ste
import math
import io
import pandas as pd
import numpy as np
import rbsc_st as rbsc
import csv
import time

def st_print(LISTSIZE, SELECTLIST, A, B, NBINS):

    A_hist, bin_edges = np.histogram(A, bins = NBINS, density=True)
    B_hist, bin_edges = np.histogram(B, bins = NBINS, density=True)

    col0, col1 = st.columns(2)

    with col0:
        st.write('a histogram of distribution of subset A values')
        st.bar_chart(A_hist)

    with col1:
        st.write('a histogram of distribution of subset B values')
        st.bar_chart(B_hist)

    # histogram(ヒストグラムを計算するための入力データ,bins,density)
    # bins 整数，文字列，またはスカラーのシーケンス．ビンの数を表す．ビンは範囲のようなもの．
    # binsが整数の場合は等間隔に配置されたビンの数を表す．
    # densityがtrueのときは重みが正規化される．
    # 戻り値は2つの配列．
    # histはヒストログラムの値．
    # bin_edgesはビンエッジ．bin_edgesのサイズは常に1+histのサイズ．つまりlength(hist)+1

def output_df(dataframe,A,B):
    csvA=dataframe.loc[A.index].reset_index(drop=True).to_csv(index=False)
    csvB=dataframe.loc[B.index].reset_index(drop=True).to_csv(index=False)

    col0, col1 = st.columns(2)

    with col0:
        st.write(dataframe.loc[A.index].reset_index(drop=True))
        ste.download_button(
            'Download data A as CSV',
            csvA,
            'dataA.csv'
        )

    with col1:
        st.write(dataframe.loc[B.index].reset_index(drop=True))
        ste.download_button(
            label="Download data B as CSV",
            data=csvB,
            file_name='dataB.csv',
            mime='text/csv'
        )

def rbscApp():
   st.title('RBSC-SubGen')

   userListsize = 0

   st.subheader('1. Data upload')

   uploaded_file = st.file_uploader('Load a CSV data file',type='csv')
   if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        df_columns = dataframe.columns.values

        st.write(dataframe)

        columns = st.selectbox(
            'Select the columns you wish to apply to RBSC-SubGen.',
            (df_columns)
        )

        read_data = dataframe[columns]
        userListsize = len(read_data)
        st.info(f'Your number of data points: {userListsize}')

   st.subheader('2. Input parameters')

   col0, col1, col2 = st.columns(3)

   with col0:
        st.write("[Subset size]")
        userSelectlist = math.floor(st.number_input('Insert subset size'))
        if userListsize <= userSelectlist:
            st.error("⚠ The subset size must be smaller than the universal set size.")
        else:
            st.info(f'Your Subset size: {userSelectlist}')

   with col1:
        st.write("[RBSC coefficient]")
        userRhostar=st.number_input('Insert RBSC coefficient')
        if userRhostar >= -1 and userRhostar <= 1:
            st.info(f'Your RBSC coefficient: {userRhostar}')
        else:
            st.error("⚠ The range of RBSC coefficient must be between -1 and 1.")

   with col2:
        st.write("[Tolerable error]")
        userEps=st.number_input('Insert tolerable error')
        if userEps < 0:
            st.error("⚠ Tolerable error must be an absolute value.")
        else:
            st.info(f'Your tolerable error: {userEps}')

   with st.expander('🤔 If you cannot create the expected subset, change Max. number of trials.'):
        st.write('[Max. number of trials]')
        userMaxtrials=math.floor(st.number_input('Insert Max. number of trials', value = 30))
        st.info(f'Your number of bins: {userMaxtrials}')

   st.subheader('3. Visualization parameters')

   st.write("[Number of histogram bins]")
   userNBins=math.floor(st.number_input('Insert number of histogram bins'))
   if userNBins < 1:
        st.error("⚠ Number of bins must be greater than or equal to 1.")
   else:
       st.info(f'Your number of bins: {userNBins}')

   if st.button('Run'):
        with st.spinner('running...'):
            start_time = time.time()
            A, B, rho = rbsc.rbsc( \
                userListsize, \
                userSelectlist, \
                userRhostar, \
                userEps, \
                read_data, \
                userMaxtrials)

            st_print(userListsize, userSelectlist, A, B, userNBins)

            output_df(dataframe,A,B)

            elapsed_time = time.time() - start_time

        st.success('Done!')
        st.success(f'Your RBSC corfficient: {rho}')
        st.success('Time elapsed %2.2f sec' % elapsed_time)

   howto = '[How to use?](https://www.notion.so/RBSC-SubGen-26bc7321cd4443e4b9e4f51113519a54)'
   st.markdown(howto, unsafe_allow_html=True)


def main():
    rbscApp()

if __name__ == "__main__":
    main()
