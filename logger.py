
import logging

# Create a custom logger
my_logger = logging.getLogger('error log')

# Create handlers
f_handler = logging.FileHandler('error.log')
f_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)


# Create formatters and add it to handlers
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)

# Add handlers to the logger
my_logger.addHandler(f_handler)

my_logger.warning('This is a warning')

info_logger = logging.getLogger('event log')
info_logger.setLevel(logging.DEBUG)

f_handler = logging.FileHandler('event.log')
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
info_logger.addHandler(f_handler)

user_logger = logging.getLogger('user log')
user_logger.setLevel(logging.DEBUG)

f_handler = logging.FileHandler('user.log')
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
user_logger.addHandler(f_handler)


ticket_logger = logging.getLogger('ticket log')
ticket_logger.setLevel(logging.DEBUG)

f_handler = logging.FileHandler('ticket.log')
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
ticket_logger.addHandler(f_handler)
