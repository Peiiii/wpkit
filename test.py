import wpkit
from wpkit import node as n
from wpkit.node import components
from wpkit.web import bps,utils,request,default_templates,resources
from wpkit.web.bps import pan,MyBlueprint
from flask import jsonify
app=wpkit.web.get_default_app(__name__)

# static
# app.add_blueprint(bps.BlueStatic(__name__,name='static',static_dir='./data/assets',url_prefix='/assets'))
# pan
bp_pan=pan.BluePan(__name__)
# @bp_pan.route('/home',methods=['get'])
# def f1():
#     # p=wpkit.basic.DirTree('./data')
#     return resources.get_template_by_name('pan').render()
    # return resources.get_template_by_name('tmp').render()
    # from wpkit.web.bps.pan import pages
    # print(pages.testobj)
    # return pages.panpage.to_string()

# pan get
# @bp_pan.route('/data',methods=['get'])
# @utils.parse_json
# def f2():
#     tree=wpkit.basic.dir_tree('./')
#     return jsonify(tree)


# pan post
# @bp_pan.route('/data',methods=['post'])
# @utils.parse_json
# def f3(cmd):
#     print(cmd)
#     return 'testing'
app.add_blueprint(bp_pan)
# app.sitemap['PanHome']='/pan/home'
# app.sitemap['PanData']='/pan/data'

# test
# bptest=MyBlueprint(name='test',import_name=__name__,url_prefix='/test')
# @bptest.route('/')
# def do():
#     return resources.get_template_by_name('testpage').render()
# app.add_blueprint(bptest)

# # fileupload
# bptest=MyBlueprint(name='FileUpload',import_name=__name__,url_prefix='/upload')
# @bptest.route('/')
# def do3():
#     return resources.get_template_string_by_name('file_upload')
# app.add_blueprint(bptest)
#
# # fileupload2
# bptest=MyBlueprint(name='Vue-FileUpload',import_name=__name__,url_prefix='/vue-upload')
# @bptest.route('/')
# def do2():
#     return resources.get_template_string_by_name('vue-uploader')
# app.add_blueprint(bptest)

print(app.url_map)
print(app.sitemap)
app.run(port=80)