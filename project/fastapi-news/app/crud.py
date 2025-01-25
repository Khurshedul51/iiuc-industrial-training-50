from sqlalchemy.orm import Session
from . import models, schemas

def get_news(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()

def get_news_list(db: Session, skip: int = 0, limit: int = 10):
    print(db, skip, limit)
    return db.query(models.News).order_by(models.News.datetime.desc()).offset(skip).limit(limit).all()


def get_or_create_category(db: Session, name: str, description: str):
    # print(db, name, description)
    category = db.query(models.Category).filter(models.Category.name == name).first()
    # print("DB Response: ", category)
    if category is None:
        category = models.Category(name=name, description=description)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category

def get_or_create_reporter(db: Session, name: str, email: str):
    reporter = db.query(models.Editor).filter(models.Editor.name == name).first()
    if reporter is None:
        reporter = models.Editor(name=name, email=email)
        db.add(reporter)
        db.commit()
        db.refresh(reporter)
    return reporter

def get_or_create_publisher(db: Session, name: str):
    publisher = db.query(models.Author).filter(models.Author.name == name).first()
    if publisher is None:
        publisher = models.Author(name=name, email="dailystar@gmail.com")
        db.add(publisher)
        db.commit()
        db.refresh(publisher)
    return publisher


def get_news_existance(db: Session, news_title: str):
    return db.query(models.News).filter(models.News.title == news_title).first()


def create_image(db: Session, news_id: int, url: str):
    db_image = models.Image(news_id=news_id, url=url)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def create_news(db: Session, news: schemas.NewsCreate):
    category = get_or_create_category(db, news.news_category, f"{news.news_category} description")
    editor = get_or_create_reporter(db, news.news_editor, f"{news.news_editor}@example.com")
    author = get_or_create_publisher(db, news.news_author)
    news_exist = get_news_existance(db, news_title=news.title)

    print(category.name, editor.name, author.name)
    if news_exist:
        return news_exist

    db_news = models.News(
        # publisher_website=news.publisher_website,
        title=news.title,
        datetime=news.datetime,
        body=news.body,
        link = news.link,
        category_id=category.id,
        editor_id=editor.id,
        author_id=author.id
    )
    print(db_news)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)

    for image_url in news.images:
        create_image(db, news_id=db_news.id, url=image_url)

    return db_news


def insert_summary(db: Session, news_id: int, summary_text: str):
    db_summary = models.Summary(news_id=news_id, summary_text=summary_text)
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary


def get_summary(db: Session, summary_id: int):
    return db.query(models.Summary).filter(models.Summary.id == summary_id).first()