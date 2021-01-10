alist=["a", "b", "c", "d", "e", 0, "g"]
alist[3:6] = [''.join(map(str,alist[3:6]))]
print(alist)