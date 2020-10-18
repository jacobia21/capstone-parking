from flask import current_app
import paramiko
from scp import SCPClient


def get_pi_image(ip_address, username, password, port=22):
    try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address,port,username,password)

        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport())

        file_dir = '/home/pi/Desktop/{}'.format(ip_address)

        scp.get(file_dir, recursive=True)


        scp.close()
    except Exception as error:
        current_app.logger.info(type(error.__name__))
        current_app.logger.info(error)