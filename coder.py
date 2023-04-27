import zlib

def encode(str):
    '''
    Переводит строку str в список бит (на каждый символ по 7 бит)
    '''
    bit_list = []
    for symbol in str:
        symbol_code = bin(ord(symbol))[2::].zfill(7)
        for bit in symbol_code:
            bit_list.append(int(bit))
    return (bit_list, zlib.crc32(str.encode('utf-8')))

def decode(bit_list):
    '''
    Переводит список бит в список символов (на каждый символ по 7 бит)
    '''
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

def check_correctness(encoder_list, decoder_list):
    if encoder_list[1] == decoder_list[1]:
        print('Сообщение не было искажено')
    else:
        print('Сообщение исказилось при передаче')
