"""Скрипт считывает значения из файла data.csv в кодировке utf-8,
затем комбинирует их и записывает в файл результаты.txt, согласно шаблону example.txt"""

import csv
import codecs


def csv_parser(csv_data):
    """Функция осуществляет преобразование данных в список, пригодный для комбинирования"""
    reader = list(csv.DictReader(csv_data, delimiter=","))

    list_of_sets = list()
    for _ in reader[0]:
        list_of_sets.append(set())

    for line in reader:
        i = 0
        for key in line.keys():
            if line[key] != "":
                if line[key] == "0":
                    line[key] = "-"
                elif line[key] == "1":
                    line[key] = "+"
                list_of_sets[i].add(line[key].strip())
            i += 1
    return list_of_sets


def file_creator(list_of_data):
    """Функция создает генератор всех комбинаций всех значений всех параметров"""
    writing_list = (name + "\t" + city + "\t" + card + "\t" + deposit + "\t" + mortgage + "\n"
                    for name in list_of_data[0]
                    for city in list_of_data[1]
                    for card in list_of_data[2]
                    for deposit in list_of_data[3]
                    for mortgage in list_of_data[4])
    return writing_list


def file_recorder(list_of_data):
    """Функция осуществляет построчную запись в файл результаты.txt"""
    with open("результаты.txt", "w") as recording_data:
        i = 0
        for record in list_of_data:
            recording_data.write(record)
            i += 1

            # Ограничитель количества записей в файле
            if i == 100:
                break


"""Открывается файл data.csv в кодировке cp1251"""
with codecs.open("data.csv", "r", "cp1251") as encoded_data:
    file_recorder(file_creator(csv_parser(encoded_data)))