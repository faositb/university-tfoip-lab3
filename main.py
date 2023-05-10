import coder
import errors
import specifications


'''
Пример работы достаточно низкоуровневых подпрограмм
(работают не с пакетами, а просто со строками) из модуля coder
'''
# enc = coder.encode("Hello")
# print(enc[0])
# dec = coder.decode(enc[0])
# print(dec[0])
# coder.DEBUG_check_correctness(enc, dec)

# '''
# А теперь иcказим один бит 
# '''
# enc[0][6] = 1
# dec = coder.decode(enc[0])
# print(dec[0])
# coder.DEBUG_check_correctness(enc, dec)


'''
Пример более высокоуровневой работы
(уже с пакетами) с подпрограммами из модуля coder

'''
# initial_message = "Hello! Russia is the biggest country in the world. It is wached by several oceans. 1234567890"
# print('Исходное сообщение:\n%s' % initial_message)
# enc_message = coder.encode_packages(initial_message, 10)
# #print(enc_message)
# '''
# а теперь немного исказим сообщение enc_message
# '''
# enc_message[1][0][35] = not enc_message[1][0][35]
# enc_message[3][0][8] = not enc_message[3][0][8]

# dec_message = coder.decode_packages(enc_message)
# #print(dec_message)
# print('Декодированное сообщение:\n%s' % ''.join(''.join(each[0]) for each in dec_message))

# error_list = coder.find_wrong_packages(dec_message)
# if len(error_list) == 0:
#     print('Ошибок при передаче данных не было')
# else:
#     print('Ошибки в следующих номерах пакетов:',error_list)

# flow_errors = 0
# for i in range(1, 4):

    # суем текст в пакеты

    # initial_message = "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do. Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do."
    # print('Исходное сообщение:\n%s' % initial_message)
    # enc_message = coder.encode_packages(initial_message, 10)


    # генерируем поток ошибок основываясь на исходных пакетах данных

    # flow_errors = None
    # if i == 1:
    #     print("ИСПОЛЬЗУЕМ БИНОМИАЛЬНУЮ МОДЕЛЬ")
    #     flow_errors = errors.generate_binomial_error_flow_from_packages(enc_message, 0.05)
    # elif i == 2:
    #     print("ИСПОЛЬЗУЕМ МОДЕЛЬ ГИЛЬБЕРТА")
    #     flow_errors = errors.generate_hilbert_error_flow_from_packages(enc_message, 0.1, 0.95, 0.8)
    # elif i == 3:
    #     print("ИСПОЛЬЗУЕМ МОДЕЛЬ ПУРТОВА")
    #     flow_errors = errors.generate_purtova_error_flow_from_packages(enc_message, 0.8, 0.95)#1e100, 2e100)
    # print(len(flow_errors), flow_errors.tolist())
    # specifications.draw_flow_errors_intervals(flow_errors, errors.Error_model_type(i))
    # '''
    # накладываем поток ошибок на исходные пакеты
    # '''
    # enc_message = errors.improse_errors_on_data(enc_message, flow_errors)
    #
    # dec_message = coder.decode_packages(enc_message)
    # #print(dec_message)
    # print('Декодированное сообщение:\n%s' % ''.join(''.join(each[0]) for each in dec_message))
    #
    # error_list = coder.find_wrong_packages(dec_message)
    # specifications.draw_distorted_blocks_intervals(error_list, dec_message, errors.Error_model_type(i))
    # print("Вероятность неправильного приема 1 бита данных = %.3f" % specifications.probability_receiving_wrong_bit(flow_errors))
    # print("Вероятность неправильного приема символа p = %.3f" % specifications.probability_receiving_wrong_symbol(initial_message, ''.join(''.join(each[0]) for each in dec_message)))
    # print("Вероятность неправильного приема блока длиной 10 символов = %.3f" % specifications.probability_receiving_wrong_block(initial_message, flow_errors, 10))
    # print("Коэффициент группирования ошибок = %.3f" % specifications.group_coefficient(flow_errors, 10))
    #
    #
    # if len(error_list) == 0:
    #     print('Ошибок при передаче данных не было')
    # else:
    #     print('Ошибки в следующих номерах пакетов:',error_list)


