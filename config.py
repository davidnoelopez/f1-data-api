from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DEBUG = True
    PORT = 5000

    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_URL = os.getenv('MONGO_URL')
    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    MONGO_PORT = os.getenv('MONGO_PORT')
    MONGO_USERNAME = os.getenv('MONGO_USERNAME')
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')






