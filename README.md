# obs-cliploader
An automatic bridge between OBS Studio and Google Drive, written in Python.

# Description
An automated script for uploading OBS Studio recordings directly to Google Drive. The script triggers automatically whenever the recording hotkey is pressed. The primary goals of this project are to save time and optimize local disk space.

# Technologies
- Python 3.11 (OBS doesn't work with newer)
- Google API Python Client
- OBS

## Getting started

### 1. Clone repository
Copy project on your computer
    ```sh
        git clone git@github.com:Nyk00s/obs-cliploader.git
    ```
### 2. Configure .env file
Create .env file and set GOOGLE_FOLDER_ID variable with your google folder id

### 3. Create Google Cloud project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. In search field type Google Drive API and enable it
4. Go to API & Services and configure OAuth consent screen (choose External and add your address email)
5. Create Credentials. In API & Services and choose Credentials -> Create Credentials -> OAuth client ID, choose Desktop application, download json file and move it to project folder

### 4. Configure obs
1. Go to Tools -> Scripts -> Python setttings and choose path to python (3.11 or older)
2. In Scripts add start_script.py

### 5. Start Recording
You can now create clips using either Recording or the Replay Buffer, and they will be automatically uploaded to your Google Drive folder. Once the upload is successful, the local file will be removed from your computer to save space.
(Note: You can disable this feature by commenting out line 126 in main.py).
