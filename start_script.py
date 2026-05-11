import os
import logging
import subprocess
import threading
import obspython as obs


script_dir = os.path.dirname(os.path.abspath(__file__))
bat_path = os.path.join(script_dir, 'starter.bat')
logs_path = os.path.join(script_dir, 'logs.log')


logging.basicConfig(filename=logs_path, level=logging.INFO, filemode='a',
                    format="[%(asctime)s] :: %(levelname)s :: %(message)s")


def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED:
        logging.info("Clip has been saved via replay buffer")
        handle_last_replay()
    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        logging.info("Clip has been saved via recording")
        handle_last_recording()


def handle_last_replay():
    file_path = obs.obs_frontend_get_last_replay()
    logging.info(f"Replay path: {file_path}")

    if file_path and os.path.exists(file_path):
        logging.info(f"Path of saved clip by Replay Buffer: {file_path}")
        run_starter_with_args(file_path)
    else:
        logging.warning("File path not found")


def handle_last_recording():
    file_path = obs.obs_frontend_get_last_recording()
    logging.info(file_path)

    if file_path and os.path.exists(file_path):
        logging.info(f"Path of saved clip by end of recording: {file_path}")
        run_starter_with_args(file_path)
    else:
        logging.warning("File path not found")


def run_starter_with_args(path):
    full_path = os.path.abspath(path)
    if os.path.exists(bat_path):
        subprocess.Popen([bat_path, full_path], cwd=script_dir, creationflags=subprocess.CREATE_NO_WINDOW)
        logging.info(f"Running starter.bat for: {full_path}")
    else:
        logging.error("Bat file not found")


def script_load(settings):
    obs.obs_frontend_add_event_callback(on_event)
    logging.info("OBS Script is loaded and listen")


def script_description():
    return "Script for sending clips on google drive"
