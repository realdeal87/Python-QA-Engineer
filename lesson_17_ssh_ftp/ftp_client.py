import argparse
import ftplib
import os


def interactive_mode(args):
    """Функция обеспечивает интерактивный режим FTP-клиента"""
    print(f"This script provides yor permission to FTP-server {args.host}")
    while True:
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
                       "Type any command for exit ")
        if choice == "1":
            print(connection.list_remote_folder())
            folder = input("Enter a name of remote folder to create: ")
            connection.create_remote_folder(folder)
        elif choice == "2":
            connection.list_remote_folder()
            folder = input("Enter a name of remote folder to delete: ")
            connection.delete_remote_folder(folder)
        elif choice == "3":
            connection.list_remote_folder()
            folder = input("Change remote folder: ")
            connection.change_remote_folder(folder)
        elif choice == "4":
            list_locale_folder()
            folder = input("Enter a name of local folder to create: ")
            os.mkdir(folder)
        elif choice == "5":
            list_locale_folder()
            folder = input("Enter a name of local folder to delete: ")
            os.rmdir(folder)
        elif choice == "6":
            list_locale_folder()
            folder = input("Change local folder: ")
            os.chdir(folder)
        elif choice == "7":
            files = input("Choose files to download from server: ")
            connection.download_files(files)
        elif choice == "8":
            files = input("Choose files to upload to server: ")
            connection.upload_files(files)
        else:
            break


def list_locale_folder():
    """Функция для вывода списка файлов в текущем локальном каталоге"""
    for file in os.listdir("."):
        print(file)


class FTPConnection:
    """Класс обеспечивает взаимодействие с FTP-сервером"""

    def __init__(self, host, user, passw, port):
        self.ftp = ftplib.FTP()
        result = self.ftp.connect(host, port)
        print(result)
        result = self.ftp.login(user, passw)
        print(result)

    def list_remote_folder(self):
        """Метод для вывода списка файлов в текущем удаленном каталоге"""
        return self.ftp.retrlines('list')

    def create_remote_folder(self, folder):
        """Метод для создания удаленного каталога"""
        self.ftp.mkd(folder)

    def delete_remote_folder(self, folder):
        """Метод для удаления удаленного каталога"""
        self.ftp.rmd(folder)

    def change_remote_folder(self, folder):
        """Метод для изменения текущего удаленного каталога"""
        self.ftp.cwd(folder)

    def download_files(self, files):
        """Метод для выгрузки файлов в локальную папку"""
        filenames = self.ftp.nlst(files)
        print(filenames)
        for filename in filenames:
            try:
                with open(filename, 'wb') as local_file:
                    self.ftp.retrbinary('RETR ' + filename, local_file.write)
            except ftplib.error_perm:
                pass

    def upload_files(self, files):
        """Метод для загрузки файлов в удаленную папку"""
        if files == "":
            filenames = [file for file in os.listdir(".")]
        else:
            filenames = list(files.split(" "))
        print(filenames)
        for filename in filenames:
            try:
                with open(filename, 'rb') as remote_file:
                    self.ftp.storbinary('STOR ' + filename, remote_file)
            except ftplib.error_perm:
                print("Хоп хей лалалей")
                pass

    def conn_close(self):
        """Метод для закрытия соединения"""
        result = self.ftp.quit()
        print(result)
        result = self.ftp.close()
        print(result)


if __name__ == "__main__":
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
    print(arguments)
    connection = FTPConnection(arguments.host, arguments.user,
                               arguments.passw, arguments.port)
    print(f"Hello, {arguments.user}!")
    interactive_mode(arguments)
    connection.conn_close()
