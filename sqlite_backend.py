import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgramingError


DB_name = 'myDB'


def connect_to_db(db=None):
    if db is None:
        mydb = ':memory:'
        print('New connection to in-memory SQLite DB...')
    else:
        mydb = '{}.db'.format(db)
        print('New connection to SQLite DB...')
    connection = sqlite3.connect(mydb)
    return connection


def connect(func):
    """Docorator to (re)open a sqlite database connection when needed.

    Parameters
    ----------
    func : function
        function which performs the database query
    
    Returns
    -------
    inner func : function
    """
    def inner_func(conn, *args, **kwargs):
        try:
            conn.execute(
                'SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgramingError):
            conn = connect_to_db(DB_name)
        return func(conn, *args, **kwargs)
    return inner_func


def disconnect_from_db(db=None, conn=None):
    if db is not DB_name:
        print("You ar trying to disconnect from a wrong DB")
    if conn is not None:
        conn.close()


@connect
def create_table(conn, table_name):
    table_name = scrub(table_name)
    sql = 'CREATE TABLE {} (rowid INTEGER PRIMARY KEY AUTOINCREMENT,' \
        'name TEXT UNIQUE, price REAL, quantity INTEGER)'.format(table_name)
    try:
        conn.execute(sql)
    except OperationalError as e:
        print(e)


def scrub(input_string):
    """Clean an input string (to prevent SQL injection)

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return ''.join(k for k in input_string if k.isalnum())


@connect
def insert_one(conn, name, price, quantity, table_name):
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('name', 'price', 'quantity') VALUES (?, ?, ?)"\
        .format(table_name)
    try:
        conn.execute(sql, (name, price, quantity))
        conn.commit()
    except IntegrityError as e:
        raise mvc_exc.ItemAlreadyStored(
            '{}: "{}" already stored in table "{}"'.format(e, name, table_name))


@connect
def insert_many(conn, items, table_name):
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('name', 'price', 'quantity') VALUES (?, ?, ?)"\
        .format(table_name)
    entries = list()
    for x in items:
        entries.append((x['name'], x['price'], x['quantity']))
    try:
        conn.executemany(sql, entries)
        conn.commit()
    except IntegrityError as e:
        print('{}: at least one in {} was already stored in table "{}"'
            .format(e, [x['name'] for x in items], table_name))
