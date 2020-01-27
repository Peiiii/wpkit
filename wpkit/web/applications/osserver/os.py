from wpkit.fsutil import FakeOS
from wpkit.web.apputils import MyBlueprint,parse_json_and_form,\
    StatusError,StatusSuccess,Status,jsonify,request,get_env,Pages

class OSServer(MyBlueprint):
    def __init__(self,url_prefix='/os',default_root_path='./',*args,**kwargs):
        super().__init__(url_prefix=url_prefix,*args,**kwargs)
        self.root_path=default_root_path
        self.os=FakeOS(self.root_path)
        self.root_path=self.os.path
        self.add_handlers()
    def add_handlers(self):
        @self.route('/')
        def do_root():
            return Pages.base.render()

        @self.route('/cmd',methods=['GET','POST'])
        @parse_json_and_form
        def do_cmd(cmd):
            print("cmd:",cmd)
            try:
                res=self.os.execute(cmd)
                return jsonify(StatusSuccess(data=res))
            except:
                if self.debug:
                    raise
                else:
                    return jsonify(StatusError())
        @self.route('/upload',methods=['GET','POST'])
        def do_upload():
            files=request.files
            print(dir(files))
            print(files)
            print(files.keys())

if __name__ == '__main__':
    OSServer(url_prefix='/').run()


