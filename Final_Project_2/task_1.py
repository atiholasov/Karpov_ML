import pandas as pd
from sqlalchemy import create_engine
import math

SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

BD_tables = ['post', 'user', 'feed_action']

query_post = "SELECT * FROM post"
query_user = 'SELECT * FROM "user"'
query_feed_action = "SELECT * FROM feed_action LIMIT 200000"

chunksize = 200000

# df_post = pd.read_sql(query_post, engine, chunksize=chunksize)
# df_user = pd.read_sql(query_user, engine, chunksize=chunksize)
df_feed_action = pd.read_sql(query_feed_action, engine, chunksize=chunksize)

for df_chunk in df_feed_action:
    action_mapping = {'view': 0, 'like': 1}
    df_chunk['like'] = df_chunk['action'].map(action_mapping)
    df_chunk.drop(columns=["action"], inplace=True)


    train = df_chunk.iloc[:-50000].copy()
    test = df_chunk.iloc[-50000:].copy()

    pivot = train.pivot_table(index='post_id',
                              columns='user_id',
                              values='like')

    corrs = pivot.corr()
    corrs = (corrs.stack().rename_axis(['userId1','userId2']).reset_index())
    corrs.columns = ['userId1','userId2','corr']
    corrs = corrs[corrs['corr'] >= 0]

    preds = []

    for user in test['user_id'].unique():

        if user in train['user_id'].unique():
            part = test[test['user_id']==user]

            neighbors = corrs[corrs['userId1']==user]
            neighbors_users = neighbors['userId2'].unique()

            if neighbors_users.shape[0]==0:
                continue

            posts_ = part['post_id'].unique()

            train_part = train[train['user_id'].isin(neighbors_users)]

            neighbors_means = train_part.groupby('user_id')['like'].mean()

            print(neighbors_means.head())


