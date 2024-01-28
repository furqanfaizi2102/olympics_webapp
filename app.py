import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy as sp



df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')


user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis')
)



if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    year,country = helper.country_year_list((df))

    selected_year = st.sidebar.selectbox("Select Year",year)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Performance in " + str(selected_year) + ' Olympics')
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    atheletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.header('Top Statistics')

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)

    with col2:
        st.header('Hosts')
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Events')
        st.title(events)

    with col2:
        st.header('Nations')
        st.title(nations)

    with col3:
        st.header('Atheletes')
        st.title(atheletes)

    nations_over_time = helper.data_over_time(df,'region')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': 'No.of Countries'}, inplace=True)
    st.title('Participating Nations Over The Years')
    fig = px.line(nations_over_time, x='Edition', y='No.of Countries')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    events_over_time.rename(columns={'Year': 'Edition', 'count': 'No.of Events'}, inplace=True)
    st.title('Events Over The Years')
    fig = px.line(events_over_time, x='Edition', y='No.of Events')
    st.plotly_chart(fig)

    atheletes_over_time = helper.data_over_time(df, 'Name')
    atheletes_over_time.rename(columns={'Year': 'Edition', 'count': 'No.of Atheletes'}, inplace=True)
    st.title('Atheletes Over The Years')
    fig = px.line(atheletes_over_time, x='Edition', y='No.of Atheletes')
    st.plotly_chart(fig)

    st.title('No.of Events Over Time(Every Sport)')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(subset=['Year', 'Event', 'Sport'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)


    st.title('Most Successfull Athelete')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successfull(df,selected_sport)
    st.table(x)

if user_menu == 'Country Wise Analysis':

    st.sidebar.title('Country Wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select Country',country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)

    st.title(selected_country + ' Medal Tally Over The Year')
    fig = px.line(country_df, x='Year', y='Medal')
    st.plotly_chart(fig)

    st.title(selected_country + ' Excels in following Sport')
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)


    st.title('Top 10 Athelete of ' + selected_country)
    top_10 = helper.most_successfull_countrywise(df,selected_country)
    st.table(top_10)




