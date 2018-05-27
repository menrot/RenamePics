import math

def get_primes(input_list):
    return (element for element in input_list if is_prime(element))


# not germane to the example, but here's a possible implementation of
# is_prime...

def is_prime(number):
    if number > 1:
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        for current in range(3, int(math.sqrt(number) + 1), 2):
            if number % current == 0: 
                return False
        return True
    return False


Mylist = [5, 17, 19, 24]
OutList = get_primes(Mylist)
for i in OutList:
    print i


print "End"
