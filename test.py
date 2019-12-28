import wpkit
from wpkit import node as n
from wpkit.node import components
from wpkit.web import bps,utils,request,default_templates,resources
from wpkit.web.bps import pan,MyBlueprint
from flask import jsonify
app=wpkit.web.get_default_app(__name__)


bp_pan=pan.BluePan(__name__)

app.add_blueprint(bp_pan)


print(app.url_map)
print(app.sitemap)
app.run(port=80)