import pandas as pd
import numpy as np
import sqlite3


def read_data():
    conn = sqlite3.connect('data/aadhaar_stats.db')
    df = pd.read_sql('select * from state_counts', conn)
    df = df.to_json(orient='records')
    conn.close()
    return df


def preprocess():
    df = pd.read_csv('data/analysis.csv')
    df.rename(columns={'Aadhaar generated': 'Generated', 'Enrolment Rejected': 'Rejected', 'Residents providing email': 'Email Available', 'Residents providing mobile number': 'Contact Available'}, inplace=True)
    df.loc[df['Generated'] > 0, 'Generated'] = 1
    df.loc[df['Rejected'] > 0, 'Rejected'] = 1
    df.loc[df['Contact Available'] > 0, 'Contact Available'] = 1
    # print(df[df['Age']==0].count())
    df.loc[df['Age'] == 0, 'Age'] = np.NAN
    # print(len(df['State'].unique()))
    df['Gender'] = df['Gender'].map({'F': 0, 'M': 1, 'T': 2}).astype(np.int64)
    # print(df.info())
    return df


def get_insights(state):
    df = preprocess()
    res = df[df['State'] == state]
    res = res.to_json(orient='records')
    return res
