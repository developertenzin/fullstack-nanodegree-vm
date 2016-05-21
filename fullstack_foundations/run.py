from sqlalchemy import create_engine, func
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

# 1: Puppies ordered alphabetically
acs_pups = session.query(Puppy).order_by(Puppy.name.asc()).all()

# 2: Puppies younger than six months ordered by birthdate
current_time = datetime.datetime.utcnow()
six_months_ago = current_time - datetime.timedelta(weeks=26)
infants = session.query(Puppy).filter(Puppy.dateOfBirth < six_months_ago).order_by(Puppy.dateOfBirth.asc()).all()

# 3: Puppies ordered by weight
puppies_by_weight = session.query(Puppy).order_by(Puppy.weight.asc()).all()

# 4: Puppies grouped by their shelters
puppies_by_shelterID = session.query(Puppy).group_by(Puppy.shelter_id).all()
puppies_by_shelterID2 = session.query(func.count(Puppy.name)).group_by(Puppy.shelter_id).all()
for i in puppies_by_shelterID2:
    print(i)
