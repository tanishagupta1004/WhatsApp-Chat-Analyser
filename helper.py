from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
extract=URLExtract()
def fetch_stats(selected_user,df):

    if selected_user !="Overall":
        df = df[df['user'] == selected_user]
    #Fetch No. of Messages
    num_messages = df.shape[0]

    #Fetch No. of Words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #Fetch No. of Media Messages
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]

    #Fetch No. of links shared
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words),num_media_messages,len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': "percent"})
    return x,df

def create_wordcloud(selected_user,df):



    f = open('stopwards.txt', 'r')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)

    wc=WordCloud(width=250,height=250,max_font_size=20,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=""))

    return df_wc

def most_common_words(selected_user,df):

    f=open('stopwards.txt','r')
    stop_words=f.read()
    if selected_user !="Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
