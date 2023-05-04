# result = 200
# dan = 25
#
# for i in range(200):
#     if i <= dan:
#         result = (int)(result * 1.1)
#     elif dan < i:
#         result = result+(4000-result)//dan
#     if i % dan == 0 and i != 0:
#         result = 1000 + (i * 10)
#         print()
#     print(i, " : ", result)

speed = 200
rpm = 4000

for i in range(200):
    if(speed >0):
        speed -= 1
        if (i%5 ==0):
            speed -= 1
        if(rpm > 200 and speed!= 0):
            rpm = rpm - ((rpm-200)//speed)
        else:
            rpm = 200

    print(speed, " : ", rpm)
