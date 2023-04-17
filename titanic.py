import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

# ページのタイトル設定
st.set_page_config(
    page_title = "titanic",
)

# csv読み込み
df0 = pd.read_csv('test.csv', index_col = 0)
df1 = pd.read_csv('gender_submission.csv', index_col = 0)

df_merged = pd.merge(df0, df1, on='PassengerId')

# セッション情報の初期化
if "page_id" not in st.session_state:
    st.session_state.page_id = -1
    st.session_state.df0 = df_merged

# 各種メニューの非表示設定
hide_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html = True)

# 最初のページ
def main_page():
    st.markdown(
        "<h2 style='text-align: center;'>タイタニック表示</h2>",
        unsafe_allow_html = True,
    )

    chart_selector = st.sidebar.selectbox("グラフ選択",["bar","hist","pie"])
    column_list_selector = st.sidebar.selectbox("内容選択", st.session_state.df0.columns.values)
    survive_selector = st.sidebar.multiselect('生存者',('0(死亡)', '1(生存)'))


    column_arr = st.session_state.df0[column_list_selector]
    column_arr0 = st.session_state.df0[st.session_state.df0["Survived"] == 0][column_list_selector]
    column_arr1 = st.session_state.df0[st.session_state.df0["Survived"] == 1][column_list_selector]
    kind = list(set(column_arr.dropna(how='all')))

    count_arr = []
    count_arr0 = []
    count_arr1 = []
    for i in range(len(kind)):
        count_arr.append(list(column_arr).count(kind[i]))
        count_arr0.append(list(column_arr0).count(kind[i]))
        count_arr1.append(list(column_arr1).count(kind[i]))

    if chart_selector == "bar":
        #fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        #fig3, ax3 = plt.subplots()

        ax2.bar(kind, count_arr, align="edge", width=0.2)
        #ax1.set_title(column_list_selector)

        ax2.bar(kind, count_arr0, align="center", width=0.2)
        #ax2.set_title(column_list_selector)

        ax2.bar(kind, count_arr1, align="edge", width=-0.2)
        ax2.set_title(column_list_selector)

        #st.pyplot(fig1)
        st.pyplot(fig2)
        #st.pyplot(fig3)

    if chart_selector == "hist":
        bin = st.sidebar.slider('binの数を決めてください', 2, len(kind), len(kind))

        Y, X, _ = plt.hist(column_arr, bins = bin)
        y_max = int(max(Y)) + 1

        fig2, ax2 = plt.subplots()

        ax2.hist(list(column_arr), bins = bin, ec = 'navy')
        #ax2.set_title("標準正規分布"+str(st.session_state.df0.shape[1])+"個データ")
        ax2.set_xlabel(column_list_selector)
        ax2.set_ylabel("度数")
        ax2.set_yticks(np.arange(0,y_max,int(y_max/10)))

        st.pyplot(fig2)

    if chart_selector == "pie":
        fig3, ax3 = plt.subplots()

        ax3.pie(count_arr, startangle=90, labels = kind, autopct="%1.1f%%", labeldistance=0.7, pctdistance=0.5)
        ax3.set_title(column_list_selector)

        st.pyplot(fig3)

    #st.text(st.session_state.df0[st.session_state.df0["Survived"] == 0])

# ページ判定
if st.session_state.page_id == -1:
    main_page()


#x軸とy軸のラベル表示
#上の度数分布表でy軸が整数になるようにする
#上の度数分布表の元データを書き換えて、正規分布のような形のヒストグラムになるようにする
