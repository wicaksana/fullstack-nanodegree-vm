from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Numeric, asc, func
from sqlalchemy.sql import label
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Puppy, Shelter


DB_FILE = 'sqlite:///puppyshelter.db'

def create_session():
    engine = create_engine(DB_FILE)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    return session

def query_all_puppies_and_return_in_ascending_order(session):
    """Queries all of the puppies and return the results in ascending alphabetical order"""
    puppies = session.query(Puppy).order_by(asc(Puppy.name))
    for puppy in puppies:
        print '{} in {}'.format(puppy.name, puppy.shelter.name)
    print '\n'

def query_all_puppies_younger_than_6_months(session):
    """Queries all puppies younger than 6 months and sort by the youngest first"""
    six_months = datetime.now().date() - timedelta(days = 6 * 30)
    puppies = session.query(Puppy).filter(Puppy.dateOfBirth > six_months).order_by(Puppy.dateOfBirth.desc())
    for puppy in puppies:
        print '{}: {}'.format(puppy.name, puppy.dateOfBirth)
    print '\n'

def query_all_puppies_by_ascending_weight(session):
    """Queries all puppies by ascending weight"""
    puppies = session.query(Puppy).order_by(asc(Puppy.weight))
    for puppy in puppies:
        print '{0}: {1:.2f} kg'.format(puppy.name, puppy.weight)
    print '\n'

def query_all_puppies_grouped_by_shelter(session):
    """Queries all puppies and group them based on their shelters"""
    puppies = session.query(label('total', func.count(Puppy.id)),
                            label('shelter_id', Puppy.shelter_id)).group_by(Puppy.shelter_id).all()
    for puppy in puppies:
        print 'There are {} puppies in {}'.format(puppy.total,
                                                  session.query(Shelter).filter(Shelter.id == puppy.shelter_id).first().name)

    print '\n'

if __name__ == '__main__':
    session = create_session()
    query_all_puppies_and_return_in_ascending_order(session)
    query_all_puppies_younger_than_6_months(session)
    query_all_puppies_by_ascending_weight(session)
    query_all_puppies_grouped_by_shelter(session)
