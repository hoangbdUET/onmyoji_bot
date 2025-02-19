from gui.tkui import Application
from tools.logsystem import MyLog

import configparser
import ctypes
import logging
import os
import subprocess
import sys
import tkinter as tk


def is_admin():
    # UAC application, get administrator rights
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


class MyBattle(Application):
    def __init__(self, master):
        Application.__init__(self, master)
        self.conf = configparser.ConfigParser()

    def set_conf(self):
        '''
        Set parameters to configuration file
        '''
        # Operating parameters
        self.conf.set('DEFAULT', 'client', str(self.client.current()))
        section = self.section.index('current')
        self.conf.set('DEFAULT', 'run_section', str(section))

        # General parameters
        self.conf.set('watchdog', 'watchdog_enable',
                      str(self.watchdog_enable.get()))
        self.conf.set('watchdog', 'max_win_time', str(self.max_win_time.get()))
        self.conf.set('watchdog', 'max_op_time',
                      str(self.max_op_time.get()))

        self.conf.set('others', 'debug_enable', str(
            self.debug_enable.get()))

        # Yuhun parameters
        self.conf.set('DEFAULT', 'run_mode', str(self.run_mode.get()))
        self.conf.set('DEFAULT', 'max_times', str(self.max_times.get()))
        self.conf.set('DEFAULT', 'end_operation',
                      str(self.end_operation.current()))
        self.conf.set('mitama', 'run_submode', str(self.run_submode.get()))
        self.conf.set('mitama', 'mitama_team_mark',
                      str(self.mitama_team_mark.current()))

        # Explore parameters
        self.conf.set('explore', 'explore_mode', str(self.explore_mode.get()))
        self.conf.set('explore', 'gouliang', str(self.gouliang))
        self.conf.set('explore', 'gouliang_b', str(self.gouliang_b))
        self.conf.set('explore', 'fight_boss_enable',
                      str(self.fight_boss_enable.get()))
        self.conf.set('explore', 'slide_shikigami',
                      str(self.slide_shikigami.get()))
        self.conf.set('explore', 'slide_shikigami_progress',
                      str(self.slide_shikigami_progress.get()))
        self.conf.set('explore', 'change_shikigami',
                      str(self.cmb.current()))

    def get_conf(self):
        # Add configuration
        try:
            self.conf.add_section('watchdog')
            self.conf.add_section('mitama')
            self.conf.add_section('explore')
            self.conf.add_section('others')
        except:
            pass

        # Change setting
        self.set_conf()

        # Save the configuration file
        with open('conf.ini', 'w') as configfile:
            self.conf.write(configfile)

    def start_onmyoji(self):
        # Display parameters
        self.show_params()

        # Read primary copy
        self.get_conf()

        subprocess.Popen("cmd.exe /c start Core.exe")
        # os.system("onmyoji.exe")

    def stop_onmyoji(self):
        os._exit(0)


def my_excepthook(exc_type, exc_value, tb):
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        msg += '   File "%.500s", line %d, in %.500s\n' % (
            filename, lineno, name)
        tb = tb.tb_next

    msg += ' %s: %s\n' % (exc_type.__name__, exc_value)

    logging.error(msg)


if __name__ == "__main__":
    try:
        # Detect administrator permissions
        if is_admin():
            # Initialization log
            MyLog.init()

            # Error message into the log
            sys.excepthook = my_excepthook
            logging.info('Get admin rights')

            # Query DPI Awareness (Windows 10 and 8)
            awareness = ctypes.c_int()
            errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(
                0, ctypes.byref(awareness))

            # Set DPI Awareness  (Windows 10 and 8)
            errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(1)
            # the argument is the awareness level, which can be 0, 1 or 2:
            # for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)

            # Set DPI Awareness  (Windows 7 and Vista)
            success = ctypes.windll.user32.SetProcessDPIAware()
            # behaviour on later OSes is undefined, although when I run it on my Windows 10 machine, it seems to work with effects identical to SetProcessDpiAwareness(1)

            # Set battle parameters
            root = tk.Tk()
            app = MyBattle(root)
            app.mainloop()

        else:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
    except:
        pass
