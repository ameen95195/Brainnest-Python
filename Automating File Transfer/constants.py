# constants variables


HOST_SERVER = "host-server"
LOGIN_USER = "login-user"
LOGIN_PASSWORD = "login-password"
DAILY_SCHEDULE_TIME = "daily-schedule-time"
REMOTE_FOLDER_PATH = "remote-folder-path"
LOCAL_FOLDER_PATH = "local-folder-path"
NETWORK_FOLDER_PATH = "internal-network-folder-path"


def consts():
    res = [HOST_SERVER, LOGIN_USER, LOGIN_PASSWORD, DAILY_SCHEDULE_TIME, REMOTE_FOLDER_PATH, LOCAL_FOLDER_PATH,
           NETWORK_FOLDER_PATH]
    return res


def check_config_data(config: dict):
    """
    check correction data configuration
    :param config: json variable
    :return: true if data was correct, false if not
    """
    iserror = False
    for key in consts():
        if key in config.keys():
            continue
        else:
            print("config file missing key: " + key)
            iserror = True
    if iserror:
        return False
    if config[HOST_SERVER] == "":
        print(f"config file missing {HOST_SERVER}: value!!")
        return
    if config[NETWORK_FOLDER_PATH] == "":
        print(f"config file missing {NETWORK_FOLDER_PATH} value!!")
        return
    if config[LOCAL_FOLDER_PATH] == "":
        print(f"config file missing {LOCAL_FOLDER_PATH} value!!")
        return

    return True
