from wpkit.gitspace import GitSpace,open_default,Store,default_remote_location,GitRepo,clone,Repo,is_git_dir,FakeOS
from wpkit.fsutil import Folder,copy_file,copy_dir,copy_fsitem
from wpkit.piu import FileDict
from wpkit.basic import T,TMetaClass,CONST_TYPE
import os,shutil,glob
from wpkit.ofile import SimpleListFile
_T=CONST_TYPE
class CONST(metaclass=TMetaClass):
    remote_branch_list=_T()
    master=_T()
    empty=_T()

class StoreItem(Folder):
    def status(self,repo=None):
        repo=repo or self.repo
        from wpkit.basic import PointDict
        info=PointDict(
            current_branch=repo.active_branch(),
            local_branches=repo.branch_list(),
            status=repo.status()
        )
        print(info)
        return info
    def __init__(self,path,remote_location=None,remote_branch=None):
        remote_location = remote_location or default_remote_location
        assert remote_branch
        if not os.path.exists(path):
            os.makedirs(path)
        path=os.path.abspath(path)
        Folder.__init__(self,path)
        if is_git_dir(path):
            repo=GitRepo(path)
        else:
            repo=GitRepo.init(path)
        self.repo=repo
        self.path=path
        self.remote_location=remote_location or default_remote_location
        self.remote_branch=remote_branch
        self.data_list=['.git','.type.store'] # clean except
        self.info_list=['.git','.type.store','.more.store']  # copy except
        self.typefile=self.openFiledict('.type.store')
        self.special_branches=['master','empty','remote_branch_list']
        self.init_branches()
    def _pull_remote_branch_list(self,repo=None,remote_location=None,remote_branch='remote_branch_list',hard=False):
        repo=repo or self.repo
        remote_location=remote_location or self.remote_location
        pull=False
        if not 'remote_branch_list' in repo.branch_list():
            repo.branch_create('remote_branch_list')
            pull=True
        if hard:
            pull=True
        if pull:
            br = repo.active_branch()
            repo.checkout_branch('remote_branch_list')
            repo.clean()
            repo.add_all()
            repo.commit()
            repo.pull(remote_location, branch=remote_branch)
            repo.checkout_branch(br)

    def init_branches(self,repo=None):
        '''
        A store repo has 3 branches: master , empty , remote_branch_list, remote_branch
        '''
        repo=repo or self.repo
        if not repo.branch_list():
            repo.commit() # create master
        if not 'empty' in repo.branch_list():
            repo.branch_create('empty')
            repo.checkout_branch('empty')
            repo.clean()
            repo.commit()
            repo.checkout_branch('master')
        if not self.remote_branch in repo.branch_list():
            repo.branch_create(self.remote_branch)
            repo.checkout_branch(self.remote_branch)
            repo.clean()
            repo.commit()
            repo.checkout_branch('master')
        self._pull_remote_branch_list(hard=False)
        repo.checkout_branch(self.remote_branch)

    def _read_remote_branch_list(self,pull=False):
        repo=self.repo
        br = repo.active_branch()
        repo.checkout_branch(CONST.remote_branch_list)
        if pull:
            self._pull_remote_branch_list(repo)
        lf = self.openSimplelistfile(CONST.remote_branch_list)
        li = lf.read()
        repo.checkout_branch(br)
        return li
    def _add_to_remote_branch_list(self,branch):
        repo=self.repo
        br=repo.active_branch()
        self._pull_remote_branch_list()
        repo.checkout_branch(CONST.remote_branch_list)
        # repo.pull(self.remote_location,CONST.remote_branch_list)
        lf=self.openSimplelistfile(CONST.remote_branch_list)
        li=lf.read()
        print("original:",li)
        li.append(branch)
        li=list(set(li))
        print("now:",li)
        lf.write(li)
        repo.add_all()
        repo.commit()
        repo.push(self.remote_location,CONST.remote_branch_list)
        repo.checkout_branch(br)
    def iter_contentpath(self):
        lis=[]
        for name in self.listdir():
            if name in self.info_list:
                continue
            else:
                path=self.path+'/'+name
                lis.append(path)
        return lis
    def set_type(self,type):
        self.typefile.type=type
        return type
    def get_type(self):
        if not self.typefile.get('type'):
            return None
        return self.typefile.type
    @classmethod
    def pull(cls,remote_location=None,remote_branch=None,path=None,overwrite=False):
        remote_location=remote_location or default_remote_location
        remote_branch=remote_branch or 'master'
        if os.path.exists(path) and len(os.listdir(path)):
            if overwrite:
                shutil.rmtree(path)
            else:
                raise FileExistsError("Can't pull because folder %s is not empty."%(path))
        if not os.path.exists(path):
            os.makedirs(path)
        repo=GitRepo.init(path)
        if not repo.branch_list():
            repo.add_all()
            repo.commit()
        if not remote_branch in repo.branch_list():
            repo.branch_create(remote_branch)
            repo.checkout_branch(remote_branch)
            repo.clean()
        repo.pull(remote_location,branch=remote_branch)
        item=cls(repo.path,remote_location=remote_location,remote_branch=remote_branch)
        type=item.get_type()
        if not type:
            type=item.set_type(T.FOLDER)
            import logging
            logging.warning('StoreItem %s has no type, so we set it as %s'%(item.path,type))
        if type==T.FOLDER:
            return StoreFolder(repo.path,remote_location=remote_location,remote_branch=remote_branch)
        else:
            assert type==T.FILE
            return StoreFile(repo.path,remote_location=remote_location,remote_branch=remote_branch)
    @classmethod
    def openStorefolder(cls,path,remote_location=None,remote_branch=None,force_pull=False,overwrite=False):
        remote_location=remote_location or default_remote_location
        if not is_git_dir(path):
            force_pull=True
        if not force_pull:
            item=StoreFolder(path,remote_location=remote_location,remote_branch=remote_branch)
        else:
            item=StoreFolder.pull(remote_location=remote_location,remote_branch=remote_branch,path=path,overwrite=overwrite)
        return item
    @classmethod
    def openStorefile(cls,path,remote_location=None,remote_branch=None,force_pull=False,overwrite=False):
        remote_location=remote_location or default_remote_location
        if not is_git_dir(path):
            force_pull=True
        if not force_pull:
            item=StoreFile(path,remote_location=remote_location,remote_branch=remote_branch)
        else:
            item=StoreFile.pull(remote_location=remote_location,remote_branch=remote_branch,path=path,overwrite=overwrite)
        return item
    def upload(self,remote_location=None,remote_branch=None,overwrite=True):
        # Todo:get remote branch list
        remote_loacation=remote_location or self.remote_location
        remote_branch=remote_branch or self.remote_branch
        assert remote_loacation and remote_branch
        assert remote_branch !='master'
        repo=self.repo
        repo.add_all()
        repo.commit()
        # br=repo.active_branch()
        if not remote_branch in repo.branch_list():
            repo.branch_create(remote_branch)
        repo.checkout_branch(remote_branch)
        repo.push(remote_loacation,remote_branch)
        # repo.checkout_branch(br)
        if not remote_branch in self._read_remote_branch_list():
            self._add_to_remote_branch_list(remote_branch)
    @classmethod
    def export(cls,path,remote_branch,remote_location=default_remote_location,name=None,cache_dir='.tmp',overwrite=False):
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        def _export_dir(obj,path,cache_dir):
            for p in obj.iter_contentpath():
                copy_fsitem(p, path)
            more = obj.morefile.copy()
            # obj.rmself()
            for name, br in more.items():
                br_cache_dir=cache_dir+'/'+br
                cls.export(path, remote_location=remote_location, remote_branch=br, name=name, cache_dir=br_cache_dir,overwrite=overwrite)
        this_dir=cache_dir+'/.this'
        obj=StoreItem.pull(remote_location=remote_location,remote_branch=remote_branch,path=this_dir)
        name = name or remote_branch
        if isinstance(obj,StoreFolder):
            if not os.path.exists(path):
                os.makedirs(path)
            assert os.path.isdir(path)
            path=path+'/'+name
            if os.path.exists(path):
                if overwrite:
                    shutil.rmtree(path)
                else:
                    raise Exception("Can't export to %s because path already existed and overwrite is not True")
            os.mkdir(path)
            _export_dir(obj,path,cache_dir)
        else:
            assert isinstance(obj,StoreFile)
            if os.path.exists(path):
                assert os.path.isdir(path)
                if name:
                    path=path+'/'+name
                ps=obj.iter_contentpath()
                ps.sort()
                p=ps[0]
                copy_fsitem(p, path)

            else:
                for p in obj.iter_contentpath():
                    copy_fsitem(p, path)
            # obj.rmself()
        # shutil.rmtree(cache_dir)


    def clean(self):
        names=self.listdir()
        for name in names:
            if name in self.data_list:
                continue
            self.remove(name)

