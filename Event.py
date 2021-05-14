import csv
import pandas as pd
from colorama import Fore
import logger


class Events:
    """this class is for events that consist of some attributes about events such as code,name,date
    place, capacity and ticket sales"""

    def __init__(self, code_event, event_name, date, place, capacity, cost, sales=0):
        self.code_event = code_event
        self.date = date
        self.place = place
        self.capacity = capacity
        self.sales = sales
        self.cost = cost
        self.event_name = event_name

    def update(self, count_ticket):
        """this method update capacity and sales items of info_event file when ticket purchased by costumer"""

        change = pd.read_csv('info_event.csv')
        location = 0
        with open('info_event.csv', 'r') as change_file:
            csv_reader = csv.DictReader(change_file)
            for row in csv_reader:
                if row['code_event'] == self.code_event:
                    new_sales = int(row['sales'])+count_ticket
                    new_capacity = int(row['capacity'])-count_ticket
                    self.sales = new_sales
                    self.capacity = new_capacity
                    change.loc[location, 'sales'] = new_sales
                    change.loc[location, 'capacity'] = new_capacity
                    change.to_csv('info_event.csv', index=False)
                    logger.info_logger.info(f'Event with code:{self.code_event}'
                                            f' and name:{self.event_name} has been updated')
                location += 1

    def calculate_discount(self, role, discount_percent, count_ticket):
        """this method take amount of discount percent and number of thicket that costumer want to buy
         and calculate final price """

        self.role = role
        discount_cost = round((int(self.cost)*count_ticket)-((int(self.cost)*count_ticket)*int(discount_percent)/100))
        print(Fore.YELLOW+f"Dear *{self.role}* the total cost of {self.event_name} "
                          f"Event is ", discount_cost, "$")
        return discount_cost

    def display_buy(self, count_ticket, cost):
        """this method show information about Ticket issued """
        print(Fore.YELLOW)
        print(f'**information of your shopping*** \n'
              f'event name:{self.event_name} \n'
              f'Date: {self.date} \n'
              f'Place: {self.place} \n'
              f'cost paid:', cost, '$ \n'
              f'ticket count:', count_ticket)
        logger.ticket_logger.info(f'the amount of {count_ticket} ticket(s) for '
                                  f'{self.code_event},{self.event_name} event '
                                  f'sold')




