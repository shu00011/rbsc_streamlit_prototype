import streamlit as st
import math
import rsbc_st as rsbc


def main():
    sliderStart = 0.0
    sliderEnd = 0.0
    mode = 'int'

    hyP = st.radio(
        "Choose a hyperparameter",
        ('LISTSIZE', 'SELECTLIST', 'RHO_STAR', 'EPS')
    )

    st.info(f'The hyperparameter of your choise: {hyP}')

    # LISTSIZE 500-1500-50で動いた

    if hyP == 'LISTSIZE':
        sliderStart = 100.0
        sliderEnd = 5000.0
    elif hyP == 'SELECTLIST':
        sliderStart = 100.0
        sliderEnd = 1000.0
    elif hyP == 'RHO_STAR':
        sliderStart = -1.0
        sliderEnd = 1.0
        mode = 'decimal'
    else:
        sliderStart = 0.00
        sliderEnd = 0.20
        mode = 'decimal'

    rangeStart = st.number_input("Select range of start", sliderStart, sliderEnd)
    rangeEnd = st.number_input("Select range of end", rangeStart + 0.01, sliderEnd)
    rangeInterval = st.number_input("sekect range of interval", 0.01, sliderEnd / 2.0)

    if mode == 'int':
        rangeStart = math.floor(rangeStart)
        rangeEnd = math.floor(rangeEnd)
        rangeInterval = math.ceil(rangeInterval)

    st.info(f'range of start: {rangeStart}')
    st.info(f'range of end: {rangeEnd}')
    st.info(f'range of interval: {rangeInterval}')

    if st.button('result'):
        with st.spinner('running...'):
            rsbc.rsbc(hyP, rangeStart, rangeEnd, rangeInterval)
        st.success('Done!')


if __name__ == "__main__":
    main()
