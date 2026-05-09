import os
import sys
import logging
from google.oauth2.credentials import Credentials

script_dir = os.path.dirname(os.path.abspath(__file__))
logs_path = os.path.join(script_dir, 'logs.log')


logging.basicConfig(filename=logs_path, level=logging.INFO, filemode='a',
                    format="[%(asctime)s] :: %(levelname)s :: %(message)s")


SCOPES = ['https://www.googleapis.com/auth/drive.file']


def get_creds_path():
    json_files = [path for path in os.listdir(script_dir) if path.lower().endswith(".json")]
    if len(json_files) > 1:
        raise Exception("To many credentials files")
    elif len(json_files) < 1:
        raise Exception("No credentials file in directory")
    else:
        return json_files[0]
            


def authenticate():
    try:
        creds = Credentials.from_authorized_user_file(get_creds_path, SCOPES)
    except Exception as e:
        logging.error(e)
        sys.exit(0) 


def main():
    if len(sys.argv) <= 0:
        logging.error("No Arguments")
    elif len(sys.argv) == 1:
        # simple check if something is to send
        authenticate()
        logging.info(sys.argv[0])
    elif len(sys.argv) == 2:
        # send particular file to cloude
        logging.info(sys.argv[0], sys.argv[1])
    else:
        # cos wymysle
        logging.info(sys.argv)


if __name__ == "__main__":
    main()


# TODO: Przesłać testowy plik na google drive
