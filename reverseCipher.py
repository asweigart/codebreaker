# Reverse Cipher
# http://inventwithpython.com/codebreaker (BSD Licensed)

print('Enter the message to encrypted:')
message = input('> ')

encrypted = ''

i = len(message) - 1
while i >= 0:
    encrypted = encrypted + message[i]
    i = i - 1

print(encrypted)