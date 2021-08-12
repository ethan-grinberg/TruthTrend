from src.zinfo.article_selector import get_summarized_news

API_KEY = 'f2ba8eba75d54f0280ac77382f7810df'


def main():
    summarized_news = get_summarized_news(API_KEY)


if __name__ == "__main__":
    main()
