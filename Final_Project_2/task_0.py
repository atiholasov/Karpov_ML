import pandas as pd
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

BD_tables = ['post', 'user', 'feed_action']

query_post = "SELECT * FROM post"
query_user = 'SELECT * FROM "user"'
query_feed_action = "SELECT * FROM feed_action LIMIT 200000"


# for_exp_q = "SELECT action, COUNT(post_id) FROM feed_action GROUP BY action"
# for_exp = pd.read_sql(for_exp_q, engine)
# print(for_exp)



chunksize = 200000


# DATA = f"""SELECT *
#         FROM feed_action f
#         JOIN post p on f.user_id = p.id
#         JOIN "user" u on f.user_id = u.id
#         LIMIT 20
#         """
##
# DF = pd.read_sql(DATA, engine, chunksize=chunksize)
#
# for DF_chunk in DF:
#     DF_chunk.drop(columns=["post_id"], inplace=True)
#     DF_chunk.drop(columns=["id"], inplace=True)
#     new_column_order = ["user_id", "gender", "age", "country", "city", "exp_group", "os", "source", "text", "topic",
#                         "time", "action"]
#     DF_chunk = DF_chunk.reindex(columns=new_column_order)
#     print(len(DF_chunk.columns))

# df_post = pd.read_sql(query_post, engine, chunksize=chunksize)
# df_user = pd.read_sql(query_user, engine, chunksize=chunksize)
df_feed_action = pd.read_sql(query_feed_action, engine, chunksize=chunksize)

# print('df_post')
# print(df_post.head())
# print('df_user')
# print(df_user.head())
# print('df_feed_action')
# print(df_feed_action.head())

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

    print(corrs)

    # print(df_chunk.head(10))
    # print(df_chunk.tail())

# print(f'len_post = {len(df_post)}')
# print(f'len_user = {len(df_user)}')
# print(f'len_actions = {len(df_feed_action)}')
