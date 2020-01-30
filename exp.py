from wpkit.fsutil import FakeOS

os=FakeOS('./')
x=os.listdir('./')
# x=os.info('./',format=True).print()
# print(x)
# import yaml
# yaml.load()
from  wpkit.basic import standard_path,get_relative_path
# x=standard_path('.')
# print(x)
x=get_relative_path('./data/blogs', './data/blogs/.')
print(x)