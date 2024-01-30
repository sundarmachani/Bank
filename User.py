import logging
from datetime import datetime
import Database


class User:
    USER = "USER"
    dateFormatter = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

    def __init__(self, name, age, phone, email, address, city, state, pincode, country):
        self.name = name
        self.age = age
        self.phone = phone
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.pincode = pincode
        self.country = country
        self.type = User.USER
        self.created_at = User.dateFormatter


def getUser(email):
    user = Database.userDataFinder(email, User.USER)
    if user:
        return user
    else:
        logging.info("No data Found with email")
        return None


def createUser(user):
    print(user.email)
    matched_user = getUser(user.email)
    if matched_user:
        logging.error("User already created")
        raise ValueError("User already created")
    else:
        new_user = User(user.name, user.age, user.phone, user.email, user.address, user.city, user.state, user.pincode,
                        user.country)
        Database.add(new_user.__dict__, None)


def deleteUser(email):
    is_deleted = Database.deleteUser(email, User.USER)
    if is_deleted:
        return True


def getAllUsers():
    users = Database.getUsers()
    if users:
        return users
