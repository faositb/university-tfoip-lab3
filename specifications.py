from matplotlib import pyplot as plt
import numpy as np

import coder


def draw_flow_errors_intervals(flow_err, type_model, len_interval=10):
    """
    Рисуем информацию о том, сколько ошибок в том или ином пакете
    :param flow_err: Поток ошибок
    :param type_model: То по какой модели был создан поток ошибок
    :param len_interval: Количество символов в одном пакете (чтоб длина в битах умножаем на 7)
    :return: ничего важного не возвращаем, только график строим
    """
    err_in_each_package = []
    flow_err = flow_err.tolist()
    len_interval *= 7
    while len(flow_err) > 0:
        if len(flow_err) > len_interval:
            err_in_each_package.append(flow_err[:len_interval + 1].count(1))
            flow_err = flow_err[len_interval + 1:]
        else:
            err_in_each_package.append(flow_err.count(1))
            flow_err = []
    plt.bar(np.arange(0, len(err_in_each_package)), err_in_each_package)
    plt.xticks(np.arange(0, len(err_in_each_package)))
    plt.xlabel("Номера пакетов")
    plt.ylabel('Количество ошибок в пакете')
    plt.title(type_model)
    plt.show()
    return err_in_each_package


def draw_distorted_blocks_intervals(list_err_package, dec_message, type_model, len_interval=10):
    """
    Рисуем информацию, какие пакеты информации были повреждены
    :param list_err_package: Номера пакетов с ошибками
    :param dec_message: Сообщение (в данном случае раскодировано,
     но тут не важно, нужно было просто получить количество пакетов
    :param type_model: То по какой модели был создан поток ошибок
    :param len_interval: Количество символов в одном пакете (чтоб длина в битах умножаем на 7)
    :return: ничего не возвращаем, только график строим
    """
    presence_errors = []
    count_package = len(dec_message)
    for i in range(count_package):
        presence_errors.append(1) if i in list_err_package else presence_errors.append(0)
    indexes = np.arange(len(presence_errors))
    plt.bar(indexes, presence_errors)
    plt.xticks(indexes)
    plt.yticks([0, 1], ['NO', 'YES'])
    plt.xlabel("Номера пакетов")
    plt.ylabel('Наличие ошибок')
    plt.title(f'Информационный поток после {type_model}')
    plt.show()


def probability_receiving_wrong_bit(flow_errors):
    """
    Расчёт вероятности ошибки/неправильного приема символа p
    """
    return np.count_nonzero(flow_errors) / len(flow_errors)


def probability_receiving_wrong_symbol(input_string, decoded_string):
    """
    Расчёт вероятности ошибки/неправильного приема символа p
    """
    p = 0
    for i in range(len(input_string)):
        if input_string[i] != decoded_string[i]:
            p += 1
    return p / len(input_string)


def group_coefficient(flow_errors, block_length):
    """
    Расчёт коэффициента группирования для блока длиной block_length символов
    """
    count = 0
    for i in range(0, len(flow_errors), block_length):
        if np.count_nonzero(flow_errors[i : i + block_length * 7]):
            count += 1
    return abs((np.log(np.count_nonzero(flow_errors)) - np.log(count)) / np.log(block_length * 7))


def probability_receiving_wrong_block(input_string, flow_errors, block_length):
    """
    Расчёт вероятности ошибки/неправильного приема блока длиной block_length символов
    """
    p = 0
    counter = 0
    for i in range(0, len(input_string), block_length):
        if (np.count_nonzero(flow_errors[i:i + block_length * 7])) != 0:
            p += 1
        counter += 1
    return p / counter


# def probability_receiving_wrong_block(input_string, error_list, block_length):
#     """
#     Расчёт вероятности ошибки/неправильного приема блока длиной block_length символов
#     """
#     return len(error_list) / (len(input_string) / block_length)   

def count_flow_rate(flow_with_err, flow_errs):
    v_package = len(coder.find_wrong_packages(flow_with_err))
    n_package = len(flow_with_err)
    k_package = len(flow_errs)
    a_package = 1
    return k_package / ((k_package + 1) + a_package) * (n_package - v_package) / n_package
