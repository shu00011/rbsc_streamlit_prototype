import streamlit as st
import math
import io
import pandas as pd
import numpy as np
import rbsc_st as rbsc
import csv
import time
import plotly.figure_factory as ff

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
    #bin_edgesはビンエッジ．bin_edgesのサイズは常に1+histのサイズ．つまりlength(hist)+1

def output_csv(A, B):

    csv=pd.DataFrame(zip(A,B),columns=['elements of the subset A',' elements of the subset B']).to_csv()

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='output.csv',
        mime='text/csv'
    )

def rbscApp():
   st.title('RBSC-SubGen')

   userListsize = 0

   st.subheader('1. Data upload')

   uploaded_file = st.file_uploader('Load a CSV data file',type='csv')
   if uploaded_file is not None:
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        read_data = [float(row) for row in string_data.splitlines()]
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
            A, B = rbsc.rbsc(
                userListsize,
                userSelectlist,
                userRhostar,
                userEps,
                read_data,
                userMaxtrials
            )

            st_print(userListsize, userSelectlist, A, B, userNBins)

            output_csv(A, B)
            elapsed_time = time.time() - start_time

        st.success('Done!')
        st.success(f'Your RBSC corfficient: {userRhostar}')
        st.success('Time elapsed %2.2f sec' % elapsed_time)

   gitLink = '[source code](https://github.com/shu00011/rbsc_streamlit_prototype)'
   st.markdown(gitLink, unsafe_allow_html=True)

   with st.expander('❔ Where to save and delete your CSV data file and output.csv?'):
        st.subheader('1. Your CSV data')
        st.markdown('''
            When you upload a CSV data file, the data are copied to the Streamlit backend via the browser, and contained in a BytesIO buffer in Python memory(i.e. RAM, not disk).
            The data will persist in RAM until the Streamlit app re-runs from top-to-bottom, which is on each widget interaction.

            As files are stored in memory, they get deleted immediately as soon as they're not needed anyone.

            This means the app removes a file from memory when:

            - The user uploads another file, replacing the original one.
            - The user clears the file uoloader.
            - The user closes the browser tab ehwn they uploaded the file.
        ''')
        fileUpload= '[Where does st.file_uploader store uploaded files and when do they get deleted?](https://docs.streamlit.io/knowledge-base/using-streamlit/where-file-uploader-store-when-deleted)'
        st.markdown(fileUpload, unsafe_allow_html=True)

        st.subheader('2. output.csv')
        st.markdown('''
            output.csv is stored in-memory while the user is connected, so it's a good idea to keep file sizes under a couple hundred megabytes to conserve memory.
        ''')
        downloadButton = '[st.download_button](https://docs.streamlit.io/library/api-reference/widgets/st.download_button)'
        st.markdown(downloadButton, unsafe_allow_html=True)

def howTo():
    st.write('how to use?')

def main():
    pagelist = ['RBSC-SubGen', 'How to use?']
    selector = st.sidebar.selectbox('Page Selection', pagelist)
    if selector == 'RBSC-SubGen':
        rbscApp()
    elif selector == 'How to use?':
        howTo()

if __name__ == "__main__":
    main()
