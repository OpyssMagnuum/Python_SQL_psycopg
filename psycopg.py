import psycopg2


def create_table(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        name VARCHAR(40),
        surname VARCHAR(40),
        email VARCHAR(80)
    );
    
    CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        phone_id INTEGER NOT NULL REFERENCES client(id),
        number VARCHAR(20) default NULL
    );
    """)


def add_client(cur, id, name, surname, email, phones=None):
    cur.execute("""
    INSERT INTO client(id, name, surname, email) VALUES(%s, %s, %s, %s);
    """, (id, name, surname, email))
    if phones is not None:
        if isinstance(phones, str):
            cur.execute("""
            INSERT INTO phones(phone_id, number) VALUES(%s, %s);
            """, (id, phones))
        else:
            for phone in phones:
                cur.execute("""
                INSERT INTO phones(phone_id, number) VALUES(%s, %s);
                """, (id, phone))


def add_phone_to_client(cur, cl_id, phones):
    if isinstance(phones, str):
        cur.execute("""
        INSERT INTO phones(phone_id, number) VALUES(%s, %s);
        """, (cl_id, phones))
    else:
        for phone in phones:
            cur.execute("""
            INSERT INTO phones(phone_id, number) VALUES(%s, %s);
            """, (cl_id, phone))


def change_client_data(cur, id, name=None, surname=None, email=None, phones=None):
    if name is not None:
        cur.execute("""
        UPDATE client SET name=%s WHERE id=%s;
        """, (name, id))
    if surname is not None:
        cur.execute("""
        UPDATE client SET surname=%s WHERE id=%s;
        """, (surname, id))
    if email is not None:
        cur.execute("""
        UPDATE client SET email=%s WHERE id=%s;
        """, (email, id))
    if phones is not None:
        # Мы как бы заново добавляем телефон(ы)
        cur.execute("""
        DELETE FROM phones WHERE phone_id=%s;
        """, id)
        add_phone_to_client(cur, id, phones)


def delete_phone(cur, id, phone):
    cur.execute("""
    DELETE FROM phones WHERE number=%s AND phone_id=%s;
    """, (phone, id))


def delete_client(cur, id):
    cur.execute("""
    DELETE FROM phones WHERE phone_id=%s;
    DELETE FROM client WHERE id=%s
    """, (id, id, ))


def client_search(cur, name=None, surname=None, email=None, phones=None):
    if name is not None:
        cur.execute("""
        SELECT * FROM client WHERE name = %s;
        """, (name, ))
        print(cur.fetchall())

    if surname is not None:
        cur.execute("""
        SELECT * FROM client WHERE surname=%s;
        """, (surname, ))
        print(cur.fetchall())
    if email is not None:
        cur.execute("""
        SELECT * FROM client WHERE email=%s;
        """, (email, ))
        print(cur.fetchall())
    if phones is not None:
        cur.execute("""
        SELECT * FROM phones WHERE number=%s;
        """, (phones, ))
        print(cur.fetchall())


# Подключение
with psycopg2.connect(database='based_database', user='postgres', password='Erfounder1!') as conn:
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phones;
        DROP TABLE client;
        """)

        create_table(cur)
        conn.commit()

        add_client(
            cur, '0',
            'Иван', 'Иванов', 'IvanIvanov@mail.ru',
            '+74356789009'
        )
        conn.commit()

        client_search(cur, name='Иван')

        add_client(
            cur, '1',
            'Алексей', 'Алексеев', 'AlexAlexeev@mail.ru',
            ['+78124566776', '+73146789559']
        )
        conn.commit()

        client_search(cur, email='AlexAlexeev@mail.ru')

        add_phone_to_client(cur, '1', '+73847984004')
        conn.commit()

        change_client_data(cur, '0', name='Кирилл', email='KirillIvanov@mail.ru')
        conn.commit()

        delete_phone(cur, '1', '+73146789559')
        conn.commit()

        client_search(cur, name='Кирилл')
        client_search(cur, name='Алексей')

        delete_client(cur, '0')
        delete_client(cur, '1')







