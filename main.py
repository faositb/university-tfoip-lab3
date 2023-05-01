import coder
import errors
import specifications
from matplotlib import pyplot as plot


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

flow_errors = 0
for i in range(1, 4):
    '''
    суем текст в пакеты
    '''
    initial_message = "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do."
    print('Исходное сообщение:\n%s' % initial_message)
    enc_message = coder.encode_packages(initial_message, 10)

    '''
    генерируем поток ошибок основываясь на исходных пакетах данных
    '''
    flow_errors = None
    if i == 1:
        print("ИСПОЛЬЗУЕМ БИНОМИАЛЬНУЮ МОДЕЛЬ")
        flow_errors = errors.generate_binomial_error_flow_from_packages(enc_message, 0.1)
    elif i == 2:
        print("ИСПОЛЬЗУЕМ МОДЕЛЬ ГИЛЬБЕРТА")
        flow_errors = errors.generate_hilbert_error_flow_from_packages(enc_message, 0.1, 0.95, 0.8)
    elif i == 3:
        print("ИСПОЛЬЗУЕМ МОДЕЛЬ ПУРТОВА")
        flow_errors = errors.generate_purtova_error_flow_from_packages(enc_message, 0.8, 0.95)#1e100, 2e100)
    print(len(flow_errors), flow_errors.tolist())
    specifications.draw_flow_errors_intervals(flow_errors, errors.Error_model_type(i))
    '''
    накладываем поток ошибок на исходные пакеты
    '''
    enc_message = errors.improse_errors_on_data(enc_message, flow_errors)

    dec_message = coder.decode_packages(enc_message)
    #print(dec_message)
    print('Декодированное сообщение:\n%s' % ''.join(''.join(each[0]) for each in dec_message))

    error_list = coder.find_wrong_packages(dec_message)
    if len(error_list) == 0:
        print('Ошибок при передаче данных не было')
    else:
        print('Ошибки в следующих номерах пакетов:',error_list)

