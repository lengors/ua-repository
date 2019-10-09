

dic = {"ola" : {123 : [2], 143 : [1]}, "adeus" : {144 : [1]}, "aa" : {132 : [1], 983 : [2], 132 : [3]}}

print(max(dic, key = lambda word : len(dic[word])))

