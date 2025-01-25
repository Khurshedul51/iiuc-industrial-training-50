import datetime
from requests_html import HTMLSession
from .database import SessionLocal
from .crud import create_news
from .schemas import NewsCreate, News

def single_news_scraper(url: str):
    session = HTMLSession()
    try:
        response = session.get(url)
        # print('response', response)
        # response.html.render()  # This will download Chromium if not found
        # print('13 line')
        publisher_website = url.split('/')[2]
        publisher = publisher_website.split('.')[1]
        title = response.html.find('h1')[0].text
        reporter = response.html.find('div.byline')[0].text
        datetime_string = response.html.find('.date', first=True).text.splitlines()[0]
        date_format = "%a %b %d, %Y %I:%M %p"
        # Convert string to datetime object
        news_datetime = datetime.datetime.strptime(datetime_string, date_format)
        category = response.html.find('.category > a', first=True).text
        content = '\n'.join([p.text for p in response.html.find('div.clearfix > p')])
        img_tags = response.html.find('img.lazyloaded')
        # print(img_tags)
        images = [img.attrs['srcset'] for img in img_tags]
        # news_datetime = datetime.datetime.now()

        print(f"Scraped news from {url}")
        print(f"Title: {title}")
        print(f"Reporter: {reporter}")
        print(f"Date: {news_datetime}")
        print(f"Category: {category}")
        print(f"Images: {images}")


        return NewsCreate(
            # publisher_website=publisher_website,
            news_author=publisher,
            title=title,
            news_editor=reporter,
            datetime=news_datetime,
            link=url,
            news_category=category,
            body=content,
            images=images,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def scrape_and_store_news(url: str, db: SessionLocal):
    # db = SessionLocal()
    news_data = single_news_scraper(url)
    print(news_data)
    inserted_news = ""
    if news_data:
        # print(news_data)
        inserted_news = create_news(db=db, news=news_data)
    db.close()

    return inserted_news

