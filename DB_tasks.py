import pandas as pd
import sqlalchemy

df = pd.read_sql(
    """SELECT DISTINCT(topic)
    FROM post """,

    con="postgresql://robot-startml-ro:pheiph0hahj1Vaif@"
        "postgres.lab.karpov.courses:6432/startml"
)

print(df)