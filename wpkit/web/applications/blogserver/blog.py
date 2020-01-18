from wpkit.web.base import  MyBlueprint
from wpkit.web.resources import get_env
from wpkit.web import resources
from wpkit.piu import Piu
from wpkit.basic import Path,DirPath,standard_path,PowerDirPath,get_relative_path
from flask import send_file
import os



class BlogServer(MyBlueprint):
    def __init__(self,url_prefix='/blogs',default_root_path='data/blogs',data_path="data/blogs",nickname='Blogs', *args,**kwargs):
        super().__init__(url_prefix=url_prefix,nickname=nickname,*args,**kwargs)

        self.data_path=Path(data_path)
        self.db_path=self.data_path/'db'
        self.db=Piu(path=self.db_path)
        default_root_path=os.path.abspath(default_root_path)
        self.db.set('root_path',default_root_path)
        self.add_handlers()
    def add_handlers(self):
        @self.route('/', defaults={'req_path': ''})
        @self.route('/<path:req_path>')
        def do_route(req_path):
            print('reqpath:',req_path)
            root_path=self.db.get('root_path')
            print("root_path:",root_path)
            real_path=root_path+'/'+req_path if req_path!='' else root_path
            real_path=PowerDirPath(real_path)
            print("real_path:",real_path)
            basename=real_path.basename()
            if basename.startswith('view='):
                real_path=real_path.dirname()/basename[len('view='):]
                print("real_path:",real_path)
                if real_path.isdir():
                    return self.do_view_dir(real_path)
                else:
                    return self.do_view_file(real_path)
            else:
                if real_path.isdir():
                    return self.do_send_dir(real_path)
                elif real_path.isfile():
                    return self.do_send_file(real_path)
            return 'not finished.'
    def do_send_file(self,path):
        return send_file(path)
    def do_send_dir(self,path):
        rel_path,names,urls,_=self.parse_dir_path(path)
        items = dict(zip(names, urls))
        return resources.Pages.links.render(links=items)
    def do_view_file(self,path):
        if path.endswith('.md'):
            tem=self.get_template('view_md.tem',os.path.dirname(path))
            return tem.render(markdown_data=PowerDirPath(path)())
        elif path.endswith('.txt') or \
                path.endswith('.json') or \
                path.endswith('.bat') or \
                path.endswith('.sh') or \
                path.endswith('.js') or \
                path.endswith('.css') or \
                path.endswith('.py'):
            tem=self.get_template('view_file.tem',os.path.dirname(path))
            return tem.render(text_data=PowerDirPath(path)())
        else:
            return self.do_send_file(path)
    def do_view_dir(self,path):
        rel_path,names,_,urls=self.parse_dir_path(path)
        items = dict(zip(names, urls))
        print('items:', items)

        if 'index.html' in names:
            return send_file(path+'/'+'index.html')
        if "index.tem" in names:
            tem=self.get_template("index.tem",path)
            return  tem.render(links=items)
        elif "index.md" in names:
            tem=self.get_template('sys/index.tem',path)
            return tem.render(body=PowerDirPath(path+'/index.md')())
        return resources.Pages.links.render(links=items)
    def get_template(self,name,dir=None):
        env=get_env(path=dir)
        try:
            tem=env.get_template(name)
        except:
            print("template not found:",name)
            return None
        return tem
    def parse_dir_path(self,path):
        root_path = Path(self.db.get('root_path'))
        root_path=standard_path(root_path)
        path=standard_path(path)
        rel_path = get_relative_path(root_path,path)
        rel_path_url=self.get_url(rel_path)
        rel_dir = os.path.dirname(rel_path)
        rel_dir_url = self.get_url(rel_dir)
        path = DirPath(path)
        names = path.list()
        vnames = ['view=' + i for i in names]
        view_urls = [standard_path(rel_path_url+'/' + vname) for vname in vnames]
        urls=[standard_path(rel_path_url+'/'+name) for name in names]
        return rel_path,names,urls,view_urls





