import streamlit as st
import pandas as pd

# GitHubリポジトリ内のCSVファイルのパスを指定
file_path = 'data/testデータ.csv'

# CSVファイルの読み込み
df = pd.read_csv(file_path)

# 列の順序を指定
columns_order = [
    "企業コード", "企業名", "店舗コード", "店舗名", "コード", "アイテム名", 
    "店舗設定名", "売上数量", "売上金額", "値引金額", "買取数", "客数", 
    "売上金額(Vポイント値引き前)", "Vポイント値引き額(税込み)", 
    "Vポイント値引額(標準税率分/税込)", "Vポイント値引額(軽減税率分/税込)", 
    "売上金額(標準税率分/税抜)", "売上金額(軽減税率分/税抜)"
]

# 指定された列順に並び替え（存在する場合のみ）
df = df[[col for col in columns_order if col in df.columns]]

# フィルターをサイドバーに配置
st.sidebar.header("フィルター")

# セッション状態でフィルターの選択を保持
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = "(すべて)"

if 'selected_store' not in st.session_state:
    st.session_state.selected_store = "(すべて)"

# 企業名を選択する
companies = ["(すべて)"] + df["企業名"].unique().tolist()
company_index = companies.index(st.session_state.selected_company)
selected_company = st.sidebar.selectbox("企業名", companies, index=company_index)

# 企業名を選んだ後に関連する店舗名のみ表示
if selected_company != "(すべて)":
    filtered_stores = df[df["企業名"] == selected_company]["店舗名"].unique().tolist()
else:
    filtered_stores = df["店舗名"].unique().tolist()

# 店舗名を選択する
store_index = filtered_stores.index(st.session_state.selected_store) if st.session_state.selected_store in filtered_stores else 0
selected_store = st.sidebar.selectbox("店舗名", ["(すべて)"] + filtered_stores, index=store_index)

# フィルター解除ボタン
if st.sidebar.button("フィルター解除"):
    st.session_state.selected_company = "(すべて)"
    st.session_state.selected_store = "(すべて)"

# フィルタリング処理
filtered_df = df.copy()
if selected_company != "(すべて)":
    filtered_df = filtered_df[filtered_df["企業名"] == selected_company]
if selected_store != "(すべて)":
    filtered_df = filtered_df[filtered_df["店舗名"] == selected_store]

# 集計表の表示
st.write(filtered_df)
