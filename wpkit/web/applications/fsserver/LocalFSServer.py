from flask import jsonify
from flask_cors import CORS
import json
from wpkit.pan import LocalFSHandle,Pan
from wpkit.web.base import MyBlueprint,Application
from wpkit.web.utils import parse_json,parse_json_and_form,request
from wpkit.web.resources import get_template_by_name
from wpkit.basic import Status,StatusError,StatusSuccess,PointDict


class LocalFSServer(MyBlueprint):
    def __init__(self,import_name='__main__',path="./",url_prefix="/fs",nickname="LocalFSServer",*args,**kwargs):
        super().__init__(import_name=import_name,url_prefix=url_prefix,nickname=nickname,*args,**kwargs)
        self.fs=LocalFSHandle(path=path)
        self.add_handlers()
    def add_handlers(self):
        @self.route('/',methods=['POST','GET'])
        def do_root():
            return get_template_by_name('pan').render()
        @self.route('/cmd',methods=['POST','GET'])
        @parse_json_and_form
        def do_cmd(cmd):
            print("cmd:", cmd)
            try:
                res = self.fs.execute(cmd)
                res = StatusSuccess(data=res)
            except:
                res = StatusError()
                return res
            return jsonify(res)
        @self.route('/upload',methods=['POST','GET'])
        @parse_json_and_form
        def do_upload(info):
            file=request.files['file']
            if isinstance(info,str):
                info=json.loads(info)
            info=PointDict.from_dict(info)
            path=self.fs.local_path(info.location)
            path=self.fs.local_path(path+'/'+info.filename)
            file.save(path)
            print('path:',path)
            print('file:',file)
            return StatusSuccess(msg="Uploading succeeded.")
        self.config_statics({
            "/files":self.fs.lpath
        })
        def getUrl(location,name):
            return 'http://%s:%s'%(self.host,self.port)+ self.url_prefix+'/files/'+self.fs.local_path(location+'/'+name)
        self.fs.add_cmd('getUrl',getUrl)

if __name__ == '__main__':
    fs=LocalFSServer(url_prefix="/fs")
    fs.run()




