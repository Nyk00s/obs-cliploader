import os
import sys
import logging
import subprocess
import obspython as obs

logging.basicConfig(filename='logs.log', level=logging.INFO, filemode='a',
                    format="[%(asctime)s] :: %(levelname)s :: %(message)s")
HOTKEY_NAME = "TEST SCRIPT"
HOTKEY_ID = obs.OBS_INVALID_HOTKEY_ID


def start():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bat_path = os.path.join(script_dir, 'starter.bat')

    if os.path.exists(bat_path):
        subprocess.Popen([bat_path, *sys.argv[1:]], creationflags=0x08000000)
        logging.info("Running starter.bat...")
    else:
        logging.error("Couldn't find starter.bat!")


def callback(pressed):
    if pressed:
        start()


def script_description():
    return "Custom hotkey for testing my script in obs"

def script_load(settings):
    global HOTKEY_ID
    HOTKEY_ID = obs.obs_hotkey_register_fronted(
        "testowy_skrypt_python_id",
        HOTKEY_NAME,
        callback()
    )

    save_array = obs.obs_data_get_array(settings, "testowy_skrypt_hotkey")
    obs.obs_hotkey_load(HOTKEY_ID, save_array)
    obs.obs_data_array_release(save_array)


def script_save(settings):
    save_array = obs.obs_hotkey_save(HOTKEY_ID)
    obs.obs_data_set_array(settings, "testowy_skrypt_hotkey", save_array)
    obs.obs_data_array_release(save_array)