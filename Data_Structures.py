#lists
#arrays
test_list = []
what = [1, 2, 3, 4]
for i in range(len(what)):
    test_list.append(what[i])

# #print(test_list[1:len(test_list)])
# what = []
# print(what)
# print(test_list)

#sets
#dict
test_dict = {'gray': 6, 'pink': 3, 'red' : 3, 'blue' : 2, 'green' : 3, 'white' : 1, 'black' : 4}
print(test_dict)

#sorts the dict alphabetically, then sort it by value, the items stay in alphabetical order if they have the same value
sort_key = dict(sorted(test_dict.items(), key=lambda x:x[0]))
sort_both = dict(sorted(sort_key.items(), key=lambda x:x[1], reverse=True))
print(sort_key)
print(sort_both)

# #print out all the items
# for item in numb_dict.items():
#     print(item)
# #print out all the keys
# for color in numb_dict.keys():
#     print(color)
# #print out all the values
# for value in numb_dict.values():
#     print(value)

# sorts the dict in reverse order
reverse_copy = dict(reversed(list(test_dict.items())))
#sort the dict in reverse alphabetically
alpha_reverse_copy = dict(sorted(test_dict.items(), reverse=True))
print(reverse_copy)
print(alpha_reverse_copy)


#queue
#set