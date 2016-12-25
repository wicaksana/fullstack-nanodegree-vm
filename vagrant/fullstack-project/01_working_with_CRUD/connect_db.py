import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey


def connect(user, password, db, host='localhost', port=5432):
    """returns a connection and a metadata object"""
    url = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, db)

    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


def create_table(con, meta):
    slams = Table('slams',
                  meta,
                  Column('name', String, primary_key=True),
                  Column('country', String))
    results = Table('results',
                    meta,
                    Column('slam', String, ForeignKey('slams.name')),
                    Column('year', Integer),
                    Column('result', String))

    meta.create_all(con)
    print("tables are created")


if __name__ == '__main__':
    con, meta = connect('postgres', 'postgres', 'postgres')

    for table in meta.tables:
        print(table)