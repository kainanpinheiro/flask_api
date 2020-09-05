from dotenv import load_dotenv
import os


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")
DB_DB = os.getenv("DB_DB")


DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'\
    .format(user=DB_USER, pw=DB_PW, url=DB_HOST, db=DB_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = False
