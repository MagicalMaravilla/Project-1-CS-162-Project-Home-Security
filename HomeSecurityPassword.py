import datetime
import re
import logging

logging.basicConfig(filename='secure_password_system.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

class SecurePasswordSystem:
    def __init__(self):
        self.password = None
        self.username = None
        self.locked_until = None
        self.failed_attempts = 0
        logging.info('SecurePasswordSystem initialized.')

    def set_initial_username(self):
        while True:
            username = input('Enter your username: ')
            if len(username) <= 20 and re.match('^[a-zA-Z0-9!@#$%^&*()_+{}|:<>?~\[\]-]*$', username):
                self.username = username
                print(f'welcome {self.username}')
                break
            else:
                print('Invalid username. Ensure it\'s within 20 characters and only contains letters, numbers, and '
                      'symbols.')

    def reset_username(self):
        confirmation = input('Are you sure you want to reset your username? (yes/no): ')
        if confirmation.lower() != 'yes':
            print('Username reset cancelled.')
            return

        current_password = input('Enter your current password for verification: ')
        if current_password != self.password:
            print('Incorrect password. Username reset cancelled.')
            return

        final_warning = input('This action cannot be undone. Are you sure you wish to proceed? (yes/no) ')
        if final_warning.lower() == 'yes':
            print('Please set new user name.')
            self.set_initial_username()
            logging.info(f'Username reset initiated by {self.username}')
        else:
            print('Username reset cancelled')

    def set_initial_password(self):
        while True:
            password = input('Enter a 4 digit numeric password: ')
            if len(password) != 4 and not password.isdigit():
                print('Invalid input. Please enter a 4 digit numeric password without any letters ')
            elif len(password) != 4:
                print('Invalid input. Your Password should be exactly 4 digits.')
            elif not password.isdigit():
                print('Invalid input. Your password should only contain numbers.')
            else:
                self.password = password
                print(
                    f'Password set successfully, welcome {self.username} to the Secure Homes Inc family. Your saftey is our'
                    'number one concern')
                break

    def reset_password(self):
        confirmation = input('Are you sure you want to reset your password? (yes/no): ')
        if confirmation.lower() != 'yes':
            print('Incorrect password. Password reset cancelled.')
            return
        final_warning = input('This action cannot be undone. Are you sure you wish to proceed? (yes/no): ')
        if final_warning.lower() == 'yes':
            print('Please set a new password.')
            self.set_initial_password()
            logging.info(f'Password reset initiated by {self.username}')
        else:
            print('Password reset cancelled.')

    def verify_password(self):
        max_attempts = 3

        if self.locked_until and datetime.datetime.now() < self.locked_until:
            print(f'Account is locked until {self.locked_until}. Please wait.')
            return

        enter_password = input(f'{self.username}, enter your password: ')
        if enter_password == self.password:
            print('Access granted')
            self.failed_attempts = 0
            self.locked_until = None
            logging.info(f'Successful login by {self.username}.')
        else:
            self.failed_attempts += 1
            remaining_attempts = max_attempts - self.failed_attempts
            if remaining_attempts > 0:
                print(f'Incorrect password. Try again. You have {remaining_attempts} attempts left')
                logging.warning(f'Failed login attempt {self.failed_attempts} by {self.username}')
            self.check_failed_attempts()

    def check_failed_attempts(self):
        if self.failed_attempts >= 3:
            self.locked_until = datetime.datetime.now() + datetime.timedelta(hours=1)
            print(f'Multiple failed attempts detected, {self.username}! System locked until {self.locked_until}.')






