from wpkit.web.applications.demo import DemoApp
from wpkit.web.applications.blogserver import BlogServer

# bs=BlogServer(url_prefix='/blogs',default_root_path='./')
# bs.run(port=80)

app=DemoApp(__name__)
# app.register_blueprint(bs)
# app.sitemap['ViewBlogs']='/blogs/view='
print(app.url_map)
app.run(port=80)