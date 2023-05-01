from matplotlib import pyplot as plt
import numpy as np



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


