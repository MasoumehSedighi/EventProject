import csv
import hashlib
import pandas as pd
import logger
from Event import Events
from colorama import Fore


class User:
    """this class have some functions for all type of user that use from application such as
    register,login,change password,buy request for events,do payment and discount"""

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    @staticmethod
    def login():

        """
        the function gets username and password from user if user name and password
        was correct login else user name or passwords were wrong show different messages
         and user can just three times for try to enter correct info"""
        try:
            i = 0
            while i < 3:

                user_name = input(Fore.LIGHTCYAN_EX+"Please enter your username:")
                password = input(Fore.LIGHTCYAN_EX+"Please enter your password:")
                hash_password = hashlib.sha256(str(password).encode('utf8')).hexdigest()
                with open('info-user.csv', 'r') as change_file:
                    csv_reader = csv.DictReader(change_file)
                    for row in csv_reader:
                        if row['user_name'] == user_name and row['password'] == hash_password:
                            print(Fore.LIGHTMAGENTA_EX+"Welcome Back, " + user_name)
                            logger.user_logger.info(f'the User with name:{user_name}'
                                                    f' has been logged in')
                            return user_name, password

                    else:
                        print(Fore.RED+" user name or Password entered is wrong")
                        i += 1

            print(Fore.LIGHTRED_EX+"Warning! Username and password entered three times incorrectly"
                                   ", please contact with Admin.")
            logger.my_logger.error('Username and password entered three times incorrectly')

        except FileNotFoundError:
            print(Fore.RED+'File users is not found')
            logger.my_logger.error('file not found', exc_info=True)

    @staticmethod
    def register():

        """ the function gets username and password from new customer if the user was exists
            show error to customer else register and add to customer file"""

        file_path = "info-user.csv"
        account = pd.read_csv(file_path)
        lst_username = list(account["user_name"])
        user_name = input(Fore.LIGHTCYAN_EX+"Please enter a username:")
        while len(user_name) == 0:
            user_name = input("Please enter a username:")
        while user_name in lst_username:
            print(Fore.LIGHTYELLOW_EX+'--This name has already been registered--')
            user_name = input(Fore.LIGHTCYAN_EX+"! Please enter a username:")
        password = input("Please enter a password:")
        while len(password) == 0:
            password = input("Please enter a password:")
        hash_password = hashlib.sha256(str(password).encode('utf8')).hexdigest()
        obj_user = User(user_name, hash_password)

        row_account = [[obj_user.user_name, obj_user.password]]
        with open(file_path, 'a', newline='') as csv_account:
            csv_writer = csv.writer(csv_account)
            csv_writer.writerows(row_account)
            print(Fore.LIGHTMAGENTA_EX+'**Your account has been successfully registered**')
            logger.user_logger.info(f'the User with name:{user_name}'
                                    f' has been registered')
            return True

    def change_password(self):
        """ this method take user name, current password and new password and change password also
         update info_user file"""

        change = pd.read_csv('info-user.csv')
        location = 0
        user_name = input(Fore.LIGHTCYAN_EX+"Please enter your username:")
        while len(user_name) == 0:
            user_name = input(" Please enter your username:")

        old_password = input("Please enter current password:")
        while len(old_password) == 0:
            old_password = input(" Please enter current password:")

        new_password = input("Please enter your new password:")
        while len(new_password) == 0:
            new_password = input(" Please enter your new password:")
        hash_oldpassword = hashlib.sha256(str(old_password).encode('utf8')).hexdigest()
        hash_newpassword = hashlib.sha256(str(new_password).encode('utf8')).hexdigest()

        with open('info-user.csv', 'r') as change_file:
            csv_reader = csv.DictReader(change_file)
            for row in csv_reader:
                if row['user_name'] == self.user_name and row['password'] == hash_oldpassword:
                    self.password = hash_newpassword
                    print(Fore.LIGHTMAGENTA_EX+"Your password is changed.")
                    change.loc[location, 'password'] = hash_newpassword
                    change.to_csv('info-user.csv', index=False)
                    logger.user_logger.info(f'the User with name:{self.user_name}'
                                            f' changed password')
                location += 1

    def buy_request(self, code_event, count_ticket):
        """ this method take code event and number of ticket that costumer want to buy check code event
        and event capacity if is correct return information about selected event """
        try:
            with open('info_event.csv', 'r') as event_file:
                event_reader = csv.DictReader(event_file)
                for line in event_reader:
                    if line['code_event'] == code_event:
                        if int(line['capacity']) != 0 and int(line['capacity']) >= count_ticket:
                            return line['code_event'], line['event_name'], line['date'], \
                                line['place'], line['capacity'], line['cost']
                else:
                    print(Fore.RED+f"Dear * {self.user_name} * this code is not available or capacity is full ! check again")
                    return False
        except FileNotFoundError:
            logger.my_logger.error('file not found', exc_info=True)

    def discount(self, code_discount):
        """this method take discount code from costumer check it in code_discount file if is correct
        return role of costumer and amount of discount percent"""

        with open('code_discount.csv', 'r') as discount_file:
            csv_reader = csv.DictReader(discount_file)
            for line in csv_reader:
                if line['code'] == code_discount:
                    return line['role'], line['discount']
            else:
                return False

    def payment(self, final_cost):
        """this method enter to system bank for paid"""
        print(Fore.LIGHTMAGENTA_EX)
        print("Welcome to Bank payment")
        print(final_cost, '$ paid successfully ')


