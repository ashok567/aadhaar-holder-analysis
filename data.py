import pandas as pd
import json

def read_data():
    df = pd.read_csv('data/aadhaar_data.csv')
    df = df.to_json(orient='records')
    return df