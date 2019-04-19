import dataset
from sqlalchemy.exc import IntegrityError
import mvc_exceptions as mvc_exc


DB_name = ':memory:'


def create_table(conn, table_name):
    conn.get_table(table_name, primary_id='name', primary_type=conn.types.text)

#    try:
#        conn.load_table(table_name)
#    except Exception as e:
#        print('Table {} does not exist. It will be created now'.format(e))
#        conn.get_table(table_name, primary_id='name', primary_type=conn.types.text)
#        print('Created table {} on database {}'.format(table_name, DB_name))


def insert_one(conn, name, price, quantity, table_name):
    table = conn.load_table(table_name)
    try:
        table.insert(dict(name=name, price=price, quantity=quantity))
    except IntegrityError as e:
        raise mvc_exc.ItemAlreadyStored(
            '"{}" already stored in table "{}".\nOriginal Exception raised: {}'
            .format(name, table.name, e))


def insert_many(conn, items, table_name):
#    table = conn.load_table(table_name)
#    try:
#        table.insert_many(items)
#    except Exception as e:
#        print(e)

    for x in items:
        try:
            insert_one(conn, x['name'], x['price'], x['quantity'], table_name)
        except mvc_exc.ItemAlreadyStored as e:
            print(e)


def select_one(conn, name, table_name):
    table = conn.load_table(table_name)
    row = table.find_one(name=name)
    if row is not None:
        return dict(row)
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored in table "{}"'.format(name, table.name))


def select_all(conn, table_name):
    table = conn.load_table(table_name)
    rows = table.all()
    return list(map(lambda x: dict(x), rows))


def update_one(conn, name, price, quantity, table_name):
    table = conn.load_table(table_name)
    row = table.find_one(name=name)
    if row is not None:
        item = {'name': name, 'price': price, 'quantity': quantity}
        table.update(item, keys=['name'])
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t update "{}" because it\'s not stored in table "{}"'.format(name, table.name))


def delete_one(conn, item_name, table_name):
    table = conn.load_table(table_name)
    row = table.find_one(name=item_name)
    if row is not None:
        table.delete(name=item_name)
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t delete "{}" because it\'s not stored in table "{}"'.format(item_name, table.name))


def main():
    conn = dataset.connect('sqlite:///{}'.format(DB_name))

    table_name = 'items'
    create_table(conn, table_name)

    my_items = [
        {'name': 'bread', 'price': 0.5, 'quantity': 20},
        {'name': 'bread', 'price': 0.5, 'quantity': 20},
        {'name': 'milk', 'price': 1.0, 'quantity': 10},
        {'name': 'wine', 'price': 10.0, 'quantity': 5},
    ]

    # CREATE
    insert_many(conn, items=my_items, table_name=table_name)
    insert_one(conn, 'beer', price=2.0, quantity=5, table_name=table_name)

    # READ
    print('SELECT milk')
    print(select_one(conn, 'milk', table_name=table_name))
    print('SELECT all')
    print(select_all(conn, table_name=table_name))

    # UPDATE
    print('UPDATE bread, SELECT bread')
    update_one(conn, 'bread', price=1.5, quantity=5, table_name=table_name)
    print(select_one(conn, 'bread', table_name=table_name))

    # DELETE
    print('DELETE beer, SELECT all')
    delete_one(conn, 'beer', table_name=table_name)
    print(select_all(conn, table_name=table_name))


if __name__ == '__main__':
    main()
