from src.zinfo.article_selector import get_summarized_news

API_KEY = '0e4a954687f342dba8cf1219706f7ff9'


def main():
    summarized_news = get_summarized_news(API_KEY)


if __name__ == "__main__":
    main()