def main():
    while True:
        print('1. Ввод строки с клавиатуры.\n2. Чтение текста из файла.\n3. Использовать строку по умолчанию.')
        resource_text = int(input('Ваш выбор... '))
        initial_message = ''
        if resource_text == 1:
            initial_message = input("Ваша строка: ")
        elif resource_text == 2:
            with open('files/sample.txt', 'r') as file:
                initial_message = file.read().replace('\n', '').replace('\r', '')
        elif resource_text == 3:
            initial_message = "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do. Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do."
        else:
            break

        enc_message = coder.encode_packages(initial_message, 10)

        print('Генерация потока ошибок:\n1. Биноминальный способ.\n2. Модель Гильберта.\n3. Модель Пуртова.\n4. Все сразу. По очереди. Со стандартными вероятностями.')
        view_err_generate_flow = int(input('Ваш выбор... '))
        f = False
        k_iter = 1
        if view_err_generate_flow == 1:
            p1 = float(input('Вероятность возникновения ошибки при передачи бита (0 < p < 1): '))
            flow_errors = errors.generate_binomial_error_flow_from_packages(enc_message, p1) # 0.05
        elif view_err_generate_flow == 2:
            p1 = float(input('Вероятность возникновения ошибки в плохом состоянии (0 < p < 1): '))
            p2 = float(input('Вероятность остаться в хорошем состоянии (0 < p < 1): '))
            p3 = float(input('Вероятность остаться в плохом состоянии (0 < p < 1): '))
            flow_errors = errors.generate_hilbert_error_flow_from_packages(enc_message, p1, p2, p3) # 0.1, 0.95, 0.8
        elif view_err_generate_flow == 3:
            p1 = float(input('Нижняя граница плотности вероятности по возникновению ошибки в пакете (0 < p < 1): '))
            p2 = float(input('Верхняя граница плотности вероятности по возникновению ошибки в пакете (0 < p < 1): '))
            flow_errors = errors.generate_purtova_error_flow_from_packages(enc_message, p1, p2) # 0.8, 0.95
        elif view_err_generate_flow == 4:
            f = True
            k_iter = 3
        else:
            break

        for k in range(1, k_iter + 1):
            enc_message = coder.encode_packages(initial_message, 10)
            if f:
                if k == 1:
                    flow_errors = errors.generate_binomial_error_flow_from_packages(enc_message, 0.005)
                elif k == 2:
                    flow_errors = errors.generate_hilbert_error_flow_from_packages(enc_message, 0.02, 0.99, 0.9)
                elif k == 3:
                    flow_errors = errors.generate_purtova_error_flow_from_packages(enc_message, 0.05, 0.1)
            print('Исходное сообщение:\n%s' % initial_message)
            if f:
                view_err_generate_flow = k
            specifications.draw_flow_errors_intervals(flow_errors, errors.Error_model_type(view_err_generate_flow))
            enc_message = errors.improse_errors_on_data(enc_message, flow_errors)
            dec_message = coder.decode_packages(enc_message)

            print('Декодированное сообщение:\n%s' % ''.join(''.join(each[0]) for each in dec_message))
            error_list = coder.find_wrong_packages(dec_message)
            specifications.draw_distorted_blocks_intervals(error_list, dec_message, errors.Error_model_type(view_err_generate_flow))
            print("Вероятность неправильного приема 1 бита данных = %.7f" % specifications.probability_receiving_wrong_bit(
                flow_errors))
            print("Вероятность неправильного приема символа p = %.7f" % specifications.probability_receiving_wrong_symbol(
                initial_message, ''.join(''.join(each[0]) for each in dec_message)))
            print(
                "Вероятность неправильного приема блока длиной 10 символов = %.7f" % specifications.probability_receiving_wrong_block(
                    initial_message, flow_errors, 10))
            print("Коэффициент группирования ошибок = %.3f" % specifications.group_coefficient(flow_errors, 10))
            print(f"Относительная скорость передачи канала: {specifications.count_flow_rate(dec_message, flow_errors):.7f}")
            if len(error_list) == 0:
                print('Ошибок при передаче данных не было')
            else:
                print('Ошибки в следующих номерах пакетов:', error_list)


if __name__ == "__main__":
    main()