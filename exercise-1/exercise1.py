import sqlite3

DATABASE = "database.sqlite"

con = sqlite3.connect(DATABASE)
cur = con.cursor()

def exercise1():
    """Exercise 1"""

    print("EXERCISE 1 BEGINNING")
    cur.execute("SELECT * FROM posts LIMIT 5")
    for row in cur:
        print(row)

    cur.execute("SELECT * FROM users LIMIT 5")
    for row in cur:
        print(row)

    cur.execute("SELECT * FROM follows LIMIT 5")
    for row in cur:
        print(row)

    cur.execute("SELECT * FROM comments LIMIT 5")
    for row in cur:
        print(row)

    cur.execute("SELECT * FROM reactions LIMIT 5")
    for row in cur:
        print(row)
    print("")

def exercise2():
    """Exercise 2, includes query for task 1.2"""

    print("EXERCISE 2 BEGINNING")
    cur.execute("SELECT location, COUNT(*) AS count FROM users GROUP BY location ORDER BY count DESC LIMIT 5")
    for row in cur:
        print(row)
    
    print("")

    cur.execute("SELECT COUNT(id) FROM users WHERE "
    "id NOT IN (SELECT user_id FROM comments) "
    "AND id NOT IN (SELECT user_id FROM posts) "
    "AND id NOT IN (SELECT user_id FROM reactions)")
    for row in cur:
        print(f"Count of lurkers: {row}")
    print("")

def exercise3():
    """Exercise 3, includes query for task 1.3"""

    print("EXERCISE 3 BEGINNING")
    cur.execute("SELECT AVG(birthdate) FROM users")
    for row in cur:
        print(f"Averaged birthyear: {row} Very unnovel I know but kind of gets the job done decent enough")

    cur.execute("SELECT birthdate FROM users ORDER BY birthdate ASC LIMIT 1")
    for row in cur:
        print(f"Oldest birthdate: {row}")

    cur.execute("SELECT birthdate FROM users ORDER BY birthdate DESC LIMIT 1")
    for row in cur:
        print(f"Youngest birthdate: {row}")

    print("")
    
    cur.execute("SELECT username, COUNT(*) as engagementCount " \
    "FROM posts " \
    "LEFT JOIN comments c ON posts.user_id = c.post_id " \
    "LEFT JOIN reactions r ON posts.user_id = r.post_id " \
    "JOIN users u ON posts.user_id = u.id "  
    "GROUP BY username "
    "ORDER BY engagementCount DESC "
    "LIMIT 5")

    for row in cur:
        print(row)
    print("")

def exercise4():
    """Exercise 4, includes query for task 1.4"""

    print("EXERCISE 4 BEGINNING")
    cur.execute("SELECT username, COUNT(*) as followerCount FROM users "
    "LEFT JOIN follows ON followed_id = users.id "
    "GROUP BY username "
    "ORDER BY followerCount DESC "
    "LIMIT 5")

    for row in cur:
        print(row)

    print("")

    cur.execute("SELECT users.username, COUNT(*) AS repeatedContent "
    "FROM (SELECT content, user_id FROM posts " \
    "UNION ALL SELECT content, user_id FROM comments) AS c " \
    "JOIN users ON c.user_id = id "
    "GROUP BY c.user_id, c.content " \
    "HAVING COUNT(*) >= 3")

    for row in cur:
        print(row)
    print("")


if __name__ == "__main__":
    exercise1()
    exercise2()
    exercise3()
    exercise4()
