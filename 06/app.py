# dataset from: https://www.kaggle.com/datasets/abhi8923shriv/sentiment-analysis-dataset/code


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from wordcloud import WordCloud, STOPWORDS
import re

df = pd.read_csv('assets/train.csv', encoding='unicode_escape')
df.dropna(inplace=True)
df = df[['text', 'sentiment']]
st.header('Tweet Sentiment Analysis App')

st.write('Welcome to the Tweet Sentiment Analysis App! Explore insights from tweets, including sentiment distribution, frequent words, and user demographics.')

# Data Table Section
st.header("Dataset Preview")
if st.button("Show All Data"):
    st.write(df)
else:
    st.write(df.head(3))


# Sentiment Chart Section
st.header("Sentiment Distribution")


sentiment_chart = alt.Chart(df).mark_bar().encode(
    x='sentiment',
    y='count()',
    color=alt.Color('sentiment', 
                    scale=alt.Scale(domain=['neutral', 'positive', 'negative'],
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
        filtered_df = df[df['sentiment'] == sentiment.lower()]
    
    # Clean all tweet texts
    cleaned_tweets = " ".join(df['text'].apply(clean_text))

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

df['text_length'] = df['text'].str.len()

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
