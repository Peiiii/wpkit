from wpkit.fsutil import FakeOS

os=FakeOS('./')
x=os.listdir('./')
x=os.info('./',format=True).print()
print(x)