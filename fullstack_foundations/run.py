from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
#from database_setup import Restaurant, Base, MenuItem
#engine = create_engine('sqlite:///restaurantmenu.db')
from animal_shelter import Shelter, Puppy, Base
engine = create_engine('sqlite:///puppyshelter.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the
# last commit by calling
# session.rollback()
session = DBSession()

#print(session.query(MenuItem).all())
#database = session.query(MenuItem).all()

all_puppies = session.query(Puppy).all()

acs_pups = session.query(Puppy).order_by(Puppy.name.asc())

current_time = datetime.datetime.utcnow()
six_months_ago = current_time - datetime.timedelta(weeks=26)

infants = session.query(Puppy).filter_by(Puppy.dateOfBirth > six_months_ago).all()






#for item in database:
#    print(item.name, item.id)



