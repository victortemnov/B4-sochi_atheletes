import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# NOTE: Directory may be different
DB_PATH = "sqlite:///sochi_atheletes.sqlite3"
Base = declarative_base()


class User(Base):
    """
    Describes the structure of the athelete table containing data about athletes
    """
    __tablename__ = 'user'

    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.FLOAT)


def connect_db():
    """
    Establishes a connection to the database, creates tables if they do not already exist, and returns a session object
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    """
    Asks the user for data and adds it to the users list
    """
    print("Hello! I'll record your data!")
    first_name = input("Please enter your name: ")
    last_name = input("And now the surname: ")
    gender = input("What's your gender? (options: Male, Female): ")
    email = input("I still need your email address: ")    
    birthdate = input("Please enter your date of birth in the format YYYY-MM-DD. for example, 1990-01-01: ")
    height = input("What is your height in meters? (Use dot to separate decimal parts): ")
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height,
    )
    return user

def main():
    """
    Carries out user interaction, processes user input
    """
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Your data is saved in the database. Thanks!")


if __name__ == "__main__":
    main()
