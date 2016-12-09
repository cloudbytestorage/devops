import sys

x = int(sys.argv[1])

if x == 1:
    list1 = []
else:
    list1 = ['Mardan']
try:
    a = list1[0]
except IndexError:
    print "Out of index"
    exit()
print a
