# from wpkit.fsutil import Folder,FakeOS
from wpkit.gitspace import GitSpace,open_default
from wpkit.basic import get_time_formated
g=open_default('space','test2')
print('branch:',g.active_branch())
def update():
    folder = g.openFolder('folder')
    dic = folder.openFieldict('readme.txt')
    if not dic.get('time', None):
        dic.time = []
    dic.time.append(get_time_formated() + '\n')
    dic.print()
    dic._save()
# g.branch_create_empty('test2')
# g.push(branch='test2')
# g.pull(branch='empty')
# g.checkout_branch('test2')
# folder=g.openFolder('data')
# dic=folder.openFieldict('config.json')
# dic.time=get_time_formated()

#g.push()
print('branches:',g.branch_list())
print('branch:',g.active_branch())
g.status()
