import re
import full_list_VGK

x = re.findall("\((\S*)", full_list_VGK.list)
print(x)
print("Elements in list: ", len(x))
