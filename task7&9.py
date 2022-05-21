import pandas as pd
from database import Database
import env
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
import botometer
import os
import tweepy as tw

def create_db():
    schema_name = env.master_db
    db_conf = env.db_production
    rdb = Database(schema=schema_name, **db_conf)
    engine = rdb.create_engine()
    return engine
connection = create_db()


def RateSentimentUsingVader(df):
    consumer_key = 'QkkJz50UsAimKlDiYLTD22YDE'
    consumer_secret = 'NyZylteqMnVH2qjdrU2pqOyi2j1Z7OXoH4BYtDycPHG8Ur0qDx'
    access_token = '1526907181991440385-vEKl302osvNTlT4ZczaN75txvWzDNt'
    access_token_secret = 'nHwFbRcy0wN1S2JAo8l20NN73liElTsuz1ecL9Xqf7YgX'
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    sid = SentimentIntensityAnalyzer()

    df['vader_scores'] = df['id'].apply(lambda x: sid.polarity_scores(api.get_status(x).text))
    df['vader_compound'] = df['vader_scores'].apply(lambda score_dict: score_dict['compound'])
    df['vader_negative'] = df['vader_scores'].apply(lambda score_dict: score_dict['neg'])
    df['vader_positive'] = df['vader_scores'].apply(lambda score_dict: score_dict['pos'])
    df['vader_neutral'] = df['vader_scores'].apply(lambda score_dict: score_dict['neu'])
    df['vader_overall_score'] = df['vader_positive'] + df['vader_negative']
    df.drop(['vader_scores'], axis=1, inplace=True)
    df['vader_sentiment_type'] = ''
    df.loc[df.vader_compound > 0.05, 'vader_sentiment_type'] = 'POSITIVE'
    df.loc[(df.vader_compound > -0.05) & (df.vader_compound < 0.05), 'vader_sentiment_type'] = 'NEUTRAL'
    df.loc[df.vader_compound <= -0.05, 'vader_sentiment_type'] = 'NEGATIVE'
    return df

def botOrHuman(df):
    rapidapi_key = "6051c92aa2msh5afa8a29d0ec40dp13d229jsn718f3f887c84"
    twitter_app_auth = {
        'consumer_key': 'QkkJz50UsAimKlDiYLTD22YDE',
        'consumer_secret': 'NyZylteqMnVH2qjdrU2pqOyi2j1Z7OXoH4BYtDycPHG8Ur0qDx',
        'access_token': '1526907181991440385-vEKl302osvNTlT4ZczaN75txvWzDNt',
        'access_token_secret': 'nHwFbRcy0wN1S2JAo8l20NN73liElTsuz1ecL9Xqf7YgX',
    }
    bom = botometer.Botometer(wait_on_ratelimit=True,
                              rapidapi_key=rapidapi_key,
                              **twitter_app_auth)

    dic_bots = {"bot5": 0, "bot10": 0, "bot15": 0, "bot20": 0, "bot25": 0, "bot30": 0}
    user_count = 0
    bot_count = 0
    value = 0
    for idx, row in df.iterrows():
        print(idx)
        try:
            value = bom.check_account(row['user_id'])['cap']['english']
            user_count = user_count + 1
        except:
            value = 0
            print(f"idx: {idx}")
            pass
        if value > 0.5:
            bot_count = bot_count + 1
        if user_count == 5:
            dic_bots["bot5"] = bot_count/5
        elif user_count == 10:
            dic_bots["bot10"] = bot_count/10
        elif user_count == 15:
            dic_bots["bot15"] = bot_count/15
        elif user_count == 20:
            dic_bots["bot20"] = bot_count/20
        elif user_count == 25:
            dic_bots["bot25"] = bot_count/25
        elif user_count == 30:
            dic_bots["bot30"] = bot_count/30

    df_bots = pd.DataFrame.from_dict(data=dic_bots,orient='index').reset_index()
    print(df_bots)

if __name__ == '__main__':
    query = "select distinct a.user_id From distinct_users_from_search_table_real_map a join link_status_search_with_ordering_real b limit 50"
    df = pd.read_sql(query, connection)
    botOrHuman(df)

    print("=========Starting Analysis with Vader=========")
    query = "select id from link_status_search_with_ordering_real"
    df = pd.read_sql(query, connection)
    df = RateSentimentUsingVader(df)
    df.to_sql('vader_analysis', connection, if_exists='replace')

