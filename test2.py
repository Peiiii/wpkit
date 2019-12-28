from wpkit.services import LocalFSServer

app=LocalFSServer(__name__,path="./")
print(app.url_map)
app.run(port=8000)