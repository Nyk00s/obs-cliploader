import os
import sys
import logging
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.exceptions import MutualTLSChannelError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import mimetypes
import pickle

script_dir = os.path.dirname(os.path.abspath(__file__))
logs_path = os.path.join(script_dir, 'logs.log')
bat_logs_path = os.path.join(script_dir, 'bot_logs.log')
logging.basicConfig(filename=logs_path, level=logging.INFO, filemode='a',
                    format="[%(asctime)s] :: %(levelname)s :: %(message)s")


load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/drive.file']
GOOGLE_FOLDER_ID = os.getenv('GOOGLE_FOLDER_ID')
logging.info(f'{GOOGLE_FOLDER_ID}')


def get_creds_path():
    json_files = [path for path in os.listdir(script_dir) if path.lower().endswith(".json")]
    if len(json_files) > 1:
        raise Exception("To many credentials files")
    elif len(json_files) < 1:
        raise Exception("No credentials file in directory")
    else:
        return os.path.join(script_dir, json_files[0])
            


def authenticate():
    try:
        creds = None
        json_path = get_creds_path()
        token_path = os.path.join(script_dir, 'token.pickle')
        logging.info(f'{json_path} {token_path}')

        if os.path.exists(token_path):
            with open(token_path, 'rb') as f:
                creds = pickle.load(f)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    json_path,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(token_path, 'wb') as f:
                pickle.dump(creds, f)
        return creds
    except Exception as e:
        logging.error(e)
        sys.exit(0) 


def upload_file(file_path: str):
    try:

        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)

        if not os.path.exists(file_path):
            logging.error(f"File {file_path} doesn't exist")
            return

        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [GOOGLE_FOLDER_ID]
        }
        mime, _ = mimetypes.guess_type(file_path)
        if mime is None:
            mime = 'application/octet-stream'

        media = MediaFileUpload(
            file_path,
            mimetype=mime,
            resumable=True,
            chunksize=1024*1024
        )

        logging.info(f"Start sending: {file_path} (MIME: {mime})")


        request = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logging.info(f"Upload progress: {int(status.progress() * 100)}%")

        logging.info(f"Success! File ID: {response.get('id')}")
    except Exception as e:
        logging.error(e)
        sys.exit(0)


def delete_clip(path: str):
    os.remove(path)


def main():
    if len(sys.argv) == 1:
        logging.error("No arguments")
    elif len(sys.argv) == 2:
        logging.info(f"{sys.argv[0]}, {sys.argv[1]}")
        clip_path = sys.argv[1]
        if os.path.exists(clip_path):
            upload_file(sys.argv[1])
            delete_clip(sys.argv[1])
    else:
        # cos wymysle
        logging.info(sys.argv)


def clean_logs_if_needed(log_path, max_lines=500):
    try:
        if not os.path.exists(log_path):
            return
        
        with open(log_path, 'r') as f:
            lines = f.readlines()

        if len(lines) > max_lines:
            with open(log_path, 'w') as f:
                f.writelines(lines[-max_lines:])
            logging.info("Logs cleaned")
    except Exception as e:
        logging.error(f"Error while cleaning logs: {e}")


if __name__ == "__main__":
    clean_logs_if_needed(logs_path)
    clean_logs_if_needed(bat_logs_path)
    main()
    logging.info('script ended')
