"""SELECT * from todos
velger alt fra todos databasen 
"""

"""SELECT "column" from todos
    SELCET "coulmn","description" from todos
    SELCET * FROM todos where title ="some shit"
     SELCET * FROM todos where title ="some shit"

     UPDATE todos SET complete=True where ID=5 
     setter complete true hvor ID =5
     DELETE from todos where ID=5 
"""


"""
skriver sqlite3 todos.db for å få kontakt med db

.schema 

navnet på databasen ikke filen i filepathen

insert into todo (title, description,priority,complete) values ("henge mer","film,ete drekke",5,0);
insert into todo (title, description,priority,complete,owner_id) values ("henge mer","film,ete drekke",5,0,1);

insert into todo (title, description,priority,complete,owner_id) values ("Trene","Sykle og lope langt",4,0,2);


delete from todo where id=4
update todo set complete =1 where id=3

.mode column

.mode box /table 


df.to_sql("tableName",engine,if_exists="append",index=false)
df.to_sql(newTable,engine)
pd.read_sql("tableName",engine) reads all 
pd.read_sql_query(SELCET * FROM todos)

drop table "name of table" 

uvicorn auth:app --reload --port 9000
pip install "passlib[bcrypt]" for cryptering


DROP TABLE IF EXISTS users 
CREATE TABLE users(
    id serial, email varchar(45) Default Null
    first_name varchar(200) default Null
    PRIMARY KEY (id)
)


DROP TABLE IF EXISTS todo 
CREATE TABLE todo(
    id serial, email varchar(45) Default Null
    first_name varchar(200) default Null
    , owner_ID integer default=Null
    PRIMARY KEY (id)
    FOREIGN KEY (owner_id) REFERENCE user(id)
)


DROP TABLE IF EXISTS users;

CREATE TABLE users (
	id SERIAL,
	Email varchar(200) DEFAULT NULL,
	username varchar(45) DEFAULT NUll,
	first_name varchar(45) DEFAULT NUll,
	last_name varchar(45) DEFAULT NUll,
	hashed_password varchar(200) DEFAULT NUll,
	is_active boolean DEFAULT NULL,
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS todo;

CREATE TABLE todo (
	id SERIAL,
	title varchar(200) DEFAULT NULL,
	description varchar(45) DEFAULT NUll,
	priority integer DEFAULT NUll,
	complete boolean DEFAULT NUll,
	owner_id integer DEFAULT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY (owner_id) REFERENCES users(id) 
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
	id SERIAL,
	Email varchar(200) DEFAULT NULL UNIQUE,
	username varchar(45) DEFAULT NUll UNIQUE,
	first_name varchar(45) DEFAULT NUll,
	last_name varchar(45) DEFAULT NUll,
	hashed_password varchar(200) DEFAULT NUll,
	is_active boolean DEFAULT NULL,
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS todo;

CREATE TABLE todo (
	id SERIAL,
	title varchar(200) DEFAULT NULL,
	description varchar(45) DEFAULT NUll,
	priority integer DEFAULT NUll,
	complete boolean DEFAULT NUll,
	owner_id integer DEFAULT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY (owner_id) REFERENCES users(id) 
);

ALEMBIC

alembic init <folderName>
alembic revision -m <message>
alembic upgrade <revision #> send revision uppgrade to database
alembic downgrade <revision #> send revision downgrade to database

lager da en ALEMBIC mappe, med en alembic ini file

alembic ini file change schlalchemy.url= postgres

inn almebic folder env, import sys, sys.path.append("..")
import models
config=context.config
fileConfig(config.config_file_name)
target_meta_data=models.Base.metdadata

alembic revision -m "createa phone number table" 

in alembic/version.
def upgrade:
	op.add_column("user",sa.Column("phone_number",sa.String(),nullable=True))

alembic upgrade versionID

def downgrade():
	op.drop_column("user","phone_number)

alembic downgrade -1 


alembic revision -m "create adress table" 



def upgrade():
	op.create_table("adress",sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
	sa.Column("adress1",sa.String(),nullable=False),
	sa.Column("adress2",sa.String(),nullable=False),
	sa.Column("city",sa.String(),nullable=False),
	sa.Column("country",sa.String(),nullable=False),
	sa.Column("postalcode",sa.String(),nullable=False)
	)



def downgrade():
	op.drop_table("adress")


alembic revision -m "add new user column for adress"

def uppgrade():
	op-add_column("users",sa.Column("adress_id",sa.Integer(),nullable=True))
	op.create_foreign_key("adress_user_fk",source_table="users",refrent_table="adress",
	local_cols=["adress_id"],remote_cols=["Id"],ondelete="CASCADE")

def downgrade():
	op.drop_constraint("adress_user_fk",table_name="users")
	op.drop_column("user","adress_id")


hvordan få database til å kun inneholde unieq verdier:
ALTER TABLE users ADD UNIQUE (email);
addes egt av seg selv  får feilrespons 500 hvis det ikke går, kan ta endre til en annen respons 

conda env create -f fastapi.yml.

conda create --name FastApiEnv python=3.9
conda install --file requirements.txt


Alter table users add unique (email);

pip install "passlib[bcrypt]"
pip install "python-jose[cryptography"]
pip install python-multipart
"""