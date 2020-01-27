from wpkit.basic import json_load,json_dump
from wpkit.piu import BackupDB
db=BackupDB('D:\work\wpkit\data\db')
info=db.get("fund_infos")
db.set('all_funds',info)
print(info)
