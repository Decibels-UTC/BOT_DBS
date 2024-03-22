# Pour le rename et recap script on a besoin 
# d'une database, seulement si le script est 
# lancé sans avoir crée les bonnes tables alors 
# le script va plant donc ce fichier permet d'éviter ça 
import pymysql as MySQLdb
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

db = MySQLdb.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"],
)

def init_user_rename():
    global db
    cursor = db.cursor()
    query = "CREATE TABLE IF NOT EXISTS user_rename(id INTEGER AUTO_INCREMENT PRIMARY KEY,member_id BIGINT NOT NULL,original_username VARCHAR(250) NOT NULL,guild_id BIGINT NOT NULL,date DATETIME NOT NULL);"
    cursor.execute(query)
    db.commit()



def init_excluded():
    global db
    cursor = db.cursor()
    query = "CREATE TABLE IF NOT EXISTS excluded(id INTEGER AUTO_INCREMENT PRIMARY KEY,member_id BIGINT NOT NULL,creation_date DATETIME NOT NULL);"
    cursor.execute(query)
    db.commit()


def init_reminders():
    global db
    cursor = db.cursor()
    query = "CREATE TABLE IF NOT EXISTS reminders(id INTEGER AUTO_INCREMENT PRIMARY KEY,guild BIGINT NOT NULL,title VARCHAR(250) NOT NULL,date DATETIME NOT NULL,date_ajout DATETIME NOT NULL);"
    cursor.execute(query)
    db.commit()


def init_database():
    init_user_rename();
    init_excluded();
    init_reminders();

init_database();