import zlib
import numpy as np


def encode_packages(received_str, chars_count):
    """
    Создаёт пакеты из строки str по chars_count символов,
    переводит их в двоичный код и возвращает список из
    кодов и хешей для каждого пакета
    """
    encoded_packages = []
    i = 0
    while i < len(received_str):
        encoded_packages.append(encode(received_str[i:i + chars_count]))
        i += chars_count
    return encoded_packages


def decode_packages(encoded_packages):
    """
    Декодирует пакеты, попутно вычисляя хеши для каждого полученного
    пакета. Возвращает список из декодированных сообщений и хешей, которые
    у них ДОЛЖНЫ быть (если пакет передан без искажений)
    """
    decoded_packages_list = []
    error_list = []
    for each in encoded_packages:
        decoded_package = [decode(each[0])[0], each[1]]
        decoded_packages_list.append(decoded_package)
    return decoded_packages_list


def check_package_correctness(one_package):
    """
    Проверка целостности пакета
    """
    return (zlib.crc32(''.join(one_package[0]).encode('utf-8'))) == one_package[1]

   
def encode(received_str):
    """
    Переводит строку str в список бит (на каждый символ по 7 бит)
    """
    bit_list = []
    for symbol in received_str:
        symbol_code = bin(ord(symbol))[2::].zfill(7)
        for bit in symbol_code:
            bit_list.append(int(bit))
    return [bit_list, zlib.crc32(received_str.encode('utf-8'))]


def decode(bit_list):
    """
    Переводит список бит в список символов (на каждый символ по 7 бит)
    """
    i = 0
    codec = 64
    char_result = 0
    result_list = []
    for i in range(0, len(bit_list), 7):
        for j in bit_list[i:i+7]:
            char_result = char_result + j * codec
            codec = codec // 2
        result_list.append(chr(char_result))
        char_result = 0
        codec = 64
    return (result_list, zlib.crc32(''.join(result_list).encode('utf-8')))


def find_wrong_packages(dec_message):
    """
    Поиск искажённых пакетов
    """
    error_list = []
    for i in range(len(dec_message)):
        if not check_package_correctness(dec_message[i]):
            error_list.append(i)
    return error_list


def DEBUG_check_correctness(encoder_list, decoder_list):
    """
    Для отладки: проверка хешей сообщений
    """
    if encoder_list[1] == decoder_list[1]:
        print('Сообщение не было искажено')
    else:
        print('Сообщение исказилось при передаче')


def generate_error_flow_from_string(message, error_probability=0.1):
    """
    Генерация потока ошибок основываясь на полученном сообщение
    :param message: Полученное сообщение
    :param error_probability: Настройка вероятности получения ошибки
    :return: Поток ошибок
    """
    len_message = len(message) * 7
    return (np.random.rand(len_message) > 1 - error_probability).astype(int)


def generate_error_flow_from_packages(received_packages, error_probability=0.1):
    """
    Генерация потока ошибок основываясь на полученных пакетах
    :param received_packages: Полученные пакеты
    :param error_probability: Настройка вероятности получения ошибки
    :return: Поток ошибок
    """
    count_bit_in_packages = sum([len(x[0]) for x in received_packages])
    return (np.random.rand(count_bit_in_packages) > 1 - error_probability).astype(int)

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
