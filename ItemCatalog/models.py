
# Imports related to database
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# Start of database creation

# Let the SqlAlchemy know, that this is our special
# classes corresponding to the table in the database
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(250), nullable=False, index=True)
    picture = Column(String(500))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    items = relationship("Item")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'Item': [item.serialize for item in self.items]
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    category = relationship(Category)
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'cat_id': self.category_id
        }


# It will create a new database
engine = create_engine('sqlite:///itemcatalog.db')

# Goes into the database and add the classes(Tables) in our database.
Base.metadata.create_all(engine)

# End of database creation
