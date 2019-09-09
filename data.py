import pandas as pd
import numpy as np
import sqlite3
import json


def read_data():
    conn = sqlite3.connect('data/aadhaar_stats.db')
    df = pd.read_sql('select * from state_counts', conn)
    df = df.to_json(orient='records')
    conn.close()
    return df


def preprocess():
    df = pd.read_csv('data/analysis.csv')
    df.rename(columns={'Aadhaar generated': 'Generated',
                       'Enrolment Rejected': 'Rejected',
                       'Residents providing email': 'Email Available',
                       'Residents providing mobile number':
                       'Contact Available'}, inplace=True)
    df.loc[df['Generated'] > 0, 'Generated'] = 1
    df.loc[df['Rejected'] > 0, 'Rejected'] = 1
    df.loc[df['Contact Available'] > 0, 'Contact Available'] = 1
    # print(df[df['Age']==0].count())
    df.loc[df['Age'] == 0, 'Age'] = np.NAN
    # print(len(df['State'].unique()))
    df['Gender'] = df['Gender'].map({'F': 0, 'M': 1, 'T': 2}).astype(np.int64)
    # print(df.info())
    return df


def gender_ratio(df):
    gender_df = df.groupby('Gender').sum().reset_index()
    m_count = gender_df[gender_df['Gender'] == 1]['Generated'][1]
    f_count = gender_df[gender_df['Gender'] == 0]['Generated'][0]
    m_ratio = round((m_count/(m_count+f_count))*100, 2)
    f_ratio = round((f_count/(m_count+f_count))*100, 2)
    gender_sent = '''On an average, {0}% of men and {1}% of women have been given aadhaar cards'''.format(str(m_ratio), str(f_ratio))
    return gender_sent


def get_insights(state):
    res = {}
    df = preprocess()
    state_df = df[df['State'] == state]
    gender_sent = gender_ratio(state_df)
    res['gender_sent'] = gender_sent
    print(res)
    return json.dumps(res)
