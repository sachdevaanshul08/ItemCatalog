from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Delete everything
session.query(Category).delete()
print "Category data deleted"
session.query(Item).delete()
print "Item data deleted"

session.commit()


user1 = User(name="Anshul Sachdeva", email="anshul_sachdeva@yahoo.com",
             picture='''https://www.pexels.com
             /photo/adorable-animal-breed-canine-356378/''')
session.add(user1)
session.commit()


# Insert data here
category1 = Category(name="Soccer")
session.add(category1)

item1 = Item(title="Football", description="football description",
             category=category1, user=user1)
session.add(item1)

item2 = Item(title="shoes", description="shoes description",
             category=category1, user=user1)
session.add(item2)

item3 = Item(title="Jersey", description="Jersey description",
             category=category1, user=user1)
session.add(item3)

session.commit()


# 2nd Category
category2 = Category(name="Snowboarding")
session.add(category2)

item1 = Item(title="Goggles", description="Goggles description",
             category=category2, user=user1)
session.add(item1)

item2 = Item(title="Snowboard", description="Snowboard description",
             category=category2, user=user1)
session.add(item2)

session.commit()

# 3rd Category
category3 = Category(name="Baseball")
session.add(category3)

item1 = Item(title="Bat", description="Bat description",
             category=category3, user=user1)
session.add(item1)

item2 = Item(title="Ball", description="Ball description",
             category=category3, user=user1)
session.add(item2)

session.commit()

# 4th Category
category4 = Category(name="Hockey")
session.add(category4)

item1 = Item(title="Hockey Stick", description="Stick description",
             category=category4, user=user1)
session.add(item1)

item2 = Item(title="Hockey ball", description="Ball description",
             category=category4, user=user1)
session.add(item2)

session.commit()

# 5th Category
category5 = Category(name="Skating")
session.add(category5)

item1 = Item(title="Skate", description="Skate description",
             category=category5, user=user1)
session.add(item1)

item2 = Item(title="Skate shoes", description="shoes description",
             category=category5, user=user1)
session.add(item2)

session.commit()

print "added items!"
