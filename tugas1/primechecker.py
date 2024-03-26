num = int(input(""))

if num == 1:
    print("Not Prime")
elif num > 1:
   # check for factors
   for i in range(2,num):
       if (num % i) == 0:
           print("Not Prime")
           break
   else:
       print("Prime")

else:
   print("Not Prime")