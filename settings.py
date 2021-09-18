from dotenv import load_dotenv
import os
load_dotenv("keys.env")

APIKEY = os.environ.get("APIKEY")
APISECRETKEY = os.environ.get("APISECRETKEY")
ACCESSTOKEN = os.environ.get("ACCESSTOKEN")
ACCESSTOKENSECRET = os.environ.get("ACCESSTOKENSECRET")

news_keys = os.environ.get("NEWSAPI")
news_keys = news_keys.split(",")
