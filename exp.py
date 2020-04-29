from wpkit.gitspace import GitRepo,Folder
from wpkit.gitspace.gitspace import get_default_remote_location
repo_name='HighSchoolLearning'
loc=get_default_remote_location(repo_name)
# clone(loc)
repo=GitRepo(repo_name)
# folder=Folder(repo.path)
# f=folder.open('README.md','w')
# f.write('# '+repo_name)
# f.close()
repo.add_all()
repo.commit()
repo.push(loc,'master')


