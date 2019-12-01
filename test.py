import wpkit
from wpkit.web import bps
app=wpkit.web.get_default_app(__name__)
app.register_blueprint(bps.bp_pan.bp_pan(app,url_prefix='/pan'))