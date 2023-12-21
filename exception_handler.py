"""
---------------------------------
 Author: gilbertorgit
 Date: 05/2023
---------------------------------
"""

import subprocess
import time
from jnpr.junos.exception import ConnectError, ConnectTimeoutError, RpcError, ConfigLoadError, ConnectRefusedError
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.utils.sw import SW
from lxml import etree
from paramiko.ssh_exception import SSHException, NoValidConnectionsError


def run_command(command, error_message=None):
    """
        Function to run a shell command using subprocess. If the command fails, an error message is printed.
        Args:
            command (str): The shell command to be executed.
            error_message (str, optional): If provided, the function will check if this error message is in the output.
                                            If it is, it will print a specific failure message.
     """
    try:
        subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        err_output = e.stderr.decode().strip() if e.stderr else ""
        if error_message and error_message in err_output:
            print(f"Command failed: {error_message}, skipping.")
        else:
            print(f"Command '{command}' failed with error: {e}")


def run_command_delete_image(command, error_message, hostname):
    """
        Function to run a command specifically for deleting images. If the command fails, a tailored error message is printed.
        Args:
            command (str): The shell command to be executed.
            error_message (str): The error message to be checked in the command output.
            hostname (str): The hostname of the device.
    """
    try:
        subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        err_output = e.stderr.decode().strip()
        if error_message in err_output:
            print(f"No domain found for {hostname}, skipping {error_message}...")


def run_command_interface(command):
    """
        Function to run a command specifically for interfacing. If the command fails, a failure message is returned.
        Args:
            command (str): The shell command to be executed.
        Returns:
            bool: True if the command succeeds, else False.
    """
    try:
        subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode().replace('\n', ' ')
        print(f"Command '{command}' failed: {error_message}, skipping.")
        return False


def poweroff_device(mgmt_ip, port=22, user='lab', password='lab123'):
    """
        Function to power off a device. If powering off fails, it retries up to three times.
        Args:
            mgmt_ip (str): The management IP of the device.
            port (int, optional): The port to connect to. Defaults to 22.
            user (str, optional): The username to connect with. Defaults to 'lab'.
            password (str, optional): The password to connect with. Defaults to 'lab123'.
    """
    for attempt in range(3):
        try:
            with Device(host=mgmt_ip, port=int(port), user=user, password=password) as dev:
                sw = SW(dev)
                sw.poweroff()
                break  # If the command was successful, exit the loop early
        except (ConnectError, ConnectTimeoutError, SSHException) as err:
            print(f'Attempt {attempt + 1} failed with error: {err}')
            time.sleep(3)  # Wait for 3 seconds before trying again


def handle_load_baseline(mgmt_ip, port, user, password, baseline_config):
    """
        Function to load a baseline configuration to a device. If loading fails, an error message is printed.
        Args:
            mgmt_ip (str): The management IP of the device.
            port (int): The port to connect to.
            user (str): The username to connect with.
            password (str): The password to connect with.
            baseline_config (str): The URL of the baseline configuration.
    """
    try:
        with Device(host=mgmt_ip, port=int(port), user=user, password=password) as dev:
            with Config(dev, mode='exclusive') as cu:
                try:
                    cu.load(url=baseline_config, overwrite=True)
                    cu.commit()
                except (RpcError, Exception) as err:
                    print("Unable to load configuration changes: {0}".format(err))
                except (ConfigLoadError, Exception) as err:
                    print("Unable to load configuration changes: {0}".format(err))
    except (ConnectionError, ConnectTimeoutError, ConnectRefusedError, SSHException, EOFError) as err:
        print(f'Cannot connect to device: {err}')
    except Exception as err:
        print(f'An unexpected error occurred: {err}')


def handle_create_baseline_config(mgmt_ip, port, user, password):
    """
        Function to create a baseline configuration for a device. If creation fails, an error message is printed.
        Args:
            mgmt_ip (str): The management IP of the device.
            port (int): The port to connect to.
            user (str): The username to connect with.
            password (str): The password to connect with.
    """

    for i in range(3):  # Will attempt to connect up to three times
        try:
            dev = Device(host=mgmt_ip, port=int(port), user=user, password=password)

            ss = StartShell(dev)
            ss.open()
            ss.run("cli -c 'show configuration | save baseline.conf'")
            ss.close()

            # If the connection was successful, break the loop
            break
        except (ConnectionError, ConnectTimeoutError, NoValidConnectionsError) as err:
            print(f'Cannot connect to device: {err}')
            print("------------->>>> Try performing Option 11: Create Router baseline config or investigate it further")

            print("-- Waiting 3 seconds before try again")
            time.sleep(3) # If connection fails, wait for 3 seconds before trying again
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            print("------------->>>> Try performing Option 11: Create Router baseline config or investigate it further")
            break


def handle_save_config_local(mgmt_ip, port, user, password, hostname):
    """
        This function saves the current configuration of a network device to a local file.

        Args:
            mgmt_ip (str): The management IP address of the device to connect to.
            port (int): The port to use when connecting to the device.
            user (str): The username to use when authenticating with the device.
            password (str): The password to use when authenticating with the device.
            hostname (str): The hostname of the device, used in the name of the backup file.
    """
    try:
        with Device(host=mgmt_ip, port=int(port), user=user, password=password) as dev:
            config = dev.rpc.get_config(options={'format': 'set'})
            with open(f'bkp_config/{hostname}_config.set', 'wb') as f:
                f.write(etree.tostring(config))
    except (ConnectionError, ConnectTimeoutError, ConnectRefusedError, SSHException) as err:
        print(f'Cannot connect to device: {err}')