class StoreFolder(StoreItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.morefile = self.openFiledict('.more.store')
        self.set_type(T.FOLDER)
    def addmore(self,name,branch):
        self.morefile[name]=branch
    def eatStore(self,path,name=None,remote_location=None,remote_branch=None,upload=True,overwrite=False,cache_dir='.tmp'):
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        os.makedirs(cache_dir)
        assert os.path.exists(path)
        if not name:
            name=os.path.basename(os.path.abspath(path))
        remote_location = remote_location or self.remote_location
        assert remote_location
        if not remote_branch:
            assert self.remote_branch
            remote_branch=self.remote_branch+'-'+name
        if upload:
            uploadStoreitem(path,remote_location=remote_location,remote_branch=remote_branch,cache_dir=cache_dir)
        self.morefile[name]=remote_branch

class StoreFile(StoreItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_type(T.FILE)
def uploadStoreitem(path,remote_location, remote_branch,cache_dir):
    assert os.path.exists(path)
    if os.path.isdir(path):
        tmp = StoreFolder(cache_dir,remote_location=remote_location,remote_branch=remote_branch)
    else:
        tmp =StoreFile(cache_dir,remote_location=remote_location,remote_branch=remote_branch)
    tmp.clean()
    if os.path.isfile(path):
        tmp.eat(path)
    else:
        for p in os.listdir(path):
            p=path+'/'+p
            tmp.eat(p)
    tmp.upload(remote_location=remote_location, remote_branch=remote_branch)
    # tmp.rmself()








