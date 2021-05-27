import sys


def generator(
        n :int,
        left :int,
        rigth :int,
        s :str):
    
    if (left + rigth == 2 * n):
        print(s)
        return s
    
    if left < n:
        return generator(n=n, left=left+1, rigth=rigth, s=s+'(')
            
    if left > rigth:
        return generator(n=n, left=left, rigth=rigth+1, s=s+')')


def generator_02(n :int):
    if n < 1:
        return []
    elif n == 2:
        return [
            '(())',
            '()()', ]
    l_v = list()
    for x in generator_02(n=n-1):
        l_v.append('({x})'.format(x=x))
        l_v.append('(){x}'.format(x=x))
        l_v.append('{x}()'.format(x=x))
    return tuple(sorted(set(l_v)))


# a_len = sys.stdin.readline().strip()
# print(generator(n=int(a_len), left=0, rigth=0, s=''),)

for x in range(5):
    print("x:", x)
    for y in generator_02(x):
        print(y)
