from matplotlib import pyplot as plt
import numpy as np



def draw_flow_errors_intervals(flow_err, type_model, len_interval=10):
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

'''
не доделано, славка ушел завтракать
'''
def draw_distorted_blocks_intervals(list_err_package, type_model):
    indexes = np.arange(len(list_err_package))
    presence_errors = []
    plt.bar(indexes, list_err_package)
    plt.xticks(indexes)
    plt.xlabel("Номера пакетов")
    plt.ylabel('Наличие ошибок')
    plt.title(type_model)
    plt.show()


