import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

# タイトル、見出し表示
st.title('Miyako先生 Online Guitar Lessons')

# ヘッダー写真表示
image = Image.open('MiyakoPic.jpg')
st.image(image)
st.subheader('Lesson 一覧')

# Lesson一覧のCSV読み込み、曲選択のためのセレクトボックス設定
df_lesson= pd.read_csv('lessonRecord.csv')
song_list = np.sort(df_lesson['Song'].unique())
song_list = np.insert(song_list, 0, 'Please select song')
song_selcted = st.sidebar.selectbox("Songs", song_list)

# テーブル中でリンクが必要なデータの作成用関数
def create_table_clickable(df_col_link, df_col_name):
    for idx, link in enumerate(df_col_link):
        link_name = df_col_name[idx]
        if link_name != 'No scores':
            df_col_link[idx] =  f'<a target="_blank" href="{link}">' + link_name + '</a>'

    return df_col_link

# レッスン一覧テーブルの表示
df = pd.DataFrame()
df['Song'] = df_lesson['Song']

df['Date'] = df_lesson['Dae of lesson'].apply(lambda x: x.replace('年','/'))
df['Date'] = df['Date'].apply(lambda x: x.replace('月','/'))
df['Date'] = df['Date'].apply(lambda x: x.replace('日',''))
df['Date'] = pd.to_datetime(df['Date'])

df['Lesson'] = df_lesson['Lesson name']
df['Score_1'] = df_lesson['Score Name'].fillna("")
df['Score_2'] = df_lesson['Score Name 2'].fillna("")
df['Remark'] = df_lesson['Remarks'].fillna("")

#　リンクが必要なカラムの作成
df['Lesson'] = create_table_clickable(df_lesson['Link to Lesson'], df_lesson['Lesson name'])
df['Score_1'] = create_table_clickable(df_lesson['Link to score 1'].fillna(""), df['Score_1'])    
df['Score_2'] = create_table_clickable(df_lesson['Link to score 2'].fillna(""), df['Score_2'])

df = df.sort_values('Date', ascending=False)

if song_selcted == 'Please select song':
    df = df.sort_values('Date', ascending=False)
else:
    df = df[df['Song']==song_selcted]
    df = df.sort_values('Date', ascending=False)

st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)