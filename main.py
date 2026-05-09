import os
import sys
import logging

logging.basicConfig(filename='logs.log', level=logging.INFO, filemode='a',
                    format="[%(asctime)s] :: %(levelname)s :: %(message)s")


SCOPES = ['https://www.googleapis.com/auth/drive.file']


def main():
    if len(sys.argv) <= 0:
        logging.error("No Arguments")
    elif len(sys.argv) == 1:
        # simple check if something is to send
        logging.info(sys.argv[0])
    elif len(sys.argv) == 2:
        # send particular file to cloude
        logging.info(sys.argv[0], sys.argv[1])
    else:
        # cos wymysle
        logging.info(sys.argv)


if __name__ == "__main__":
    main()


# TODO: Dodac hotkey w obsie i przetestowac czy skrypty sie wykonują
