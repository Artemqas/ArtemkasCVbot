import random

ran = random.randint(1,3)
print(ran)
mess = str(input())
if mess == str(ran):
    print('good')
else: print('try again')
