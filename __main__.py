from src.zinfo.article_selector import get_summarized_news

API_KEY = 'debd522136164978a43f9815fe4dde7d'


def main():
    summarized_news = get_summarized_news(API_KEY)


if __name__ == "__main__":
    main()
