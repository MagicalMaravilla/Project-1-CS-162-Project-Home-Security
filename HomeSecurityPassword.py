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
        self.guest_expiration = None
        self.guest_attempts = 0
        self.guess_password = '1969'
        logging.info('SecurePasswordSystem initialized.')

    def set_initial_username(self):
        while True:
            try:
                username = input('Enter your username: ').strip()
                if not username:
                    print('Username cannot be empty. Using default username "user123".')
                    self.username = username
                    print(f'Welcome {self.username}!')
                    break
                else:
                    print('Invalid username. Ensure it\'s within 20 character limit and only contains letters, numbers,'
                          'and symbols')
            except Exception as e:
                logging.error(f"An error occurred while setting username: {e}")
                print('An unexpected error occurred. Please try again.')

    def reset_username(self):
        try:
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
        except Exception as e:
            logging.error(f'An error occurred while resetting username: {e}')
            print('An unexpected error occurred. Please try again.')

    def set_initial_password(self):
        while True:
            try:
                password = input('Enter a 4 digit numeric password: ').strip()
                if not password:
                    print('Password cannot be empty. Using default password for this specific device to "1776".')
                    self.password = '1776'
                    break
                elif len(password) == 4 and password.isdigit():
                    self.password = password
                    print(f'Password set successfully, welcome {self.username} to Secure Homes Inc family. Your safety'
                          f'is our number one concern.')
                    break
                else:
                    print('Invalid input. Please enter a 4-digit numeric password')
            except Exception as e:
                logging.error(f"An error occurred while setting password: {e}")
                print('An unexpected error occurred. Please try again. ')


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
        try:
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
        except Exception as e:
            logging.error(f'An error occurred while verifying password: {e}')
            print('An unexpected error occurred. Please try again.')

    def check_failed_attempts(self):
        try:
            if self.failed_attempts >= 3:
                self.locked_until = datetime.datetime.now() + datetime.timedelta(hours=1)
                print(f'Multiple failed attempts detected, {self.username}! System locked until {self.locked_until}.')
        except Exception as e:
            logging.error(f'An error occurred while checking failed attempts: {e}')
            print('An unexpected error occurred. Please try again.')

    def set_guest_access(self):
        try:
            duration = int(input('Enter the number of days for guest access (1 - 31): '))
            if not 1 <= duration <= 31:
                print('Invalid duration. Please enter a value between 1 and 31.')
                return

            time_choice = input('Do you want to set a specific time of day for access (yes/no): ')
            if time_choice.lower().strip() =='yes':
                time_of_day = input('Enter the time in HH:MM format (24-hour):')
                match = re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', time_of_day)
                if not match:
                    print('Invalid time format. Please use HH:MM in 24-hour format.')
                    return
            else:
                time_of_day = datetime.datetime.strftime('%H:%M')
                self.guest_expiration = datetime.datetime.now() + datetime.timedelta(days=duration)
                print(f'Guest access granted until {self.guest_expiration}')
        except Exception as e:
            logging.error(f'An error occurred while setting guest access: {e}')
            print('An unexpected error occurred. Please try again.')

    def verify_guest_access(self):
        try:
            current_time = datetime.datetime.now()
            if not self.guest_expiration or current_time > self.guest_expiration:
                print('Guest access expired or not set.')
                return

            if current_time.hour >= 0 and current_time < 6:
                print('Access restricted during nighttime (12 AM - 6 AM).')
                return
            if self.guest_attempts >= 10:
                print('Too many failed attempts. Guest access locked.')
                return
            guest_password = input('Enter guest password: ')
            if guest_password == '1969':
                print('Guest access granted.')
                logging.info(f'Guest accessed at {current_time}.')
            else:
                self.guest_attempts += 1
                print(f'Incorrect password. you have {10 - self.guest_attempts} attempts left.')
        except Exception as e:
            logging.info(f'An error occurred while verifying guest access:{e}')
            print('An unexpected error occurred. Please try again.')

    def owner_override(self):
        owner_password = input('Enter owner password for override: ')
        if owner_password == self.password:
            print('Owner Override successful. Access granted.')
            logging.info(f'Owner override at {datetime.datetime.now()}.')
        else:
            print('Incorrect owner password. Access Denied')

        def guest_feature(self):
            print('Guess can view the current time.')
            print(f'Current time: {datetime.datetime.now().strftime("%H:%M:%S")}')

            if hasattr(self, 'guest_expiration'):
                time_remaining = self.guest_expiration - datetime.datetime.now()
                hours, remainder = divmod(time_remaining.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                print(f'Guest access will expire in {time_remaining.days} days, {hours} hours, {minutes} minutes, and {seconds}, seconds')
            else:
                print('Guest access expiration time not set.')






