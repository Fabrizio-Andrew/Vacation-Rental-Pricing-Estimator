from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData
db_string = "postgresql://whrrmvflhmdcnm:491f478d709408d4096823526a71594df29cda7bda7b84e24bb1af80513fb740@ec2-23-23-133-10.compute-1.amazonaws.com:5432/dcrrjn77esq9ru"

db = create_engine(db_string)

meta = MetaData(db)
user_table = Table('users', meta,  
                       Column('uid', String, autoincrement=True),
                       Column('email', String, primary_key=True, nullable=False, ),
                       Column('password', String, nullable=False))
# create table users (
# uid serial NOT NULL PRIMARY KEY,
# email TEXT NOT NULL UNIQUE,
# password TEXT NOT NULL);


with db.connect() as conn:

    # Create
    user_table.create()
    insert_statement = user_table.insert().values(email="test@gmail.com", password="testhaha")
    conn.execute(insert_statement)

    # # Read
    # select_statement = user_table.select()
    # result_set = conn.execute(select_statement)
    # for r in result_set:
    #     print(r)

    # # Update
    # update_statement = user_table.update().where(user_table.c.year=="2016").values(title = "Some2016Film")
    # conn.execute(update_statement)

    # # Delete
    # delete_statement = user_table.delete().where(user_table.c.year == "2016")
    # conn.execute(delete_statement)