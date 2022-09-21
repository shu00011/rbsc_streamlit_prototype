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

   col0, col1, col2, col3 = st.columns(4)

   with col0:
        st.write("[LISTSIZE]")
        userListsize = math.floor(st.number_input('Insert LISTSIZE'))
        st.info(f'Your LISTSIZE: {userListsize}')

   with col1:
        st.write("[SELECTLIST]")
        userSelectlist = math.floor(st.number_input('Insert SELECTLIST'))
        if userListsize <= userSelectlist:
            st.error("⚠ The subset must be smaller than the universal set.")
        else:
            st.info(f'Your SELECTLIST: {userSelectlist}')

   with col2:
        st.write("[RHO_STAR]")
        userRhostar=st.number_input('Insert RHO_STAR')
        if userRhostar >= -1 and userRhostar <= 1:
            st.info(f'Your RHO_STAR: {userRhostar}')
        else:
            st.error("⚠ The range of RHO_STAR must be between -1 and 1.")

   with col3:
        st.write("[EPS]")
        userEps=st.number_input('Insert EPS')
        st.info(f'Your EPS: {userEps}')

   st.write("Number of bins")
   userNBins=math.floor(st.number_input('Insert number of bins'))
   if userNBins < 1:
        st.error("⚠ Number of bins must be greater than or equal to 1.")
   else:
       st.info(f'Your number of bins: {userNBins}')

   uploaded_file = st.file_uploader('Choose a CSV file',type='csv')
   if uploaded_file is not None:
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        read_data=[float(row) for row in string_data.splitlines()]

   with st.expander('🤔 If you cannot create the expected subset, change Max. number of trials.'):
        st.write('[Max. number of trials]')
        userMaxtrials=math.floor(st.number_input('Insert Max. number of trials', value = 30))
        st.info(f'Your number of bins: {userMaxtrials}')

   if st.button('result'):
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
        st.success('Time elapsed %2.2f sec' % elapsed_time)

   gitLink = '[source code](https://github.com/shu00011/rbsc_streamlit_prototype)'
   st.markdown(gitLink, unsafe_allow_html=True)

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
