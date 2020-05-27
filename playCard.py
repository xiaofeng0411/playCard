from email.header import Header
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import time
import setting
import smtplib
from email.mime.text import MIMEText
from time import strftime, localtime

go_work_hour = int(setting.go_work_hour)
back_work_hour = int(setting.back_work_hour)
directory = setting.adb_install_directory
sender = setting.sender_email_account
psw = setting.sender_email_password
receive = setting.receive_email_account


# Opening and closing the dingding is encapsulated as a dresser function
def with_open_close_dingding(func):
    def wrapper(self, *args, **kwargs):
        print("open dingding program")
        operation_list = [self.adbpower, self.adbclear,self.adbopen_dingding]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
        # Make sure it is fully booted and loaded with the appropriate buttons
        # (adjust here depending on the phone's response speed)
        time.sleep(10)
        # loading the punch interface
        operation_list1 = [self.adbclick_workbench,self.adbselect_attendance_button]
        for operation in operation_list1:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
            # Wait for the response after clicking the screen
            time.sleep(10)
        # Wait for the work interface to load
        time.sleep(10)
        # execute operation of punch in or punch out
        func(self, *args, **kwargs)
        # the aftermath
        print("killing dingding program success")
        operation_list2 = [self.adbback_desktop, self.adbkill_dingding, self.adbpower]
        for operation in operation_list2:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
        print("kill dingding program success")
    return wrapper


class dingDing:
    def __init__(self, directory):
        self.directory = directory
        # Light up the screen
        self.adbpower = '"%s\\adb" shell input keyevent 26' % directory
        # Sliding screen to unlock
        self.adbclear = '"%s\\adb" shell input swipe %s' % (directory,setting.unlock_coordinates)
        # Start the dingding application
        self.adbopen_dingding = '"%s\\adb" shell monkey -p com.alibaba.android.rimet -c android.intent.category.LAUNCHER 1' % directory
        # Closed dingding
        self.adbkill_dingding = '"%s\\adb" shell am force-stop com.alibaba.android.rimet' % directory
        # Return to the phone desktop
        self.adbback_desktop = '"%s\\adb" shell input keyevent 3' % directory
        # Click the workbench
        self.adbclick_workbench = '"%s\\adb" shell input tap %s' % (directory, setting.check_work)
        # Click the punch card interface button
        self.adbselect_attendance_button = '"%s\\adb" shell input tap %s' % (directory, setting.work_position)
        # Click the punch card button
        self.adbpunch_in = '"%s\\adb" shell input tap %s' % (directory, setting.check_position)
        # Click punch out button
        self.adbpunch_out = '"%s\\adb" shell input tap %s' % (directory, setting.play_position)


    #punch in
    @with_open_close_dingding
    def goto_work(self):
        operation_list = [self.adbpunch_in]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
            time.sleep(3)
        email_info = "punch in playcard success"
        self.send_email(email_info)
        print("punch in playcard success")

    # punch out
    @with_open_close_dingding
    def off_work(self):
        operation_list = [self.adbpunch_out]
        for operation in operation_list:
            process = subprocess.Popen(operation, shell=False, stdout=subprocess.PIPE)
            process.wait()
            time.sleep(3)
        email_info = "punch out playcard success"
        self.send_email(email_info)
        print("punch out playcard success")

    # send email to owner
    @staticmethod
    def send_email(info):
        msg = MIMEText(info, _charset="utf-8")
        sender = "wxdlxs@126.com"
        sender_host = "smtp.126.com"
        password = "IBQDBEMGWHYWFQUB"
        revicer = ["824316775@qq.com"]
        msg["Subject"] = "打卡信息邮件"
        msg['From'] = Header("打卡脚本", "utf-8")
        msg["To"] = ','.join(revicer)
        smtp = smtplib.SMTP()
        smtp.connect(sender_host, 25)
        smtp.login(sender, password)
        smtp.sendmail(sender, revicer, msg.as_string())
        print("send mail success")


def punch_in():
    print("start punching in")
    dingDing(directory).goto_work()


def punch_out():
    print("start punching out")
    dingDing(directory).off_work()


# execute the main function
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    print("start process")
    scheduler.add_job(punch_in, 'cron', day_of_week='1-5', hour=go_work_hour, minute=15)
    scheduler.add_job(punch_out, 'cron', day_of_week='1-5', hour=back_work_hour, minute=30)
    scheduler.start()
    print(strftime("%Y-%m-%d %H:%M:%S----4", localtime()))

