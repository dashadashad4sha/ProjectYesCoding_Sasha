import sqlite3


def add_player(username):
    bd = sqlite3.connect("grabmen_db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
        select * from users
        where name='{username}';
                """)

    res = a.fetchall()

    if not res:
        cur.execute(f"""
            insert into users (name)
            values ('{username}');
                    """)

        a = cur.execute(f"""
                select user_id from users
                where name='{username}';
                        """)
        res = a.fetchall()
        cur.execute(f"""
                    insert into users_skins (user_id, skin_id)
                    values ({res[0][0]}, 1);
                            """)

    bd.commit()
    cur.close()


def add_score(username, score):
    bd = sqlite3.connect("grabmen_db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
        select best_score, balance from users
        where name='{username}';
                """)

    res = a.fetchall()

    if res[0][0] < score:
        cur.execute(f"""
                update users 
                set best_score={score}
                where name='{username}';
                     """)

    balance = res[0][1]
    cur.execute(f"""
                update users 
                set balance={balance + score}
                where name='{username}';
                 """)

    bd.commit()
    cur.close()


def leaderboard():
    bd = sqlite3.connect("grabmen_db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
        select name, best_score from users
        order by best_score desc
        limit 3;
                """)

    res = a.fetchall()

    bd.commit()
    cur.close()
    return res


def best_score(name):
    bd = sqlite3.connect("grabmen_db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
            select best_score from users
            where name='{name}';
                    """)

    res = a.fetchall()

    bd.commit()
    cur.close()
    return res


def get_skin_info(skin_id):
    bd = sqlite3.connect("grabmen_db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
                select * from skins
                where skin_id='{skin_id}';
                        """)

    res = a.fetchall()

    info = {'cost': res[0][1], 'color1': res[0][2], 'color2': res[0][3], 'width': res[0][4]}

    bd.commit()
    cur.close()
    return info


def user_has_skin(user_name, skin_id):
    bd = sqlite3.connect("grabmen_db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
                    select * from users_skins
                    where skin_id={skin_id} and user_id=(select user_id from users where name='{user_name}')
                            """)

    res = a.fetchall()
    bd.commit()
    cur.close()

    if not res:
        return False
    return True


def balance(user_name):
    bd = sqlite3.connect("grabmen_db.db")
    cur = bd.cursor()

    a = cur.execute(f"""
                     select balance from users
                     where name='{user_name}';
                     """)

    balance = a.fetchall()
    return balance[0][0]


def buy_skin(user_name, skin_id, cost):
    bd = sqlite3.connect("grabmen_db.db")
    cur = bd.cursor()

    a = cur.execute(f"""
                 select balance from users
                 where name='{user_name}';
                 """)

    balance = a.fetchall()[0][0]

    if balance >= cost:
        cur.execute(f"""
            insert into users_skins (user_id, skin_id)
            values ((select user_id from users where name='{user_name}'), {skin_id});
                    """)

        cur.execute(f"""
                update users 
                set balance={balance - cost}
                where name='{user_name}';
                        """)
    bd.commit()
    cur.close()
