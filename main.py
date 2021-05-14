import sys
from Event import Events
from Userfile import User, Admin, Costumer
import logger
from colorama import Fore


def main():
    menu()


def menu():

    print(Fore.BLUE + "*********Welcome to Online sales of tickets***********")

    print("""
                      A: Sign up
                      B: Login
                      Q: Quit

                    """)
    try:
        choice = input(Fore.CYAN + "Please Enter Choice number:")
        if choice == "A" or choice == "a":
            if User.register() == True:
                menu()
        elif choice == "B" or choice == "b":
            try:
                user_name, password = User.login()
                if user_name == 'Admin':
                    admin_menu(user_name, password)
                else:
                    user_menu(user_name, password)
            except TypeError:
                menu()
        elif choice == "Q" or choice == "q":
            sys.exit()
        else:
            raise TypeError

    except TypeError:
        print(Fore.LIGHTWHITE_EX)
        print("just choice A, B and Q")
        logger.my_logger.error('the choice of menu was entered incorrectly', exc_info=True)
        menu()


def admin_menu(user_name, password):
    admin = Admin(user_name, password)

    print(Fore.BLUE + "What do you like to do?")

    print("""
                      A: Add event
                      B: buy event's ticket
                      R: Report
                      C: change password
                      Q: Quit

                    """)
    try:
        choice = input(Fore.CYAN + "Please your Choice:")
        if choice == "A" or choice == "a":
            if Admin.add_event() == True:
                admin_menu(user_name, password)

        elif choice == 'B' or choice == 'b':
            user_menu(user_name, password)

        elif choice == 'C' or choice == 'c':
            admin.change_password()
            admin_menu(user_name, password)

        elif choice == 'R' or choice == 'r':
            print(Fore.LIGHTGREEN_EX)
            print(admin.report())
            back = False
            while back == False:
                back = input(Fore.LIGHTCYAN_EX + 'press Enter to back ')
            admin_menu(user_name, password)

        elif choice == "Q" or choice == "q":
            logger.user_logger.info(f'the User with name:{user_name} log out')
            menu()
        else:
            raise TypeError

    except TypeError:
        print(Fore.LIGHTWHITE_EX)
        print("just choice A, B, R, C and Q")
        logger.my_logger.error('the choice of menu was entered incorrectly', exc_info=True)
        admin_menu(user_name, password)


def user_menu(user_name, password):
    costumer = Costumer(user_name, password)

    print(Fore.BLUE + "What do you like to do?")

    print("""
                      A: view the list of events
                      C: change password
                      Q: Quit

                    """)
    try:
        choice = input(Fore.CYAN + "Please your Choice:")

        if choice == 'A' or choice == 'a':
            print(Fore.LIGHTGREEN_EX)
            print(Costumer.view_events())
            answer = input(Fore.LIGHTCYAN_EX + "Do you like to buy ticket Y/N?")
            if answer == 'Y' or answer == 'y':
                code_event = input("Enter 'code' of event for buy it :")
                try:
                    count_ticket = int(input('How many ticket do you want?'))
                    assert count_ticket > 0
                except ValueError:
                    print(Fore.RED + 'Error! must choice Integers')
                    logger.my_logger.error('value error occurred ', exc_info=True)
                    user_menu(user_name, password)
                except AssertionError:
                    print(Fore.RED + 'entered value is incorrect,try again')
                    logger.my_logger.error('entered value was 0 or negative number', exc_info=True)
                    user_menu(user_name, password)

                if costumer.buy_request(code_event, count_ticket) == False:
                    user_menu(user_name, password)
                else:
                    code_event, event_name, date, place, capacity, place = costumer.buy_request(code_event, count_ticket)
                    obj_buy = Events(code_event, event_name, date, place, capacity, place)

                    answer = input('Do you have any discount code Y/N? ')
                    if answer == 'Y' or answer == 'y':
                        user_discount = input('Enter discount code :')
                        if costumer.discount(user_discount) == False:
                            print(Fore.RED + ' this discount code is not valid please try again ')
                            user_menu(user_name, password)
                        else:
                            role, discount_percent = costumer.discount(user_discount)
                            discount_cost = obj_buy.calculate_discount(role, discount_percent, count_ticket)
                    elif answer == 'N' or answer == 'n':
                        discount_percent = 0
                        role = "user"
                        discount_cost = obj_buy.calculate_discount(role, discount_percent, count_ticket)
                    else:
                        print(Fore.WHITE + "your code discount is not available")
                        discount_percent = 0
                        role = "user"
                        discount_cost = obj_buy.calculate_discount(role, discount_percent, count_ticket)
                    answer = input(Fore.LIGHTCYAN_EX + 'Are you sure for buy tickets Y/N ?')
                    if answer == 'Y' or answer == 'y':
                        costumer.payment(discount_cost)
                        obj_buy.display_buy(count_ticket, discount_cost)
                        obj_buy.update(count_ticket)
                        if user_name == 'Admin':
                            admin_menu(user_name, password)
                        else:
                            user_menu(user_name, password)

                    elif answer == 'N' or answer == 'n':
                        user_menu(user_name, password)

            elif answer == 'N' or answer == 'n':
                user_menu(user_name, password)
            else:
                print(Fore.LIGHTWHITE_EX + "just press Y or N")
                user_menu(user_name, password)

        elif choice == 'C' or choice == 'c':
            costumer.change_password()
            user_menu(user_name, password)

        elif choice == "Q" or choice == "q":
            if user_name == 'Admin':
                admin_menu(user_name, password)
            else:
                logger.user_logger.info(f'the User with name:{user_name} log out')
                menu()
        else:
            raise TypeError

    except TypeError:
        print(Fore.LIGHTWHITE_EX)
        print("just choice A, C and Q")
        logger.my_logger.error('the choice of menu was entered incorrectly', exc_info=True)
        user_menu(user_name, password)


menu()
