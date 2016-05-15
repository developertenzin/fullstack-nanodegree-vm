import sys

from sqlalchemy import
Column, Foreignkey, Interger, String

from sqlalchemy.ext.declarative import
declarative_base

from sqlalchemy.orm import relationsihp

from sqlalchemy import create_engine

Base = declarative_base()

######## insert at end of file #########


engine = create_engine('sqlite:///restaurantmenu.db')

