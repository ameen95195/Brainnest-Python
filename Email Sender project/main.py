import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from constants import Consts
import schedule
import json
import time
from datetime import datetime


class Main:

    def __init__(self):
        # read text.txt file
        with open("config.json") as f:
            self.configfile = json.load(f)

        # add schedule time for sending emails
        schedule.every().day.at(self.configfile[Consts.DAILY_SCHEDULE_TIME]).do(self.start_process)
        while True:  # keep app running for scheduling
            schedule.run_pending()
            time.sleep(1)

    def start_process(self):

        # make sure to reread config file agine next day
        with open("config.json") as f:
            self.configfile = json.load(f)

        msg = MIMEMultipart()
        msg[Consts.MSG_SUBJECT] = self.configfile[Consts.MSG_SUBJECT]
        msg.attach(MIMEText(self.configfile[Consts.MSG_CONTENT], "plain"))

        attach = self.get_attach_file()
        if attach is None:
            if not input("there is an error getting attached file\n "
                         "please add correct attachment-location in text.txt and press any key to continue\n"
                         " or (e) to send the message without attachment: ").lower().__eq__("e"):
                self.start_process()
                return
        else:
            msg.attach(attach)

        self.sendemails(self.configfile[Consts.RECIPIENTS_EMAILS], msg)

    def get_attach_file(self):
        """

        :return: attached file that specify in text.txt file with key: attachment-location
        """
        print("Getting attachment....")
        att_file_name = self.configfile[Consts.ATTACH_LOCATION].split("/")[-1]  # getting file name only
        try:  # catch any error may happen and write it in logs.txt file
            with open(self.configfile[Consts.ATTACH_LOCATION], "rb") as f:
                attach = MIMEApplication(f.read(), _subtype="pdf")  # initialize attachment file

            # add header data for file to be readable by email engin
            attach.add_header('Content-Disposition', 'attachment', filename=att_file_name)
            print("Setting attachment....")
            return attach
        except Exception as e:
            with open("logs.txt", "a") as log:
                log.write(f'[{datetime.now()}] ' + str(e) + '\n')
                log.close()
            print(e)
            return None

    def sendemails(self, receivers: [str], e_msg: MIMEMultipart()):
        """
        send emails to all receptions in text.txt array element with key: recipients-emails
        :param receivers: the receptions e-mail
        :param e_msg: MIMEMultipart object message
        """
        try:  # catch any error may happen and write it in logs.txt file
            print(f"Connecting to {self.configfile[Consts.HOST_SERVER]} server  ...")
            with smtplib.SMTP_SSL(self.configfile[Consts.HOST_SERVER], self.configfile[Consts.PORT]) as server:
                print(f"Connection established to {self.configfile[Consts.HOST_SERVER]} server.")

                # login to the server by user email and password
                server.login(self.configfile[Consts.SENDER_EMAIL], self.configfile[Consts.SENDER_PASSWORD])
                # set the sender email
                e_msg[Consts.MSG_FROM] = self.configfile[Consts.SENDER_EMAIL]

                # iterate on all receptions to send them the report email
                for receiver in receivers:
                    print(f"sending to {receiver} ...")
                    e_msg[Consts.MSG_TO] = receiver

                    try:  # inner try in case rising error will not stop the loop
                        server.send_message(e_msg)
                        print(f"Mail has sent to {receiver} .")
                    except Exception as e:
                        with open("logs.txt", "a") as log:
                            log.write(f'[{datetime.now()}] ' + str(e) + '\n')
                            log.close()
                        print(e)

        except Exception as e:
            with open("logs.txt", "a") as log:
                log.write(f'[{datetime.now()}] ' + str(e) + '\n')
                log.close()
            print(e)


Main()
