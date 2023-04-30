import numpy as np
import random as rt
from enum import Enum


class Error_model_type(Enum):
    """
    Тип распределения для эмуляции ошибок
    """
    BINOMIAL= 1 # Биномиальный (ошибки независимы)
    HILBERT = 2 # Модель Гильберта ()

"""
Биномиальное распределение
"""

# def generate_binomial_error_flow_from_string(message, error_probability=0.1):
#     """
#     Генерация потока ошибок основываясь на полученном сообщении
#     :param message: Полученное сообщение
#     :param error_probability: Настройка вероятности получения ошибки
#     :return: Поток ошибок
#     """
#     len_message = len(message) * 7
#     return (np.random.rand(len_message) > 1 - error_probability).astype(int)


def generate_binomial_error_flow_from_packages(received_packages, error_probability=0.1):
    """
    Генерация потока ошибок для пакетов на основе биномиального распределения
    :param received_packages: Полученные пакеты
    :param error_probability: Настройка вероятности получения ошибки
    :return: Поток ошибок
    """
    count_bit_in_packages = sum([len(x[0]) for x in received_packages])
    return (np.random.rand(count_bit_in_packages) > 1 - error_probability).astype(int)

"""
Модель Гильберта
"""

def generate_hilbert_error_flow_from_packages(received_packages, err_probability, p00, p11):
    """
    Генерация потока ошибок для пакетов на основе биномиального распределения
    :param received_packages: Полученные пакеты
    :param error_probability: Вероятность ошибки в плохом состоянии
    :param p00: Вероятность остаться в хорошем состоянии
    :param p01: Вероятность остаться в плохом состоянии
    :return: Поток ошибок
    """
    channel = []
    length = sum([len(x[0]) for x in received_packages])
    flag = True  # флаг состояния, True - хорошее, False - плохое
    true_err1 = 0 # фактические вероятности ошибки
    true_err2 = 0
    for i in range(length):
        t = rt.random() # случайное число для определения вероятности перехода из одного состояния в другое
        if flag == True:        
            if t >= p00:  # переход в плохое состояние
                flag = False
                true_err1 = rt.random() 
                if true_err1 <= err_probability:  # вероятность получения ошибки
                    channel.append(1)
                else:
                    channel.append(0)
            else:  # остаться в хорошем состоянии
                channel.append(0)
        else:
            if t >= p11:  # возвращение в хорошее
                flag = True
                channel.append(0)
            else:  # остаться в плохом состоянии
                true_err2 = rt.random()
                if true_err2 <= err_probability:  # вероятность получения ошибки
                    channel.append(1)
                else:
                    channel.append(0)

    count = 0.0
    for i in range(len(channel)):
        if channel[i] == 1:
            count += 1
    err_probability_real = count / len(channel)  # итоговая вероятность ошибки в канале
    # return err_probability_real
    return np.array(channel)



"""
Общие и вспомогательные подпрограммы
"""
def improse_errors_on_data(received_packages, received_error_flow):
    """
    Накладывается поток ошибок на пакеты данных
    :param received_packages:
    :param received_error_flow:
    :return: Возвращаем пакеты с ошибками
    """
    k = 0
    for el_package in range(len(received_packages)):
        for code_msg in range(len(received_packages[el_package][0])):
            if received_error_flow[k]:
                a = received_packages[el_package][0][code_msg]
                received_packages[el_package][0][code_msg] = 1 - received_packages[el_package][0][code_msg]
            k += 1
    return received_packages