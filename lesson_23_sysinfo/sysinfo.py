"""Модуль для сбора информации о системе"""
import os
import subprocess
import sys

params = ["apache2", "80", "python", "."]
try:
    params[0] = sys.argv[1]
    params[1] = sys.argv[2]
    params[2] = sys.argv[3]
    params[3] = sys.argv[4]
except IndexError:
    print("Usage: python", sys.argv[0],
          "service port package path\n"
          "Script will use next values:", params)

# Сетевые интерфейсы
print("\nNetwork interfaces:")
grep_proc = subprocess.Popen(["grep", "-v", "Kernel"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
subprocess.call(["netstat", "-i"], stdout=grep_proc.stdin)
ifaces, ifaces_err = grep_proc.communicate()
ifaces = ifaces.decode()
print(ifaces)

# Маршрут по умолчанию
print("Default route:")
grep_proc = subprocess.Popen(["grep", "-P", "Destination|default"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
subprocess.Popen(["netstat", "-r"], stdout=grep_proc.stdin)
route, route_err = grep_proc.communicate()
route = route.decode()
print(route)

# Информация о состоянии процессора
print("CPU Info:")
cpu = subprocess.call(["lscpu"])

# Информация о процессе
print("\nCurrent process:")
c_proc = subprocess.call(["ps", str(os.getpid())])

# Список всех процессов
print("\nAll processes:")
a_proc = subprocess.call(["ps", "-a"])

# Статистика работы сетевых интерфейсов
print("\nInterfaces statistic:")
i_stat = subprocess.call(["cat", "/proc/net/dev"])

# Статус работы сервиса apache2
print("\n" + params[0] + " status:")
service_status = subprocess.call(["systemctl", "status", params[0]])

# Состояние сетевого порта 80/TCP на сервере localhost
print("\n" + params[1] + "/TCP status on localhost:")
grep_proc = subprocess.Popen(["grep", "-A1", "PORT"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
subprocess.Popen(["nmap", "-p", params[1], "localhost"], stdout=grep_proc.stdin)
port_status, port_status_err = grep_proc.communicate()
port_status = port_status.decode()
print(port_status)

# Версия пакета
print(params[2] + " package version:")
package_version = subprocess.call([params[2], "--version"])

# Список файлов в директории
print("\nList of files in:", params[3])
print(os.listdir(path=params[3]))

# Текущая директория
print("\nCurrent directory")
print(os.getcwd())

# Версия ядра
print("\nKernel version:")
print(os.uname()[2])

# Версия операционной системы
print("\nSystem version:")
print(os.uname()[0], os.uname()[3])
