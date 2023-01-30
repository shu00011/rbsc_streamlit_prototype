import streamlit as st
import streamlit_ext as ste
import math
import pandas as pd
import numpy as np
import rbsc_st as rbsc
import time


def ht_print(A, B, NBINS, column=None):
    if column is not None:
        st.write(f'[{column}]')

    A_hist, bin_edges = np.histogram(A, bins=NBINS, density=True)
    B_hist, bin_edges = np.histogram(B, bins=NBINS, density=True)

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


def dataframe_loc(dataframe, X):
    return dataframe.loc[X.index].reset_index(drop=True)


def output_df(dataframe, A, B):
    dataframeA = dataframe_loc(dataframe, A)
    dataframeB = dataframe_loc(dataframe, B)

    csvA = dataframeA.to_csv(index=False)
    csvB = dataframeB.to_csv(index=False)

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


def check_userRhostar(userRhostar, name=None):
    if userRhostar >= -1 and userRhostar <= 1:
        if name == None:
            st.info(f'Your RBSC coefficient: {userRhostar}')
        else:
            st.info(f'Your RBSC coefficient of {name}: {userRhostar}')
    else:
        st.error("⚠ The range of RBSC coefficient must be between -1 and 1.")


def rbscApp():
    st.title('RBSC-SubGen')

    url = 'https://www.notion.so/RBSC-SubGen-26bc7321cd4443e4b9e4f51113519a54'

    st.markdown(f'''
    <a href={url}><button style="background-color:white; border-radius: 5px; border: 1px solid; border-color: #d3d3d3; margin: 5px; color:#6495ed;">How to use?</button></a>
    ''',
                unsafe_allow_html=True)

    userListsize = 0
    MAX_SELECT = 2
    MULTI = False

    st.subheader('1. Data upload')

    uploaded_file = st.file_uploader('Load a CSV data file', type='csv')
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file).drop(
            columns='Unnamed: 0', errors='ignore')
        df_columns = dataframe.columns.values

        st.write(dataframe)

        columns = st.multiselect(
            'Select the columns you want to apply to RBSC-SubGen.',
            (df_columns),
            max_selections=MAX_SELECT
        )

        userListsize = len(dataframe)
        st.info(f'Your number of data points: {userListsize}')

        columns_len = len(columns)

        if columns_len == MAX_SELECT-1 or columns_len == MAX_SELECT:
            read_data = dataframe[columns[0]]
            if columns_len == MAX_SELECT:
                MULTI = True

    st.subheader('2. Input parameters')

    col0, col1, col2 = st.columns(3)

    with col0:
        st.write("[Subset size]")
        userSelectlist = math.floor(st.number_input('Insert subset size'))

        if MULTI and userListsize <= userSelectlist*8:
            st.error(
                "⚠ The subset size must be less than one-eighth of the universal set size.")
        elif userListsize <= userSelectlist:
            st.error(
                "⚠ The subset size must be smaller than the universal set size.")
        else:
            st.info(f'Your Subset size: {userSelectlist}')

    with col1:
        st.write("[RBSC coefficient]")

        if MULTI is not True:
            userRhostar = st.number_input('Insert RBSC coefficient')
            check_userRhostar(userRhostar)
        else:
            userRhostarA = st.number_input(
                f'Insert RBSC coefficient of: {columns[0]}')
            check_userRhostar(userRhostarA, columns[0])
            userRhostarB = st.number_input(
                f'Insert RBSC coefficient of: {columns[1]}')
            check_userRhostar(userRhostarB, columns[1])

    with col2:
        st.write("[Tolerable error]")
        userEps = st.number_input('Insert tolerable error')
        if userEps < 0:
            st.error("⚠ Tolerable error must be an absolute value.")
        else:
            st.info(f'Your tolerable error: {userEps}')

    with st.expander('🤔 If you cannot create the expected subset, change Max. number of trials.'):
        st.write('[Max. number of trials]')
        userMaxtrials = math.floor(st.number_input(
            'Insert Max. number of trials', value=30))
        st.info(f'Your number of Max. number of trials: {userMaxtrials}')

    st.subheader('3. Visualization parameters')

    st.write("[Number of histogram bins]")
    userNBins = math.floor(st.number_input('Insert number of histogram bins'))
    if userNBins < 1:
        st.error("⚠ Number of bins must be greater than or equal to 1.")
    else:
        st.info(f'Your number of bins: {userNBins}')

    if st.button('Run'):
        with st.spinner('running...'):
            start_time = time.time()

            if MULTI is not True:
                A1, B2, rho = rbsc.rbsc(
                    userListsize,
                    userSelectlist,
                    userRhostar,
                    userEps,
                    read_data,
                    userMaxtrials)
            else:
                A, B, rho = rbsc.rbsc(
                    userListsize,
                    userSelectlist*4,
                    userRhostarA,
                    userEps,
                    read_data,
                    userMaxtrials)

                dataframeA = dataframe_loc(dataframe, A)
                dataframeB = dataframe_loc(dataframe, B)

                read_dataA = dataframeA[columns[1]]

                A1, A2, rho1 = rbsc.rbsc(
                    len(dataframeA),
                    userSelectlist,
                    userRhostarB,
                    userEps,
                    read_dataA,
                    userMaxtrials)

                read_dataB = dataframeB[columns[1]]

                B1, B2, rho2 = rbsc.rbsc(
                    len(dataframeB),
                    userSelectlist,
                    userRhostarB,
                    userEps,
                    read_dataB,
                    userMaxtrials)

                dataframeA1 = dataframe_loc(dataframeA, A1)
                dataframeB2 = dataframe_loc(dataframeB, B2)

            if MULTI is not True:
                ht_print(A1, B2, userNBins)
            else:
                ht_print(dataframeA1[columns[0]],
                         dataframeB2[columns[0]], userNBins, columns[0])
                ht_print(A1, B2, userNBins, columns[1])

            output_df(dataframe, A1, B2)

            elapsed_time = time.time() - start_time

        st.success('Done!')
        if MULTI is not True:
            st.success(f'Your RBSC corfficient: {rho}')
        else:
            st.success(f'Yout RBSC corfficient of {columns[0]}: {rho}')
            st.success(
                f'Yout RBSC corfficient of {columns[1]}: {rho1} and {rho2}')

        st.success('Time elapsed %2.2f sec' % elapsed_time)


def main():
    rbscApp()


if __name__ == "__main__":
    main()
