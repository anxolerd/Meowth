from sqlalchemy import Column, Integer, String, Text, ForeignKey
from project.database import Base, get_db


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    short_description = Column(String(300))
    text = Column(Text())
    category_id = Column(Integer, ForeignKey('category.id'))
    name_in_url = Column(String(50))
    visits = Column(Integer)
    salary = Column(String(50))
    description = Column(String(200)) #for search spider
    keywords = Column(String(1000))

    def __init__(self, title, short_description, text, category_id,
                 name_in_url, description=None,
                 keywords=None, salary=None,  visits = 0):
        self.title = title
        self.short_description = short_description
        self.text = text
        self.category_id = category_id
        self.name_in_url = name_in_url
        self.visits = visits
        self.salary = salary
        self.description = description
        self.keywords = keywords
        self.save()

    def __repr__(self):
        return self.title

    def save(self):
        db = get_db()
        db.add(self)
        db.commit()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name
        self.save()

    def save(self):
        db = get_db()
        db.add(self)
        db.commit()
