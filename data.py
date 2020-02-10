import pandas as pd
import numpy as np
import sqlite3
import json
from fractions import Fraction


conn = sqlite3.connect('data/aadhaar_stats.db')
dataset = pd.read_csv('data/analysis.csv', low_memory=False)
dataset.rename(columns={'Aadhaar generated': 'Generated',
                        'Enrolment Rejected': 'Rejected',
                        'Residents providing email': 'Email Available',
                        'Residents providing mobile number':
                        'Contact Available'}, inplace=True)
dataset.loc[dataset['Generated'] > 0, 'Generated'] = 1
dataset.loc[dataset['Rejected'] > 0, 'Rejected'] = 1
dataset.loc[dataset['Contact Available'] > 0, 'Contact Available'] = 1
dataset.loc[dataset['Age'] == 0, 'Age'] = np.NAN
dataset['Gender'] = dataset['Gender'].map(
    {'F': 0, 'M': 1, 'T': 2}).astype(np.int64)


def read_data():
    df = pd.read_sql('select * from state_counts', conn)
    df = df.to_json(orient='records')
    return df


def aadhaar_ratio(state):
    df = pd.read_sql(
        "select * from state_counts where State=\'{0}\'".format(state), conn)
    appl_ratio = (float(df['Aadhaar_Count']) / float(df['Population']))*100
    if appl_ratio <= 100:
        appl_sent = '''Aadhaar applications percentage of \
            {1} is {0}%'''.format(
            str(round(appl_ratio, 2)), state)
    else:
        appl_sent = '''Aadhaar applications percentage of {0} is exceeded more \
            than 100%'''.format(
            state)
    return appl_sent


def gender_ratio(df):
    m_count = df[df['Gender'] == 1]['Gender'].count()
    f_count = df[df['Gender'] == 0]['Gender'].count()
    m_ratio = round((m_count/(m_count+f_count))*100, 2)
    f_ratio = round((f_count/(m_count+f_count))*100, 2)
    gender_sent = '''{0}% men and {1}% women have applied for \
        Aadhaar'''.format(
        str(m_ratio), str(f_ratio))
    return gender_sent


def contact_details(df):
    yes_df = df[df['Contact Available']
                == 1]['Contact Available'].count()
    contact_sent = '''{0} of state population have provided \
        contact details'''.format(
        str(Fraction(yes_df, len(df))))
    return contact_sent


def approval_count(df):
    approved = df[df['Rejected'] == 0]['Rejected'].count()
    ratio = (approved/len(df))*100
    approval_sent = '''{0}% of Aadhaars were approved by UIDIA'''.format(
        str(round(ratio, 2)))
    return approval_sent


def get_insights(state):
    res = {}
    appl_sent = aadhaar_ratio(state)
    res['appl_sent'] = appl_sent
    state_df = dataset[dataset['State'] == state]
    gender_sent = gender_ratio(state_df)
    res['gender_sent'] = gender_sent
    contact_sent = contact_details(state_df)
    res['contact_sent'] = contact_sent
    approval_sent = approval_count(state_df)
    res['approval_sent'] = approval_sent
    return json.dumps(res)
