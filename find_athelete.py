"""
NOTE: To use this script, you must first execute users.py to write data to the database
"""
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Directory may be different
DB_PATH = "sqlite:///sochi_atheletes.sqlite3"
Base = declarative_base()


class Athelete(Base):
    """
    Describes the structure of the Athlete Table containing data about the Athletes
    """
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


class User(Base):
    """
    Describes the structure of the user table containing data about users
    """
    __tablename__ = 'user'

    id = sa.Column(sa.String(36), primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


def connect_db():
    """
    Establishes a connection to the database, 
    creates tables if they do not already exist, 
    and returns a session object
    """

    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    """
    Asks the user for data and adds it to the users list
    """
    print("Let's look for athletes similar to one of the users.")
    user_id = input("Enter user ID: ")
    return int(user_id)


def convert_str_to_date(date_str):
    """
    Converts a date string in the YYYY-MM-HH format to a datetime.date object
    """
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date


def nearest_by_bd(user, session):
    """
    Finds the closest athlete by date of birth to user
    """
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = convert_str_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd
    
    user_bd = convert_str_to_date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd
    
    return athlete_id, athlete_bd


def nearest_by_height(user, session):
    """
    Finds the closest athlete to user
    """
    athletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height
    
    return athlete_id, athlete_height


def main():
    """
    Carries out user interaction, processes user input
    """
    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("No such user was found.")
    else:
        bd_athlete, bd = nearest_by_bd(user, session)
        height_athlete, height = nearest_by_height(user, session)
        print(
            "Closest athlete by date of birth: {}, his date of birth: {}".format(bd_athlete, bd)
        )
        print(
            "Nearest athlete: {}, his height: {}".format(height_athlete, height)
        )


if __name__ == "__main__":
    main()
