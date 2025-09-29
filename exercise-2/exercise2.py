import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

DATABASE = "database.sqlite"

con = sqlite3.connect(DATABASE)
cur = con.cursor()

def exercise1():
    print("EXERCISE 1 BEGINNING")

    date_values_user = []

    cur.execute("SELECT created_at FROM users ORDER BY created_at ASC")
    for row in cur:
        date_values_user.append(row[0])

    datetime_values_users = pd.to_datetime(date_values_user)

    series = pd.Series(1, index = datetime_values_users)

    total_count_cumulative = series.resample("ME").count().cumsum()

    userData = {
        'users': total_count_cumulative
    }
    userdf = pd.DataFrame(userData)

    plt.plot(userdf['users'])
    plt.title("Growth of users")
    plt.xlabel("Count")
    plt.ylabel("Date")
    plt.legend("Test")
    plt.show()

    forecastdf = total_count_cumulative.reset_index()
    forecastdf.columns = ["ds", "y"] # Why does Prophet *require* this :)))

    future_user_count_model = Prophet(growth = "linear")
    future_user_count_model.fit(forecastdf)

    prediction = future_user_count_model.make_future_dataframe(periods = 3*365, freq = "D")
    prediction["cap"] = 350
    forecast = future_user_count_model.predict(prediction)
    future_user_count_model.plot(forecast)
    plt.show()
    
    print(" ")

def exercise2():
    print("EXERCISE 2 BEGINNING")
    
    query = """WITH comment_scoring AS (
                SELECT post_id, ROUND(COUNT(*) * 0.75, 1) AS score
                FROM comments
                GROUP BY post_id
            ), reaction_scoring AS (
                SELECT post_id, ROUND(COUNT(*) * 0.25, 1) AS score
                FROM reactions 
                GROUP BY post_id
            ), total_scoring AS (
                SELECT post_id, SUM(score) AS total_score FROM (
                    SELECT * FROM comment_scoring
                    UNION ALL
                    SELECT * FROM reaction_scoring
                )
                GROUP BY post_id
            )
            SELECT post_id, total_score
            FROM total_scoring
            GROUP BY post_id
            ORDER BY total_score DESC
            LIMIT 3
            """
    cur.execute(query)
    for row in cur:
        print(f"Post id and engagement score: {row}")
    print(" ")

def exercise3():
    print("EXERCISE 3 BEGINNING")

    query = """
    WITH engagements AS (
        SELECT post_id,
        MIN(created_at) AS first_engagement,
        MAX(created_at) AS last_engagement
        FROM comments
        GROUP BY post_id
    )
    SELECT ROUND(AVG(JULIANDAY(e.first_engagement) - JULIANDAY(p.created_at)), 1),
    ROUND(AVG(JULIANDAY(e.last_engagement) - JULIANDAY(p.created_at)), 1) FROM posts p
    LEFT JOIN engagements e ON p.id = e.post_id
    """
    cur.execute(query)
    print("Differences counted in days")
    for row in cur:
        print(f"Time until first engagement average: {row[0]}")
        print(f"Time until last engagement average: {row[1]}")
    print(" ")

def exercise4():
    print("EXERCISE 4 BEGINNING")
    
    query = """
    WITH comment_engagement AS (
        SELECT
            p.user_id AS poster,
            c.user_id AS engager,
            COUNT(*) AS count
        FROM comments c
        JOIN posts p ON c.post_id = p.id
        GROUP BY p.user_id, c.user_id
    ),
    reaction_engagement AS (
        SELECT
            p.user_id AS poster,
            r.user_id AS engager,
            COUNT(*) AS count
        FROM reactions r
        JOIN posts p ON r.post_id = p.id
        GROUP BY p.user_id, r.user_id
    ),
    total_engagement AS (
        SELECT
            poster,
            engager,
            SUM(count) AS count
        FROM (
            SELECT * FROM comment_engagement
            UNION ALL
            SELECT * FROM reaction_engagement
        )
        GROUP BY poster, engager
    ),
    pairs AS (
        SELECT
            CASE WHEN poster < engager THEN poster ELSE engager END AS user1,
            CASE WHEN poster < engager THEN engager ELSE poster END AS user2,
            SUM(count) AS interaction_count
        FROM total_engagement
        WHERE poster != engager
        GROUP BY user1, user2
    )
    SELECT
        u1.username AS user1,
        u2.username AS user2,
        p.interaction_count
    FROM pairs p
    JOIN users u1 ON u1.id = p.user1
    JOIN users u2 ON u2.id = p.user2
    ORDER BY p.interaction_count DESC
    LIMIT 3
    """
    cur.execute(query)
    for row in cur:
        print(row)

if __name__ == "__main__":
    exercise1()
    exercise2()
    exercise3()
    exercise4()
