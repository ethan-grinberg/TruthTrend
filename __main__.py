from src.zinfo.article_selector import get_summarized_news

API_KEY = 'eeeaefaae3c14737bc08e252a6e1991b'


def main():
    summarized_news = get_summarized_news(API_KEY)


if __name__ == "__main__":
    main()
