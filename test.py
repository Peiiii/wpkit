import wpkit
from wpkit.piu import Piu
from wpkit.basic import PointDict
# import os
t=wpkit.basic.DirTree('./')
t.pprint2()
info=t.path().info()
print(PointDict.from_dict(info).pprint2())
# print(os.path.exists('./'))
# t.print_size()
# p=t.geta('path')
# # print(p.exists())
# print(t.geta('path').getatime())
