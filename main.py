import coder

enc = coder.encode("Hello!")
print(enc[0])
dec = coder.decode(enc[0])
print(dec[0])
coder.check_correctness(enc, dec)

'''
А теперь изказим один бит 
'''
enc[0][6] = 1
dec = coder.decode(enc[0])
print(dec[0])
coder.check_correctness(enc, dec)
