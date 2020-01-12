def test():
    from wpkit.linux import clean_port, get_local_ip
    from wpkit.web.applications.demo import demo, DemoApp, LocalFSServer, MyBlueprint
    app=DemoApp(__name__)
    app.sitemap['Download']='http://%s:%s'%(get_local_ip(),8001)
    app.register_blueprint(LocalFSServer(nickname="ManageDownloads",url_prefix="/manage_download",path="D:/work"))
    print(app.url_map)
    app.run(host=get_local_ip(),port=80)

test()