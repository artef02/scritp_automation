# -*- coding: utf-8 -*-
import pandas as pd
import math
import numpy as np
from datetime import datetime
from IPython.display import display,HTML

date = "2024-05-01"
df = pd.read_excel('interventions_0105.xlsx')

import pandas as pd
from IPython.display import display, HTML
df['data_closed_at'] = pd.to_datetime(df['closed_at'].astype(str).str.split().str[0])
df[['user_reply_in_average_bh', 'user_reply_in_average_count']] = df[['user_reply_in_average_bh', 'user_reply_in_average_count']].fillna(0)
df['on_time_list'] = df['user_reply_in_average_bh'] * df['user_reply_in_average_count']
nombre_conversation = df['data_closed_at'].eq(date).sum()
nombre_conversation_inf_10800 = df.query('on_time_list <= 10800 and data_closed_at == @date').shape[0]
OnTime = f"{(nombre_conversation_inf_10800 / nombre_conversation * 100):.2f}%"
back_log = df.query('on_time_list > 10800 and data_closed_at == @date')['on_time_list'].mean()
back_log = (back_log - 10800) / 3600 if pd.notna(back_log) else 0

style = "<style>.result {text-transform:uppercase;color:rgb(255,102,0);font-weight:bold;text-align:center;padding:20px;font-size:20px;margin:auto;border:2px solid}</style>"
display(HTML(style + f"<div class='result'><span>On Time: </span>{OnTime}</div>"))
display(HTML(style + f"<div class='result'><span>Back Log: </span>{back_log}</div>"))

message = pd.read_excel('message_0105.xlsx')
date_message = "2024-05-26"

def transformation(message1,nom_colonne) :
    message_301 = message1[nom_colonne].value_counts().sort_index()
    df_intervalles1 = pd.DataFrame(message_301)
    df_intervalles1 = df_intervalles1.reset_index()
    df_intervalles1['index'] = pd.to_datetime(df_intervalles1['index'], format='%H:%M:%S').apply(lambda x: datetime(2000, 1, 1, x.hour, x.minute, x.second))
    index_range1 = pd.date_range(start='2000-01-01 00:00:00', end='2000-01-01 23:30:00', freq='30T')
    df_intervalles1 = df_intervalles1.set_index('index').reindex(index_range1, fill_value=0).reset_index()
    df_intervalles1['tranche_30min'] = df_intervalles1['index'].dt.time
    df_intervalles1 = df_intervalles1.drop(columns={'index'})
    df_intervalles1 = df_intervalles1.set_index('tranche_30min')
    return df_intervalles1

message['nb_massage_reçu'] = message['created_at'].dt.floor('30T').dt.time
message1 = message[(message['status']=='Répondu') | (message['status']=='En traitement') | (message['status']=='Nouveau') | (message['status']=='Archivé')]

message['nb_message_traité_Total agent (par rapport au reçus)'] = message['created_at'].dt.floor('30T').dt.time
message2 = message[(message['status']=='Répondu') | (message['status']=='En traitement') | (message['status']=='Archivé')]

message['nb_message_sortant_Total agent'] = message['created_at'].dt.floor('30T').dt.time
message3 = message[(message['status']=='Réponse agent') | (message['status']=='Message agent')]

df_intervalles1 = transformation(message1,'nb_massage_reçu')
df_intervalles2 = transformation(message2,'nb_message_traité_Total agent (par rapport au reçus)')
df_intervalles3 = transformation(message3,'nb_message_sortant_Total agent')

resultat = pd.concat([df_intervalles1,df_intervalles2,df_intervalles3],axis=1)
