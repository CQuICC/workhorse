#!/usr/bin/env python
# from future import print_function, division
import requests
import getpass
import sys
import keyring

def get_login_data():
    # keyring.get_keyring

    username = keyring.get_password("netaccess", "username")
    password = keyring.get_password("netaccess", "password")
    if not username or not password:
        print("Error: Credentials not found. Please store them using keyring.")
        sys.exit(1)
    return {'userLogin': username, 'userPassword': password}



def get_approve_data():
    duration = '3'  # Always set to 1 day
    print('You have requested approval for 1 day')
    return {'duration': duration, 'approveBtn': ''}

def has_logged_in(response):
    '''Checks if login request is successful. Returns false if not.
    '''
    # If response is not 200 OK, raise error
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    # Check if login has failed by searching for a substring in the response
    # content
    elif b'/account/approve' not in response.content:
        return False

    return True

def main():

    # User agent string from Firefox 49 running on a Linux machine
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'}

    login_data = get_login_data()
    approve_data = get_approve_data()

    with requests.Session() as s:

        # Login request
        p = s.post('https://netaccess.iitm.ac.in/account/login',
                data=login_data, headers=headers)

        # Check if login is successful.
        if has_logged_in(p):
            print('Login successful.')
        else:
            print('Wrong username or password provided. Login failed!')
            sys.exit(0)

        # Approve machine request
        p = s.post('https://netaccess.iitm.ac.in/account/approve',
                data=approve_data, headers=headers)

        # If response is not 200 OK, approval has failed. Exit.
        if p.status_code != requests.codes.ok:
            p.raise_for_status()
        else:
            print('Machine approved successfully.')

        sys.exit(0)


if __name__ == '__main__':

    main()