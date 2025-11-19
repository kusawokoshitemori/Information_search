import streamlit as st
import pandas as pd

st.markdown(" ## トイレ検索")

# データの読み込み
try:
    df = pd.read_csv('Toilet.csv', encoding="Shift-JIS")
except FileNotFoundError:
    st.error("Toilet.csv が見つかりません。同じディレクトリに配置してください。")
    st.stop()
except Exception as e:
    st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    st.stop()

# 検索UIの表示
st.sidebar.subheader("検索条件")
male_exists = st.sidebar.checkbox("男性用洋式あり")
female_exists = st.sidebar.checkbox("女性用洋式あり")
multipurpose_exists = st.sidebar.checkbox("多機能トイレあり")

filtered_df = df.copy()

# 条件によってファルセット検索
if male_exists:
    filtered_df = filtered_df[filtered_df['男性用洋式'] != 0]

if female_exists:
    filtered_df = filtered_df[filtered_df['女性用洋式'] != 0]

if multipurpose_exists:
    filtered_df = filtered_df[filtered_df['多機能トイレ'] == 'あり']

if len(filtered_df) == 0:
    st.write("一致する結果はありません")
else:
    map_df = filtered_df[["latitude", "longitude"]].copy()
    map_df.columns = ['lat', 'lon']
    st.map(map_df)

    st.subheader("検索結果")
    for i in range(len(filtered_df)):
        st.markdown("---")
        st.write('<span style="color:red">' + filtered_df["name"].iloc[i] + '</span>', unsafe_allow_html=True)
        st.write("住所：" + filtered_df["住所"].iloc[i])
        st.write("カテゴリ：" + filtered_df["Category"].iloc[i])
        if male_exists:
            st.write(f"男性用洋式:" + f" {int(filtered_df['男性用洋式'].iloc[i])}")

        if female_exists:
            st.write(f"女性用洋式:" + f" {int(filtered_df['女性用洋式'].iloc[i])}")

        if multipurpose_exists:
            st.write(f"多機能トイレ:" + f" {filtered_df['多機能トイレ'].iloc[i]}")
