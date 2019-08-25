import pandas as pd
import json
import sqlite3

def read_data():
    conn = sqlite3.connect('data/aadhaar_stats.db')
    df = pd.read_sql('select * from state_counts', conn)
    df = df.to_json(orient='records')
    conn.close()
    return df


