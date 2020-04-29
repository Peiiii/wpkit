# from wpkit.gitspace.StoreFolder import StoreFolder,StoreFile,StoreItem,Store
from wpkit.gitspace.Store import Store
from wpkit.basic import get_time_formated
from wpkit.utils import SimpleListFile
from wpkit.utils import remove_fsitem


def main():

    # test3()
    # test5()
    # test6()
    # test7()
    # test8()
    # test9()
    # test10()
    # get_font()
    # test11()
    # test12()
    # test13()
    # test14()
    # test15()
    # test16()
    # test17()
    # test18()
    test19()
    # test20()
    pass

def test20():
    store=Store()
def test19():
    store=Store()
    store.get('blogs','blogs',overwrite=True)
def test18():
    store=Store()
    store.get('fonts/msyh.ttf','./',overwrite=True)
def test17():
    store=Store()
    store.set('blogs','data/blogs',recursive=True)


def test16():
    store=Store()
    store.set('fonts/msyh.ttf','./fonts/msyh.ttf')


def test15():
    store=Store()
    # store.sync_keys()
    store.get('fonts/msyh.ttf',overwrite=True)
def test14():
    export('./','wpkit.dist')
def export(path,branch):
    StoreItem.export(path=path,remote_branch=branch)
def test13():
    '''upload imgs'''
    StoreItem.uploadStoreitemRecursive('dist',remote_branch='wpkit.dist')
def test12():
    '''upload imgs'''
    StoreItem.uploadStoreitemRecursive('data',remote_branch='data')
def get_font():
    StoreItem.export('fonts/msyh.ttf',remote_branch='msyh.ttf')

def test11():
    '''upload recursive'''
    StoreItem.uploadStoreitemRecursive('fonts',remote_branch='fonts')
def test10():
    folder = StoreFolder.openStorefolder(path='folder-deploy', remote_branch='folder-deploy',
                                         force_pull=False, overwrite=True)
def test9():
    StoreFolder.export('export',remote_branch='folder',overwrite=True)
def test8():
    folder = StoreFolder.openStorefolder(path='folder', remote_branch='folder',
                                         force_pull=False, overwrite=True)
    folder.eatStore(path='deploy')
    folder.upload()

def test7():
    file=StoreFile.openStorefile(path='msyh', remote_branch='msyh.ttf',
                                         force_pull=False, overwrite=True)
    file.upload()

def test6():
    folder = StoreFolder.openStorefolder(path='remote_branch_list', remote_branch='remote_branch_list',
                                         force_pull=True, overwrite=True)
    repo=folder.repo
    # repo.checkout_branch('remote_branch_list')
    # folder.rmfile('test.json')

    folder.upload()
def test5():
    folder=StoreFolder.openStorefolder(path='folder',remote_branch='folder',
                                       force_pull=False,overwrite=True)
    folder.status()
    add_content(folder)
    folder.upload()
    folder._pull_remote_branch_list()
    repo=folder.repo
    # repo.pull(folder.remote_location,'remote_branch_list')
    x=folder._read_remote_branch_list()
    print(x)
    folder.status()






def add_content(folder):
    dic = folder.openFiledict('test.json')
    if not dic.get('times',None):
        dic.times=[]
    time = get_time_formated()
    dic.times.append(time)
    dic._save()
def add_file(folder):
    from uuid import uuid4
    # folder=StoreFile()
    folder.newfile(uuid4().hex+'.txt')
def test1():
    folder = StoreFolder('./folder',remote_branch='folder')
    repo = folder.repo
    print(dict(repo.refs))
    add_content(folder)
    add_file(folder)
    folder.upload()

def test2():
    StoreFolder.export('export',remote_branch='folder',overwrite=True)
    import os,shutil
def test3():
    folder = StoreFile('./file', remote_branch='file')
    repo = folder.repo
    print(dict(repo.refs))
    add_content(folder)
    folder.upload()
def test4():
    StoreFile.export('export', remote_branch='file', overwrite=True)


if __name__ == '__main__':
    main()
# test1()
# test2()

# test3()
# test4()


# ref='refs/remotes/origin/bgs-1'
# repo.checkout_branch(ref)
#
# a=folder.openFieldict('test.json')
# a.time=get_time_formated()
# folder.upload()
