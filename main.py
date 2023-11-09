import streamlit as st
from streamlit_marquee import streamlit_marquee
import time
import os
import csv
import pandas as pd
import plotly.express as px
import base64

df = pd.read_csv("baseprices.csv")

# App title
st.set_page_config(
    page_title = 'Real-Time Crypto Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}

    /* This code gets the first element on the sidebar,
    and overrides its default styling */
    section[data-testid="stSidebar"] div:first-child {
        top: 0;
        height: 100vh;
    }
</style>
""", unsafe_allow_html=True)
hide_streamlit_margin = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
</style>
"""
st.markdown(hide_streamlit_margin, unsafe_allow_html=True)


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"gif"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )


def stock_ticker(text):
    streamlit_marquee(**{
        # the marquee container background color
        'background': "#000000",
        # the marquee text size
        'fontSize': '0px',
        # the marquee text color
        "color": "#18db28",
        # the marquee text content
        'content': text,
        # the marquee container width
        'width': 'auto',
        # the marquee container line height
        'lineHeight': "2px",
        # the marquee duration
        #'animationDuration': '20s',
    })


def read_file(filename):
    with open(f"{filename}", "r") as f:
        SMRF1 = f.readlines()
    return SMRF1

add_bg_from_local('appbackground.gif')

stock_ticker_source = []

with open('stock_list.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        company = row['COMPANY']
        price = row['PRICE']
        percent_change = row['CHANGE']

        if float(percent_change) > 0:
            plus_sign = "+"
        else:
            plus_sign = ""

        # Format the stock information into a string
        stock_info = f"{company} ${price} {plus_sign}{percent_change}%"
        stock_ticker_source.append(stock_info)

# Combine the stock information into a single string
stock_ticker_text = "    ".join(stock_ticker_source)

title = '<p style="font-family: Sans Serif; color:crimson; font-size: 40px;">KringleKoin\u2122 Market Price</p>'
st.markdown(title, unsafe_allow_html=True)

stock_ticker(f'<p style="font-family: Lucida Console; font-size: 24px">{stock_ticker_text}</p>')

fig = px.line(df, x='Time', y='Price $', color='Coin', color_discrete_sequence=["red", "green"], markers=True)
fig.update_layout(height=550, paper_bgcolor="rgba(255,0,0,0.3)", plot_bgcolor="rgba(255,255,255,0.6)", legend=dict(bgcolor='black'))
fig.update_traces(marker=dict(size=10, symbol=df["marker"], angleref="previous"))
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

initial = read_file("baseprices.csv")
while True:
    time.sleep(10)
    current = read_file("baseprices.csv")
    if initial != current:
        st.rerun()
