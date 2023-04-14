import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# ページのタイトル設定
st.set_page_config(
    page_title = "titanic",
)

# csv読み込み
df0 = pd.read_csv('test.csv', index_col = 0)

# セッション情報の初期化
if "page_id" not in st.session_state:
    st.session_state.page_id = -1
    st.session_state.df0 = df0

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

    column_list = st.session_state.df0.columns.values
    column_list_selector = st.sidebar.selectbox("内容選択", column_list)
    arr = []

    #top5=st.session_state.df0.sort_values(column_selector, ascending = False)[:5][column_list_selector]

    #fig1, ax1 = plt.subplots(figsize = (6.4, 4.8))

    #ax1.bar(top5.index.values,top5)
    #ax1.set_title(column_list_selector+"店上位5位売り上げ")
    #ax1.set_xlabel("売上年月日")
    #ax1.set_ylabel("総売上")

    kind = list(set(list(st.session_state.df0[column_list_selector])))

    arr.append(list(st.session_state.df0[column_list_selector]).count(kind[0]))
    arr.append(list(st.session_state.df0[column_list_selector]).count(kind[1]))

    fig2, ax2 = plt.subplots(figsize = (9.0, 5.4))

    ax2.pie(arr, labels = kind)
    ax2.set_title(column_list_selector)
    ax2.set_xlabel("")
    ax2.set_ylabel("")

    #st.pyplot(fig1)
    st.pyplot(fig2)
    st.text(set(list(st.session_state.df0[column_list_selector])))

# ページ判定
if st.session_state.page_id == -1:
    main_page()


#x軸とy軸のラベル表示
#上の度数分布表でy軸が整数になるようにする
#上の度数分布表の元データを書き換えて、正規分布のような形のヒストグラムになるようにする
