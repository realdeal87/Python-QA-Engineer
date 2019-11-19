import argparse
import logging
import paramiko


def interpretator_mode(args, log):
    print(f"Script runs in interpretator mode. You can execute commands on "
          f"remote host {args.host} by means ssh connection. "
          f"Type 'quit' or 'exit' to stop.")
    while True:
        command = input("> ")
        if command in ("exit", "quit"):
            break
        result = execute_command(args, command)
        log.info(result)


def interactive_mode(args):
    print(f"This script helps you to setup FTP server on "
          f"remote host {args.host} by means ssh connection.")
    while True:
        print("\nChoose your option(1-4):\n"
              "1) Install vsftpd FTP-server\n"
              "2) Change FTP-server port\n"
              "3) Add new user\n"
              "4) Delete user\n"
              "5) Restart FTP-Server and exit\n"
              "For exit without restart input other command")
        choice = input()
        if choice == "1":
            install_vsftpd(args, logger)
            configure_vsftpd(args, logger)
        elif choice == "2":
            change_port(args, logger)
        elif choice == "3":
            add_user(args, logger)
        elif choice == "4":
            del_user(args, logger)
        elif choice == "5":
            restart_server(args, logger)
            break
        else:
            break


def install_vsftpd(args, log):
    result = execute_command(args, "which vsftpd")
    log.info(result)
    if not result:
        print("Installing vsftpd...")
        result = execute_command(args, "sudo apt-get install vsftpd")
        log.info(result)
        result = execute_command(args, "sudo systemctl start vsftpd")
        log.info(result)
        result = execute_command(args, "sudo systemctl enable vsftpd")
        log.info(result)
        print("Server vsftpd installed!")
    else:
        print("Server vsftpd already installed!")


def configure_vsftpd(args, log):
    config = """listen=NO
                listen_ipv6=YES
                anonymous_enable=NO
                local_enable=YES
                write_enable=YES
                local_umask=022
                dirmessage_enable=YES
                use_localtime=YES
                xferlog_enable=YES
                connect_from_port_20=YES
                chroot_local_user=YES
                secure_chroot_dir=/var/run/vsftpd/empty
                pam_service_name=vsftpd
                rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
                rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
                ssl_enable=NO
                pasv_enable=Yes
                pasv_min_port=10000
                pasv_max_port=10100
                allow_writeable_chroot=YES""".split()
    while True:
        choice = input("Configure /etc/vsftpd.conf? [Y/n] ")
        if choice == "Y":
            print("Configurating...")
            result = execute_command(args, "sudo cp /dev/null /etc/vsftpd.conf")
            log.info(result)
            for line in config:
                command = "sudo bash -c 'echo " + line + " >> /etc/vsftpd.conf'"
                result = execute_command(args, command)
                log.info(result)
            print("Server configurated!")
            break
        elif choice == "n":
            break
        else:
            print("Type 'Y' or 'n'")


def change_port(args, log):
    result = execute_command(args, "which vsftpd")
    log.info(result)
    if result:
        port = input("Input FTP-server port(Default: 20) ")

        try:
            int(port)
        except ValueError:
            print("Used default port: 20")
            param = "listen_port=20"
        else:
            print("Used port: " + port)
            param = "listen_port=" + port

        command = "sudo sed -i '/connect_from_port_20=YES/ i\\" + param + "' /etc/vsftpd.conf"
        log.debug(command)
        result = execute_command(args, "sudo sed -i '/^listen_port=/d' /etc/vsftpd.conf")
        log.info(result)
        result = execute_command(args, command)
        log.info(result)
    else:
        print("You need install vsftpd before!")


def add_user(args, log):
    name = input("Enter username: ")
    checkout = "cat /etc/passwd | grep ^" + name
    result = execute_command(args, checkout)
    log.info(result)
    if not result:
        passw = input("Enter password : ")
        confirmpass = input("Confirm password : ")
        if passw == confirmpass:
            result = execute_command(args, "sudo groupadd ftp_users")
            log.info(result)
            command = "sudo useradd -p " + passw + " -s /bin/bash -G ftp_users -m " + name
            result = execute_command(args, command)
            log.info(result)
            # result = execute_command(args, "chmod 555 /home/user")
            print("User " + name + " created!")
        else:
            print("Password incorrect.")
    else:
        print("This user already exists.")


def del_user(args, log):
    name = input("Enter user to delete: ")
    checkout = "cat /etc/group | grep ^ftp_users\.*\\" + name
    log.debug(checkout)
    result = execute_command(args, checkout)
    log.info(result)
    if result:
        confirm = input("ATTENTION! Home directory and all files of user " + name +
                        "will be deleted! Type Y to confirm! ")
        if confirm == "Y":
            command = "sudo deluser " + name + "; sudo rm -rf /home/" + name
            result = execute_command(args, command)
            log.info(result)
        else:
            print("No user deleted")
    else:
        print("No such a user created by this script")


def restart_server(args, log):
    result = execute_command(args, "which vsftpd")
    log.info(result)
    if result:
        print("Server restarting...")
        result = execute_command(args, "sudo service vsftpd restart")
        log.info(result)
    else:
        print("You need install vsftpd before!")


def execute_command(args, command):
    return SSHConnector(args.host, args.user, args.passw, args.port).command(command)


class SSHConnector:
    """Класс для создания соединения по SSH и отправки команд"""

    def __init__(self, host, user, secret, port=22):
        self.secret = secret
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=host, username=user, password=secret, port=port)
        self.channel = self.client.get_transport().open_session()
        self.channel.set_combine_stderr(True)
        self.channel.get_pty()

    def command(self, command):
        """Метод для выполнения команды"""
        self.channel.exec_command(command)
        stdin = self.channel.makefile('wb', -1)
        stdout = self.channel.makefile('rb', -1)
        if command.startswith("sudo"):
            stdin.write(self.secret + "\n")
            stdin.flush()
        result = stdout.read().decode("utf-8")
        self.channel.close()
        self.client.close()
        return result


if __name__ == "__main__":

    logger = logging.getLogger("ssh_client")
    logger.setLevel(logging.DEBUG)
    shr = logging.StreamHandler()
    shr.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    shr.setFormatter(formatter)
    logger.addHandler(shr)

    parser = argparse.ArgumentParser()

    parser.add_argument("--host", "-s",
                        action="store",
                        help="Host address",
                        required=True)

    parser.add_argument("--user", "-u",
                        action="store",
                        help="Username",
                        required=True)

    parser.add_argument("--passw", "-p",
                        action="store",
                        help="Password",
                        required=True)

    parser.add_argument("--port", "-r",
                        action="store",
                        help="Server SSH port",
                        type=int,
                        default=22)

    parser.add_argument("--imode", "-I",
                        action="store_true",
                        help="Run script in interpretator mode")

    arguments = parser.parse_args()
    print(f"Hello, {arguments.user}!")

    if arguments.imode:
        interpretator_mode(arguments, logger)
    else:
        interactive_mode(arguments)
