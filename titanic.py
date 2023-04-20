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

    #選択する各項目のリスト作成用
    def df_list(x):
        st.session_state.df_list = list(set(st.session_state.df0[x].dropna(how='all')))

    #選択されている項目のテキスト表示用
    def add_text(x, y):
        if list(set(x)) == list(set(st.session_state.df0[y].dropna(how='all'))):
            st.sidebar.text("全ての人が選ばれています。")
        else:
            st.sidebar.text(str(set(st.session_state.df0[y].dropna(how='all')) - set(x)) + "の人が除かれています。")

    #元データから棒グラフ、円グラフ、ヒストグラムで描画しても複雑になる要素の削除
    column_list = st.session_state.df0.columns.values
    column_list = column_list[column_list != 'Survived']
    column_list = column_list[column_list != 'Name']
    column_list = column_list[column_list != 'Ticket']
    column_list = column_list[column_list != 'Cabin']

    column_list_selector = st.sidebar.selectbox("どの要素についてのグラフを描きますか？", column_list)

    #棒グラフ、円グラフ、ヒストグラムで描画しても複雑になるグラフ要素の削除
    if column_list_selector in ["Pclass", "Sex", "Embarked"]:
        chart_list = ["以下から選んでください", "bar", "pie"]
    elif column_list_selector in ["Age", "Fare"]:
        chart_list = ["以下から選んでください", "hist"]
    else:
        chart_list = ["以下から選んでください", "bar", "hist", "pie"]

    chart_selector = st.sidebar.selectbox("どんなグラフを描きますか？",chart_list)

    #サイドバー作成用
    #生存or死亡
    df_list("Survived")
    st.session_state.survive_selector = st.sidebar.multiselect("Survived",st.session_state.df_list, default = st.session_state.df_list)
    if st.session_state.survive_selector == [0]:
        st.sidebar.text("生存者が選ばれています。")
    elif st.session_state.survive_selector == [1]:
        st.sidebar.text("死亡者が選ばれています。")
    else:
        st.sidebar.text("全ての人が選ばれています。")

    #性別
    df_list("Sex")
    st.session_state.sex_selector = st.sidebar.multiselect("Sex", st.session_state.df_list, default = st.session_state.df_list)
    if st.session_state.sex_selector == ["male"]:
        st.sidebar.text("男性が選ばれています。")
    elif st.session_state.sex_selector == ["female"]:
        st.sidebar.text("女性が選ばれています。")
    else:
        st.sidebar.text("全ての人が選ばれています。")

    #同乗している兄弟や配偶者
    df_list("SibSp")
    sibsp_selector = st.sidebar.multiselect('SibSp', st.session_state.df_list, default = st.session_state.df_list)
    add_text(sibsp_selector, "SibSp")

    #同乗している親
    df_list("Parch")
    parch_selector = st.sidebar.multiselect('Parch', st.session_state.df_list, default = st.session_state.df_list)
    add_text(parch_selector, "Parch")

    #出港地
    df_list("Embarked")
    embarked_selector = st.sidebar.multiselect('Embarked', st.session_state.df_list, default = st.session_state.df_list)
    add_text(embarked_selector, "Embarked")

    st.session_state.select_arr = st.session_state.df0[
                                        (
                                        st.session_state.df0["Survived"].isin(st.session_state.survive_selector)
                                        & st.session_state.df0["Sex"].isin(st.session_state.sex_selector)
                                        & st.session_state.df0["SibSp"].isin(sibsp_selector)
                                        & st.session_state.df0["Parch"].isin(parch_selector)
                                        & st.session_state.df0["Embarked"].isin(embarked_selector)
                                        )
                                    ][column_list_selector]
    count_arr = []
    count_select =[]
    column_arr = st.session_state.df0[column_list_selector]
    kind = list(set(column_arr.dropna(how='all')))

    for i in range(len(kind)):
        count_arr.append(list(column_arr).count(kind[i]))
        count_select.append(list(st.session_state.select_arr).count(kind[i]))

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
        ax2.hist(list(st.session_state.select_arr), bins = bin, ec = 'navy', alpha = 0.5)
        ax2.set_xlabel(column_list_selector)
        ax2.set_ylabel("度数")
        ax2.set_yticks(np.arange(0, y_max, int(y_max/10)))

        st.pyplot(fig2)

    if chart_selector == "pie":
        fig3, ax3 = plt.subplots()
        fig4, ax4 = plt.subplots()

        ax3.pie(count_arr, startangle=90, labels = kind, autopct="%1.1f%%", labeldistance=0.7, pctdistance=0.5)
        ax3.set_title(column_list_selector)

        ax4.pie(count_select, startangle=90, labels = kind, autopct="%1.1f%%", labeldistance=0.7, pctdistance=0.5)
        ax4.set_title(column_list_selector)

        st.pyplot(fig3)
        st.pyplot(fig4)

# ページ判定
if st.session_state.page_id == -1:
    main_page()
