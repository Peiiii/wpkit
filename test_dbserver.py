from wpkit.services import DBServer
app=DBServer(__name__,dbpath='./data/dbserver/db')
app.run(port=8001)