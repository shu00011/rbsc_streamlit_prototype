import streamlit as st
import math
import rsbc_st as rsbc


def main():
    sliderStart = 0.0
    sliderEnd = 0.0
    isInt = True

    st.write("[LISTSIZE]")
    sliderStart=100.0
    sliderEnd=5000.0
    rangeStartL = st.number_input("Select range of start", sliderStart, sliderEnd)
    rangeEndL = st.number_input("Select range of end", rangeStartL + 0.01, sliderEnd)
    rangeIntervalL = st.number_input("Select range of interval", 0.01, sliderEnd / 2.0)
    rangeStartL = math.floor(rangeStartL)
    rangeEndL = math.floor(rangeEndL)
    rangeIntervalL = math.ceil(rangeIntervalL)

    st.info(f'range of start: {rangeStartL}')
    st.info(f'range of end: {rangeEndL}')
    st.info(f'range of interval: {rangeIntervalL}')


    st.write("[SELECTLIST]")
    sliderStart=100.0
    sliderEnd=1000.0
    rangeStartS = st.number_input("Select range of start", sliderStart, sliderEnd)
    rangeEndS = st.number_input("Select range of end", rangeStartS + 0.01, sliderEnd)
    rangeIntervalS = st.number_input("Select range of interval", 0.01, sliderEnd / 2.0)
    rangeStartS = math.floor(rangeStartS)
    rangeEndS = math.floor(rangeEndS)
    rangeIntervalS = math.ceil(rangeIntervalS)

    st.info(f'range of start: {rangeStartS}')
    st.info(f'range of end: {rangeEndS}')
    st.info(f'range of interval: {rangeIntervalS}')


    st.write("[RHO_STAR]")
    sliderStart=-1.0
    sliderEnd=1.0
    rangeStartR = st.number_input("Select range of start", sliderStart, sliderEnd)
    rangeEndR = st.number_input("Select range of end", rangeStartR + 0.01, sliderEnd)
    rangeIntervalR = st.number_input("Select range of interval", 0.01, sliderEnd / 2.0)

    st.info(f'range of start: {rangeStartR}')
    st.info(f'range of end: {rangeEndR}')
    st.info(f'range of interval: {rangeIntervalR}')


    st.write("[EPS]")
    sliderStart=0.00
    sliderEnd=0.20
    rangeStartE = st.number_input("Select range of start", sliderStart, sliderEnd)
    rangeEndE = st.number_input("Select range of end", rangeStartE + 0.01, sliderEnd)
    rangeIntervalE = st.number_input("Select range of interval", 0.01, sliderEnd / 2.0)

    st.info(f'range of start: {rangeStartE}')
    st.info(f'range of end: {rangeEndE}')
    st.info(f'range of interval: {rangeIntervalE}')

#     hyP = st.radio(
#         "Choose a hyperparameter",
#         ('LISTSIZE', 'SELECTLIST', 'RHO_STAR', 'EPS')
#     )
#
#     st.info(f'The hyperparameter of your choise: {hyP}')
#
#     # LISTSIZE 500-1500-50で動いた
#
#     if hyP == 'LISTSIZE':
#         sliderStart = 100.0
#         sliderEnd = 5000.0
#     elif hyP == 'SELECTLIST':
#         sliderStart = 100.0
#         sliderEnd = 1000.0
#     elif hyP == 'RHO_STAR':
#         sliderStart = -1.0
#         sliderEnd = 1.0
#         isInt = False
#     else:
#         sliderStart = 0.00
#         sliderEnd = 0.20
#         isInt = False
#
#     rangeStart = st.number_input("Select range of start", sliderStart, sliderEnd)
#     rangeEnd = st.number_input("Select range of end", rangeStart + 0.01, sliderEnd)
#     rangeInterval = st.number_input("sekect range of interval", 0.01, sliderEnd / 2.0)
#
#     if isInt:
#         rangeStart = math.floor(rangeStart)
#         rangeEnd = math.floor(rangeEnd)
#         rangeInterval = math.ceil(rangeInterval)
#
#     st.info(f'range of start: {rangeStart}')
#     st.info(f'range of end: {rangeEnd}')
#     st.info(f'range of interval: {rangeInterval}')

    if st.button('result'):
        with st.spinner('running...'):
            rsbc.rsbc(
                rangeStartL,
                rangeEndL,
                rangeIntervalL,
                rangeStartS,
                rangeEndS,
                rangeIntervalS,
                rangeStartR,
                rangeEndR,
                rangeIntervalR,
                rangeStartE,
                rangeEndE,
                rangeIntervalE
            )
#             rsbc.rsbc(hyP, rangeStart, rangeEnd, rangeInterval)
        st.success('Done!')


if __name__ == "__main__":
    main()
