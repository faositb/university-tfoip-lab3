import random

import numpy as np
import random as rt
from enum import Enum


class Error_model_type(Enum):
    """
    Тип распределения для эмуляции ошибок
    """
    BINOMIAL= 1 # Биномиальный (ошибки независимы)
    HILBERT = 2 # Модель Гильберта ()
    PURTOV = 3 # Модель Пуртова

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


def generate_binomial_error_flow_from_packages(received_packages, error_probability=0.005):
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
    :param err_probability: Вероятность ошибки в плохом состоянии
    :param p00: Вероятность остаться в хорошем состоянии
    :param p11: Вероятность остаться в плохом состоянии
    :return: Поток ошибок
    """
    channel = []
    length = sum([len(x[0]) for x in received_packages])
    flag = True  # флаг состояния, True - хорошее, False - плохое
    true_err1 = 0 # фактические вероятности ошибки
    true_err2 = 0
    for i in range(length):
        t = rt.random() # случайное число для определения вероятности перехода из одного состояния в другое
        if flag:
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

'''
Модель Пуртова
'''

def generate_purtova_error_flow_from_packages(received_packages, err_probability_low=0.05, err_probability_high=0.1):
    """
    Генерация потока ошибок для пакетов на основе модели Пуртова
    :param received_packages: Полученные пакеты
    :param err_probability_low: Нижняя плотность вероятности для пакета
    :param err_probability_high: Верхняя плотность вероятности для пакета
    :return: Поток ошибок
    """
    err_flow = []
    for i_package in received_packages:
        len_package = len(i_package[0])
        err_probability_package = rt.uniform(err_probability_low, err_probability_high)
        if err_probability_package > 1:
            [err_flow.append(1) for x in range(len_package)]
        else:
            list_err_probability = div_probability_package(err_probability_package, len_package)
            for j_err_probability in rt.sample(list_err_probability, len(list_err_probability)):
                err_flow.append(1 if rt.uniform(0, 1) < j_err_probability else 0)
    return np.array(err_flow)



"""
Общие и вспомогательные подпрограммы
"""


def div_probability_package(received_num,received_length_packages):
    """
    Разбивает плотность вероятностей пакета на вероятности для каждого бита
    :param received_num: собственно число - плотность вероятностей для целого пакета
    :param received_length_packages: - длина (количество) битов в пакете
    :return: список вероятностей для каждого бита
    """
    probability_each_bit = []
    for idx in range(received_length_packages - 1):
        probability_each_bit.append(rt.uniform(1e-20, received_num - sum(probability_each_bit)))
    probability_each_bit.append(received_num - sum(probability_each_bit))
    probability_each_bit[-1] = 1e-20
    return probability_each_bit

def improse_errors_on_data(received_packages, received_error_flow):
    """
    Накладывается поток ошибок на пакеты данных
    :param received_packages: Полученные пакеты данных
    :param received_error_flow: Полученный поток ошибок
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