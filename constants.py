import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
API_USER = os.getenv('API_USER')
API_PASS = os.getenv('API_PASS')
BASE_URL = 'http://stub.2xt.com.br/air'
