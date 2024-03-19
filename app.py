from fastapi import FastAPI, HTTPException
from datetime import date
from datetime import timedelta
from pydantic import BaseModel
# import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

"""
@app.get("/")
def say_hello():
    return "hello, world"


@app.get("/sum")
def sum_two(a: int, b: int) -> int:
    return a + b


@app.get("/print/{number}/{num_2}")
def print_num(number: int, num_2: int) -> int:
    return number ** 2 + num_2


@app.get("/sum_date")
def sum_date(current_date: date, offset: int) -> date:
    var = timedelta(days=offset)
    ans = current_date + var
    return ans


@app.post("/user_hello")
def out_print(name: str):
    return {"message": f"Hello, {name}"}




class User(BaseModel):
    name: str
    surname: str
    age: int
    registration_date: date


@app.post("/user/validate")
def validate(user_data: User):
    callback = f"Will add user: {user_data.name} {user_data.surname} with age {user_data.age}"
    return callback


@app.get('/db')
def call_to_db(size: int):
    df = pd.read_sql(
        f'''
            SELECT *
            FROM "user"
            LIMIT {size}
            ''',
        con="postgresql://robot-startml-ro:pheiph0hahj1Vaif@"
            "postgres.lab.karpov.courses:6432/startml"
    )

    return df.to_dict()

"""


@app.get('/user/{id}')
def call_to_db(id: int):
    conn = psycopg2.connect("postgresql://robot-startml-ro:pheiph0hahj1Vaif@"
                            "postgres.lab.karpov.courses:6432/startml",
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    cursor.execute(
        f"""
                SELECT gender, age, city
                FROM "user"
                WHERE id = {id}
                """)
    result = cursor.fetchone()
    if result == None:
        raise HTTPException(status_code=404, detail="user not found")
    else:
        return result


