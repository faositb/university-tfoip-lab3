import coder

'''
Пример работы достаточно низкоуровневых подпрограмм
(работают не с пакетами, а просто со строками) из модуля coder
'''
enc = coder.encode("Hello")
print(enc[0])
dec = coder.decode(enc[0])
print(dec[0])
coder.DEBUG_check_correctness(enc, dec)

'''
А теперь изказим один бит 
'''
enc[0][6] = 1
dec = coder.decode(enc[0])
print(dec[0])
coder.DEBUG_check_correctness(enc, dec)


'''
Пример более высокоуровневой работы
(уже с пакетами) с подпрограммами из модуля coder

'''
initial_message = "Hello! Russia is the biggest country in the world. It is wached by several oceans. 1234567890"
print('Исходное сообщение:\n%s' % initial_message)
enc_message = coder.encode_packages(initial_message, 10)
# print(enc_message)
'''
а теперь немного исказим сообщение enc_message
'''
enc_message[1][0][35] = not enc_message[1][0][35]
enc_message[3][0][8] = not enc_message[3][0][8]

dec_message = coder.decode_packages(enc_message)
# print(dec_message)
print('Декодированное сообщение:\n%s' % ''.join(''.join(each[0]) for each in dec_message))

error_list = coder.find_wrong_packages(dec_message)
if len(error_list) == 0:
    print('Ошибок при передаче данных не было')
else:
    print('Ошибки в следующих номерах пакетов:',error_list)