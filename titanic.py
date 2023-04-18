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
df0 = pd.read_csv('train.csv', index_col = 0)
#df1 = pd.read_csv('gender_submission.csv', index_col = 0)

#df_merged = pd.merge(df0, df1, on='PassengerId')

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
    column_list = column_list[column_list != 'Survived']
    column_list = column_list[column_list != 'Name']

    chart_selector = st.sidebar.selectbox("グラフ選択",["bar","hist","pie"])
    column_list_selector = st.sidebar.selectbox("内容選択", column_list)
    survive_selector = st.sidebar.multiselect('生存者',(0, 1), default = [0, 1])
    sex_selector = st.sidebar.multiselect('Sex', list(set(st.session_state.df0["Sex"].dropna(how='all'))), default = list(set(st.session_state.df0["Sex"].dropna(how='all'))))
    #age_selector = st.sidebar.multiselect('Age', list(set(st.session_state.df0["Age"].dropna(how='all'))), default = list(set(st.session_state.df0["Age"].dropna(how='all'))))
    sibsp_selector = st.sidebar.multiselect('SibSp', list(set(st.session_state.df0["SibSp"].dropna(how='all'))), default = list(set(st.session_state.df0["SibSp"].dropna(how='all'))))
    parch_selector = st.sidebar.multiselect('Parch', list(set(st.session_state.df0["Parch"].dropna(how='all'))), default = list(set(st.session_state.df0["Parch"].dropna(how='all'))))
    #ticket_selector = st.sidebar.multiselect('Ticket', list(set(st.session_state.df0["Ticket"].dropna(how='all'))), default = list(set(st.session_state.df0["Ticket"].dropna(how='all'))))
    #fare_selector = st.sidebar.multiselect('Fare', list(set(st.session_state.df0["Fare"].dropna(how='all'))), default = list(set(st.session_state.df0["Fare"].dropna(how='all'))))
    #cabin_selector = st.sidebar.multiselect('Cabin', list(set(st.session_state.df0["Cabin"].dropna(how='all'))), default = list(set(st.session_state.df0["Cabin"].dropna(how='all'))))
    embarked_selector = st.sidebar.multiselect('Embarked', list(set(st.session_state.df0["Embarked"].dropna(how='all'))), default = list(set(st.session_state.df0["Embarked"].dropna(how='all'))))

    column_arr = st.session_state.df0[column_list_selector]
    kind = list(set(column_arr.dropna(how='all')))

    select_arr = st.session_state.df0[
                                        (
                                        st.session_state.df0["Survived"].isin(survive_selector)
                                        & st.session_state.df0["Sex"].isin(sex_selector)
                                        #& st.session_state.df0["Age"].isin(age_selector)
                                        & st.session_state.df0["SibSp"].isin(sibsp_selector)
                                        & st.session_state.df0["Parch"].isin(parch_selector)
                                        & st.session_state.df0["Embarked"].isin(embarked_selector)
                                        )
                                    ][column_list_selector]
    count_arr = []
    count_select =[]

    for i in range(len(kind)):
        count_arr.append(list(column_arr).count(kind[i]))
        count_select.append(list(select_arr).count(kind[i]))

    if chart_selector == "bar":

        fig, ax = plt.subplots()
        index = np.arange(len(kind))
        bar_width = 0.3

        ax.bar(index, count_arr, width = bar_width, label='ALL')
        ax.bar(index + bar_width, count_select, width = bar_width, label='select')
        ax.set_title(column_list_selector)
        ax.set_xticks(index + 0.5*bar_width, kind)
        ax.legend()

        st.pyplot(fig)

    if chart_selector == "hist":
        bin = st.sidebar.slider('binの数を決めてください', 2, len(kind), len(kind))

        Y, X, _ = plt.hist(column_arr, bins = bin)
        y_max = int(max(Y)) + 1

        fig2, ax2 = plt.subplots()

        ax2.hist(list(column_arr), bins = bin, ec = 'navy')
        ax2.set_xlabel(column_list_selector)
        ax2.set_ylabel("度数")
        ax2.set_yticks(np.arange(0, y_max, int(y_max/10)))

        st.pyplot(fig2)

    if chart_selector == "pie":
        fig3, ax3 = plt.subplots()

        ax3.pie(count_arr, startangle=90, labels = kind, autopct="%1.1f%%", labeldistance=0.7, pctdistance=0.5)
        ax3.set_title(column_list_selector)

        st.pyplot(fig3)

# ページ判定
if st.session_state.page_id == -1:
    main_page()
