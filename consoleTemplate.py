"""
---------------------------------
 Author: gilbertorgit
 Date: 03/2023
---------------------------------
"""

import logging
import pexpect
from time import sleep, time
import re

from basicInfra import BasicInfra

USER = "root"
ROOT_PASSWORD = "juniper123"
LAB_PASSWORD = "lab123"
MGMT_INTERFACE_VMX = "fxp0"


class ConsoleConfig:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler('app.log')
        self.handler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    # create the file to log all the pexpect commands
    @staticmethod
    def logfile_pexpect_start(child, hostname, mode='ab'):
        fout = open(f'pexpect_log_file.txt{hostname}', f'{mode}')  # Create a logfile
        child.logfile = fout  # it will log all the child input/output to mylogfile.txt

    @staticmethod
    def countdown(time_sec):
        while time_sec:
            mins, secs = divmod(time_sec, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            sleep(1)
            time_sec -= 1

    # Get the console
    def get_console(self, hostname):
        self.logger.debug(f"Trying to get initial Console: {hostname}")
        return pexpect.spawn(f"virsh console {hostname} --force", timeout=3)

    # get the console from get_console method
    def get_console_prompt(self, hostname):
        print("#" * 80, f"Trying to get initial Console: {hostname}")
        while True:
            try:
                child = self.get_console(hostname)
                self.logfile_pexpect_start(child, hostname, 'wb')
                child.send("\r\r\r")
                try:
                    index = child.expect(["error: failed to get domain", ".*ogin:"], timeout=3)
                    child.expect(".*ogin:")
                    child.sendcontrol("]")
                    # We got the console, so return True
                    self.logger.debug(f"Console prompt ready for {hostname}")
                    return True
                except pexpect.exceptions.TIMEOUT:
                    # The console isn't ready yet, so kill the child process and try again
                    print(f"Console {hostname} not ready, trying again...")
                    self.logger.debug(f"Console {hostname} not ready, trying again...")
                    child.kill(0)
                    sleep(10)
                except pexpect.exceptions.EOF:
                    # There is no console, domain is not configured
                    print(f"Domain {hostname} is not configured")
                    child.kill(0)
                    self.logger.debug(f"Domain {hostname} is not configured")
                    return False
            except Exception as e:
                print(str(e))
                self.logger.info(str(e))
                return False

    def junos_common_config(self, hostname, mgmt_ip):
        print("-" * 40, f"Configuring root/lab user, hostname and MGMT IP: {hostname}-{mgmt_ip}")
        # Step 0: Getting Console
        print("Step 0: Get Console")
        child = self.get_console(hostname)
        # fout = open('mylogfile.txt', 'wab')
        # child.logfile = fout
        self.logfile_pexpect_start(child, hostname)
        child.send("\r\r\r")
        child.expect(".*ogin:")

        # Step 1: Log in as root
        print("Step 1: Log in as root")
        self.logger.debug(f"sending USER: {USER}")
        child.sendline(USER)

        child.expect("root.*", timeout=3)
        child.send("\r")

        match = None
        while match is None:
            child.sendline('uptime')
            self.logger.debug(f"sending uptime")
            child.expect("root.*", timeout=3)
            r = child.before.decode('utf-8')
            #print(f"------- printing {r}")
            self.logger.debug(f"Get the uptime output")
            match = re.search(r'up\s+(\d+)\s+mins', r)
            self.logger.debug(f"Printing uptime child.before: {r}")
            sleep(1)

            if match:
                print(f"- Check if system uptime is bigger than 6min to start the configuration")
                uptime = int(match.group(1))
                print(f"System uptime: {uptime}")
                if uptime < 6:
                    self.logger.debug(f"if uptime less than 6 wait until 6 min to start the configuration")
                    # wait for the remaining time
                    to_wait = (6 - uptime) * 60
                    print(f"*** Waiting: {to_wait} seconds to configure")
                    self.countdown(to_wait)
                    #sleep((6 - uptime) * 60)

        # Step 2: Enter CLI
        print("Step 2: CLI")
        self.logger.debug("Sending cli")
        child.sendline("cli")

        # Step 3: EDIT
        print("Step 3: EDIT")
        child.expect("root.*")
        self.logger.debug("Sending edit (configure)")
        child.sendline("edit")
        child.expect("root.*", timeout=60)

        # Step 4: ROOT PWD
        print("Step 6: Configure ROOT PWD")
        self.logger.debug("Setting root authentication")
        child.sendline("set system root-authentication plain-text-password")
        child.expect("New password:")
        self.logger.debug("sending new password")
        child.sendline(ROOT_PASSWORD)
        self.logger.debug("sending Retype new password")
        child.expect("Retype new password:")
        child.sendline(ROOT_PASSWORD)

        # Step 5: LAB USER/PWD
        print("Step 7: Configure LAB USER/PWD")
        self.logger.debug("Setting lab authentication")
        child.sendline("set system login user lab class super-user authentication plain-text-password")
        child.expect("New password:")
        self.logger.debug("sending new password")
        child.sendline(LAB_PASSWORD)
        self.logger.debug("sending Retype new password")
        child.expect("Retype new password:")
        child.sendline(LAB_PASSWORD)

        # Step 6: HOSTNAME/NETCONF/SSH
        print("Step 8: Configure HOSTNAME/NETCONF/SSH")
        self.logger.debug(f"Configuring host-name to {hostname}")
        child.sendline(f"set system host-name {hostname}")
        self.logger.debug("Configuring netconf and ssh")
        child.sendline("set system services netconf ssh")
        child.sendline("set system services ssh")
        child.sendline("set system services ssh root-login allow")

        # Step 7: MGMT INTERFACE
        print("Step 9: Configure MGMT INTERFACE")
        child.send("\r")
        child.expect("root.*", timeout=60)
        self.logger.debug(f"delete all interfaces")
        child.sendline("delete interfaces")
        self.logger.debug(f"Configure MGMT INTERFACE {MGMT_INTERFACE_VMX} with address {mgmt_ip}/24")
        child.sendline(f"set interface {MGMT_INTERFACE_VMX} unit 0 family inet address {mgmt_ip}/24")
        child.send("\r")
        child.expect("root.*", timeout=60)
        child.sendcontrol("]")

    def junos_vmx_specific_config(self, hostname):
        print("-" * 40, f"Configuring vMX specific config: {hostname}")
        child = self.get_console(hostname)
        self.logfile_pexpect_start(child, hostname)
        child.send("\r\r\r")
        # Step 8: Delete Configs
        print("Step 4: Delete Configs")
        child.expect("root.*", timeout=60)
        self.logger.debug("Deleting chassis, system and protocols")
        child.sendline("delete chassis auto-image-upgrade")
        child.sendline("delete system processes dhcp-service")
        child.sendline("delete protocols router-advertisement")

        # Step 9: FPC LITE-MODE
        print("Step 5: Configure FPC LITE-MODE")
        self.logger.debug("Configuring lite-mode")
        child.sendline("set chassis fpc 0 lite-mode")
        child.send("\r")
        child.expect("root.*", timeout=60)
        child.sendcontrol("]")

    def junos_commit_quit(self, hostname):
        print("-" * 40, f"Commit config and quit: {hostname}")
        child = self.get_console(hostname)
        self.logfile_pexpect_start(child, hostname)
        child.send("\r\r\r")
        # Step 10: COMMIT and save baseline configuration
        print("Step 10: COMMIT")
        self.logger.debug("Committing changes and quit edit mode")
        child.expect("root.*", timeout=60)
        child.sendline(f"show | save {hostname}_baseline.conf")
        child.expect("root.*", timeout=60)
        child.sendline("commit and-quit")

        # EXIT ROUTER
        print("EXIT ROUTER")
        child.expect("root.*", timeout=60)
        self.logger.debug("quit CLI mode")
        child.sendline("quit")
        child.expect("root.*", timeout=60)
        self.logger.debug("quit shell")
        child.sendline("exit")

        # EXIT CONSOLE
        print("EXIT CONSOLE")
        child.expect("login:", timeout=60)
        self.logger.debug("quit console")
        child.sendcontrol("]")

    def vmx_config(self, hostname, mgmt_ip):
        self.logger.debug("Starting vmx_config")
        if self.get_console_prompt(hostname):
            self.logger.debug("received TRUE from get_console_prompt")
            self.junos_common_config(hostname, mgmt_ip)
            self.junos_vmx_specific_config(hostname)
            self.junos_commit_quit(hostname)

            print("-" * 20, f'- {hostname} configuration completed\n')