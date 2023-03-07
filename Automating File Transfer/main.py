import json
import time
from datetime import datetime
from ftplib import FTP
from threading import Thread
import os
import shutil
from typing import Any

import schedule

import constants


def logs(e):
    with open("logs.txt", "a") as log:
        log.write(f'[{datetime.now()}] ' + str(e) + '\n')
        log.close()
    print(e)


class Main:
    def __init__(self):
        self.fileconfig = self.check_config_file()
        if self.fileconfig is None:
            return

        print("program started... \nWaiting for the scheduled time...")
        # add schedule time for sending emails
        schedule.every().day.at(self.fileconfig[constants.DAILY_SCHEDULE_TIME]).do(self.start_process)
        while True:  # keep app running for scheduling
            schedule.run_pending()
            time.sleep(1)

    def start_process(self):
        with FTP(self.fileconfig[constants.HOST_SERVER]) as ftp:
            if self.fileconfig[constants.LOGIN_USER] != "":  # login via user and password if exists in config file
                ftp.login(self.fileconfig[constants.LOGIN_USER], self.fileconfig[constants.LOGIN_PASSWORD])
            else:
                ftp.login()
            ftp.cwd(self.fileconfig[constants.REMOTE_FOLDER_PATH])  # move to the files directory
            self.download_all_files(ftp)  # start downloading files
            self.move_files_to_internal_network()  # start moving files to the internal network

    def download_all_files(self, ftp: FTP):
        """
        download all files in current dir of ftp connection
        :param ftp: ...
        """
        try:
            for file in ftp.nlst():
                print(f"downloading file: {file}...")
                self.download_file(ftp, file, self.fileconfig[constants.LOCAL_FOLDER_PATH])
                print(f"downloading complete {file}...")
        except Exception as e:
            logs(e)

    def move_files_to_internal_network(self):
        """
        moving files from local directory to internal network directory
        warning!!! if internal network folder or path not exists it will make a directory with the same given path
        """
        if self.fileconfig[constants.NETWORK_FOLDER_PATH] != "" \
                and os.path.exists(self.fileconfig[constants.NETWORK_FOLDER_PATH]) == False:  # check path exists
            os.makedirs(self.fileconfig[constants.NETWORK_FOLDER_PATH])
        try:
            print("start moving files to internal network")
            for file in os.listdir(self.fileconfig[constants.LOCAL_FOLDER_PATH]):
                source = self.fileconfig[constants.LOCAL_FOLDER_PATH] + file
                destination = self.fileconfig[constants.NETWORK_FOLDER_PATH] + file
                shutil.move(source, destination)
                print(f"{file} has been moved to internal network")
        except Exception as e:
            logs(e)

    def check_config_file(self) -> dict | None:
        """
        check config file and return json data after check every thing is correct
        :return: json variable
        """
        try:
            with open("config.json") as f:
                configfile = json.load(f)
                if constants.check_config_data(configfile):
                    return configfile
                else:
                    raise ValueError

        except ValueError:
            logs("config file missing some data...!")
            return None
        except Exception as e:
            logs(e)
            return None

    def download_file(self, ftp: FTP, filename, localpath=""):
        """
        :param ftp: connected class
        :param filename:
        :param localpath: (optional) local path to download in it
        """
        if localpath != "" and os.path.exists(localpath) == False:
            os.makedirs(localpath)
        try:  # RETR is a builtin command to download file
            with open(localpath + filename, "wb") as f:
                ftp.retrbinary("RETR " + filename, f.write)
        except Exception as e:
            logs(e)


Main()
