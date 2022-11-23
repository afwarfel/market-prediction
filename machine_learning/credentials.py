from os.path import exists
import os
import pandas as pd
import collections


def credentials():
    """
    Check if a credentials file already exists and if it doesn't, generate one and ask the user for all of their credentials which will then be stored. This should make the process more streamlined and not require any credentials to be committed to a repo.
    """

    #Here you define all of the credentials that you'll need from the user
    required_credentials = ['FRED API Key']

    credentials_file_pathway = os.path.join('data','credentials.json')

    if exists(credentials_file_pathway):
        credentials = pd.read_json(credentials_file_pathway)
    else:
        credentials = {}
        for required_credential in required_credentials:
            credentials[required_credential] = input('What is your '+required_credential+'? ')
        pd.DataFrame(credentials, index=[0]).to_json(credentials_file_pathway,orient='records',indent=4)
        print('Credentials stored within data folder...')

    credentials = pd.read_json(credentials_file_pathway)
    if collections.Counter(required_credentials) != collections.Counter(credentials.columns):
        for required_credential in required_credentials:
            if required_credential not in credentials.columns:
                credentials[required_credential] = input('What is your '+required_credential+'? ')
        pd.DataFrame(credentials, index=[0]).to_json(credentials_file_pathway,orient='records',indent=4)
        print('Updating credentials stored within data folder...')

    for x in required_credentials:
        if len(credentials[x][0]) == 0:
            credentials[x] = input('What is your '+x+'? ')
            pd.DataFrame(credentials, index=[0]).to_json(credentials_file_pathway,orient='records',indent=4)
            print('Updating credentials stored within data folder...')

    return credentials