class Admin(User):

    """this class has three attribute such as user_name,password and role of admin user, Admin can
    add events to info_event file and review tickets sold and Remaining tickets"""

    def __init__(self, user_name, password, role='Admin'):
        super().__init__(user_name, password)
        self.role = role

    @staticmethod
    def add_event():
        """this method allow to Admin add new events"""

        file_path = "info_event.csv"
        events = pd.read_csv(file_path)
        lst_event = list(events["code_event"])

        code_event = input(Fore.LIGHTCYAN_EX+"Please enter a code's event:")
        while len(code_event) == 0:
            code_event = input("Please enter a code's event:")
        while code_event in lst_event:
            print(Fore.LIGHTYELLOW_EX+"--This code's event has been recorded--")
            code_event = input(Fore.LIGHTCYAN_EX+"! Please enter a code's event:")
        event_name = input("Please enter an event:")
        while len(event_name) == 0:
            event_name = input("Please enter an event:")
        date = input("Please enter an event's date(m/d/y):")
        while len(date) == 0:
            date = input("Please enter an event's date(m/d/y):")
        place = input("Please enter an event's place:")
        while len(place) == 0:
            place = input("Please an event's place:")
        capacity = input("Please enter an event's capacity:")
        while len(capacity) == 0:
            capacity = input("Please an event's capacity:")
        cost = input("Please enter an event's cost:")
        while len(cost) == 0:
            cost = input("Please an event's cost:")

        obj_event = Events(code_event, event_name, date, place, capacity, cost, sales=0)

        row_event = [[obj_event.code_event, obj_event.event_name, obj_event.date,
                      obj_event.place, obj_event.capacity, obj_event.cost, obj_event.sales]]

        logger.info_logger.info(f'Event with code:{obj_event.event_name} and name:{obj_event.event_name} is created')

        with open(file_path, 'a', newline='') as csv_events:
            csv_writer = csv.writer(csv_events)
            csv_writer.writerows(row_event)
            print(Fore.LIGHTMAGENTA_EX+'**Event has been successfully recorded**')
            return True

    @staticmethod
    def report():
        """this method show remaining capacity and sold ticket to Admin"""
        try:
            events = pd.read_csv('info_event.csv', index_col='code_event')
            df = events.iloc[:, [0, 3, 5]]
            return df

        except FileNotFoundError:
            print(Fore.RED + 'File events not found')
            logger.my_logger.error('file not found', exc_info=True)
            exit(1)


class Costumer(User):
    """this class is for all of users that want to do functions such as costumer """

    def __init__(self, user_name, password, role='costumer'):
        super().__init__(user_name, password)
        self.role = role

    @staticmethod
    def view_events():
        """this methods show list of events"""
        while True:
            try:
                events = pd.read_csv('info_event.csv', index_col='code_event')
                df = events.iloc[:, [0, 1, 2, 3, 4]]
                return df
            except FileNotFoundError:
                print(Fore.RED+'File events not found')
                logger.my_logger.error('file not found', exc_info=True)
                exit(1)


