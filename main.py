import streamlit as st
import math
import io
import pandas as pd
import numpy as np
import rbsc_st as rbsc
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

   uploaded_file = st.file_uploader('Choose a file',type='csv')
   if uploaded_file is not None:
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        read_data=[float(row) for row in string_data.split('\r\n')]

   if st.button('result'):
        with st.spinner('running...'):
            elapsed_time = rbsc.rbsc(
                userListsize,
                userSelectlist,
                userRhostar,
                userEps,
                userNBins,
                read_data
            )

        st.success('Done!')
        st.success('Time elapsed %2.2f sec' % elapsed_time)


if __name__ == "__main__":
    main()
