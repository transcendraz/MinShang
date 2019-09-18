print 1+9*9
print 1+2*2
print 1+2

print
a='hello'
b='hi';   c='q'; d= 'ok'
e=a+c
print e
print 'q' in e
print 'i' in e
print e[0:100:2]

a=['h','e','l','l','o']
print a
a.append('k')
a.insert(2, 'd')
a.remove('o')
print a.index('l',4,5)
print a
a.sort()
print a 
print 

f={'name':'raz','age':19}
e=dict(name='ok', age= 32)
print e.items()
print e['name']
e['name']='nota'
print e['name']
'''
a = dict(one=1, two=2, three=3)
b = {'one': 1, 'two': 2, 'three': 3}
c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
d = dict([('two', 2), ('one', 1), ('three', 3)])
e = dict({'three': 3, 'one': 1, 'two': 2})
a == b == c == d == e
'''

print f['name']
print len(f)
print 

f=7
print f
while f<31:
    f*=2
    print f,
    if f==28: break
print 

i=7.28
while i<=10: 
    print i,
    i+=1
    if i>8:
        print i,
        i-=7
    elif i<6:
        print i,
        i+=1
    else:
        print i
        break
print

class what:
    num=55
    supnum=8
    total=55+8
    top='wxy'
    gender='female'
    def say(self):
        return 'i am groot'

Groot=what()
print Groot.num
print Groot.supnum
print Groot.say()
print Groot.top
Groot.gender='male'
print Groot.gender
print
