"""Скрипт для установки соединения и работы с FTP-сервером"""
import argparse
import ftplib
import logging
import os


def interactive_mode(args, log):
    """Функция для запуска скрипта в интерактивном режиме"""
    print(f"This script helps you to work with FTP-server {args.host}")
    while True:
        try:
            print(f"\nYour current remote folder is: {connection.ftp.pwd()}")
            print(f"Your current local folder is: {os.getcwd()}\n")
            choice = input("Choose your action:\n"
                           "1) Create remote folder\n"
                           "2) Delete remote folder\n"
                           "3) Change remote folder\n"
                           "4) Create local folder\n"
                           "5) Delete local folder\n"
                           "6) Change local folder\n"
                           "7) Download files\n"
                           "8) Upload files\n"
                           "To exit enter any another command\n")
            if choice == "1":
                result = connection.list_remote_folder()
                log.info(result)
                folder = input("\nEnter a name of remote folder to create: ")
                result = connection.create_remote_folder(folder)
                log.info(result)
                print("Remote folder created")
            elif choice == "2":
                result = connection.list_remote_folder()
                log.info(result)
                folder = input("\nEnter a name of remote folder to delete: ")
                result = connection.delete_remote_folder(folder)
                log.info(result)
                print("Remote folder deleted")
            elif choice == "3":
                result = connection.list_remote_folder()
                log.info(result)
                folder = input("\nChoose remote folder: ")
                result = connection.change_remote_folder(folder)
                log.info(result)
                print("Remote folder changed")
            elif choice == "4":
                list_locale_folder()
                folder = input("\nEnter a name of local folder to create: ")
                os.mkdir(folder)
                print("Local folder created")
            elif choice == "5":
                list_locale_folder()
                folder = input("\nEnter a name of local folder to delete: ")
                os.rmdir(folder)
                print("Local folder deleted")
            elif choice == "6":
                list_locale_folder()
                folder = input("\nChoose local folder: ")
                os.chdir(folder)
                print("Local folder changed")
            elif choice == "7":
                files = input("\nChoose files to download from server: ")
                connection.download_files(files, logger)
                print("Download completed")
            elif choice == "8":
                files = input("\nChoose files to upload to server: ")
                connection.upload_files(files, logger)
                print("Upload completed")
            else:
                break
        except (ftplib.error_perm,
                FileExistsError, FileNotFoundError,
                IsADirectoryError, NotADirectoryError) as err:
            log.error(err)
            print("Error. See log.")


def list_locale_folder():
    """Функция для вывода списка файлов в текущем локальном каталоге"""
    for file in os.listdir("."):
        print(file)


class FTPConnection:
    """Класс обеспечивает взаимодействие с FTP-сервером"""

    def __init__(self, host, user, passw, port, log):
        self.ftp = ftplib.FTP()
        result = self.ftp.connect(host, port)
        log.info(result)
        try:
            result = self.ftp.login(user, passw)
            log.info(result)
        except ftplib.error_perm as err:
            log.error(err)
            print("Пользователя не существует или неверный логин и пароль")
            os.abort()

    def list_remote_folder(self):
        """Метод для вывода списка файлов в текущем удаленном каталоге"""
        return self.ftp.retrlines('list')

    def create_remote_folder(self, folder):
        """Метод для создания удаленного каталога"""
        return self.ftp.mkd(folder)

    def delete_remote_folder(self, folder):
        """Метод для удаления удаленного каталога"""
        return self.ftp.rmd(folder)

    def change_remote_folder(self, folder):
        """Метод для изменения текущего удаленного каталога"""
        return self.ftp.cwd(folder)

    def download_files(self, files, log):
        """Метод для выгрузки файлов в локальную папку"""
        filenames = list()
        if files == "":
            pass
        else:
            if files == "*":
                for file in self.ftp.nlst():
                    filenames.append(file)
            else:
                filenames = files.split(" ")
            log.info(filenames)
            for filename in filenames:
                with open(filename, 'wb') as local_file:
                    result = self.ftp.retrbinary('RETR ' + filename, local_file.write)
                    log.info(result)

    def upload_files(self, files, log):
        """Метод для загрузки файлов в удаленную папку"""
        filenames = list()
        if files == "":
            pass
        else:
            if files == "*":
                for file in os.listdir("."):
                    if os.path.isfile(file):
                        filenames.append(file)
            else:
                filenames = list(files.split(" "))
            log.info(filenames)
            for filename in filenames:
                with open(filename, 'rb') as remote_file:
                    result = self.ftp.storbinary('STOR ' + filename, remote_file)
                    log.info(result)

    def conn_close(self, log):
        """Метод для закрытия соединения с FTP-сервером"""
        result = self.ftp.quit()
        log.info(result)


if __name__ == "__main__":

    logger = logging.getLogger("ftp_client")
    logger.setLevel(logging.DEBUG)
    shr = logging.StreamHandler()
    shr.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    shr.setFormatter(formatter)
    logger.addHandler(shr)
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", "-s",
                        action="store",
                        help="FTP-server host",
                        required=True)

    parser.add_argument("--user", "-u",
                        action="store",
                        help="Username",
                        required=True)

    parser.add_argument("--passw", "-p",
                        action="store",
                        help="User password",
                        required=True)

    parser.add_argument("--port", "-r",
                        action="store",
                        type=int,
                        default=21,
                        help="FTP-server port")

    arguments = parser.parse_args()
    connection = FTPConnection(arguments.host, arguments.user,
                               arguments.passw, arguments.port, logger)
    print(f"Hello, {arguments.user}!")
    interactive_mode(arguments, logger)
    connection.conn_close(logger)
