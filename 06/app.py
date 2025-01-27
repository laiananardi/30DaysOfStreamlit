# dataset from: https://www.kaggle.com/datasets/charunisa/chatgpt-sentiment-analysis/data

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from wordcloud import WordCloud, STOPWORDS
import re

df = pd.read_csv('assets/file.csv')
df.dropna(inplace=True)

df = df[['tweets', 'labels']]
st.header('ChatGPT Sentiment Analysis Dashboard')

st.write('Analyze tweets about ChatGPT! See sentiment trends, explore the data, view word clouds, and check text length.')

# Data Table Section
st.header("Dataset Preview")
if st.button("Show All Data"):
    st.write(df)
else:
    st.write(df.head(3))


# Sentiment Chart Section
st.header("Sentiment Distribution")


sentiment_chart = alt.Chart(df).mark_bar().encode(
    x='labels',
    y='count()',
    color=alt.Color('labels', 
                    scale=alt.Scale(domain=['neutral', 'good', 'bad'],
                    range=['#1f77b4', '#2ca02c', '#d62728'])
                    ), 
).properties(
    width=600,
    height=400
).configure_axis(
    labelAngle=0  # Keeps the x-axis labels horizontal
)
st.write(sentiment_chart)


# Function to clean tweets and remove stray characters
def clean_text(text):
    # Remove anything that's not a letter or a space (such as single letters or punctuation)
    text = re.sub(r'\b\w{1,2}\b', '', text)  # Remove words with 1 or 2 characters
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text


# Word Cloud for Each Sentiment (Optional):
st.header("Word Cloud by Sentiment")
sentiment = st.selectbox('Select Sentiment', ['All', 'Positive', 'Negative', 'Neutral'])

if st.button("Generate Word Cloud by Sentiment"):
    if sentiment == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['labels'] == sentiment.lower()]
    
    # Clean all tweet texts
    cleaned_tweets = " ".join(df['tweets'].apply(clean_text))

    # Create a word cloud from the filtered text, excluding stopwords
    wordcloud = WordCloud(
        stopwords=STOPWORDS,  # Exclude stopwords
        width=800, 
        height=400, 
        max_words=50,
        collocations=False,
        background_color='white'
    ).generate(cleaned_tweets)

    
    # Create the figure and axis object explicitly
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Hide axis
    st.pyplot(fig)

# Text Length Distribution

df['text_length'] = df['tweets'].str.len()

st.header("Text Length Distribution:")
chart = alt.Chart(df).mark_bar().encode(
    alt.X('text_length:Q', bin=True, title='Text Length'),
    alt.Y('count():Q', title='Frequency')
).properties(
    title='Distribution of Text Length in Tweets',
    width=600,
    height=400
)

st.altair_chart(chart)
