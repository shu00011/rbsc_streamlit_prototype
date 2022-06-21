import streamlit as st
import math
import io
import pandas as pd
import numpy as np
import rsbc_st as rsbc
import csv

def open_csv_numpy_loadtxt(filename):
   data=np.loadtxt(filename, delimiter="\n")
   return data

def main():
   col0, col1, col2, col3 = st.columns(4)

   with col0:
        st.write("[LISTSIZE]")
        userListsize=math.floor(st.number_input('Insert LISTSIZE'))
        st.info(f'Your LISTSIZE: {userListsize}')

   with col1:
        st.write("[SELECTLIST]")
        userSelectlist=math.floor(st.number_input('Insert SELECTLIST'))
        st.info(f'Your SELECTLIST: {userSelectlist}')

   with col2:
        st.write("[RHO_STAR]")
        userRhostar=st.number_input('Insert RHO_STAR')
        st.info(f'Your RHO_STAR: {userRhostar}')

   with col3:
        st.write("[EPS]")
        userEps=st.number_input('Insert EPS')
        st.info(f'Your EPS: {userEps}')

   st.write("Number of bins")
   userNBins=math.floor(st.number_input('Insert number of bins'))
   st.info(f'Your number of bins: {userNBins}')

# https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader
   uploaded_file = st.file_uploader('Choose a file')
   if uploaded_file is not None:
#         # To read file as bytes:
#         bytes_data = uploaded_file.getvalue()
#         st.write(bytes_data)

        # To convert to a string based IO:
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
#         st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)

        # ----ここから　作業中．うまく動かない．
        # TODO: floatでimportできるように．
        csv_reader=csv.reader(stringio)#delimiter='\n'

        # TODO: 下2行のコメントアウト外すとなぜか画面がレンダリングされない
#         for row in csv_reader:
#             yield[float(i) for i in row]
        read_data=[float(row) for row in csv_reader]
        st.write(read_data)

        # TODO: stringをnumpyのarrayに変換
#         stringArray=np.array([string_data])
#         floatArray=stringArray.np.astype(float)
#         csv_data=open_csv_numpy_loadtxt(floatArray)
#         st.write(csv_data)

        # ---- ここまで

#         # Can be used wherever a "file-like" object is accepted:
#         dataframe = pd.read_csv(uploaded_file)
#         st.write(dataframe)

   if st.button('result'):
        with st.spinner('running...'):
            rsbc.rsbc(
                userListsize,
                userSelectlist,
                userRhostar,
                userEps,
                userNBins
            )

        st.success('Done!')

if __name__ == "__main__":
    main()
