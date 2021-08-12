from src.zinfo.article_selector import get_summarized_news

API_KEY = '5964b2e875064a83a9033afc11f48101'


def main():
    summarized_news = get_summarized_news(API_KEY)


if __name__ == "__main__":
    main()
