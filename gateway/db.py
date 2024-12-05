import datetime
import json
from peewee import *

db = SqliteDatabase('sequencing.db')

class BaseModel(Model):
    class Meta:
        database = db

class Run(BaseModel):
    id = IntegerField(primary_key=True)
    created = DateTimeField(default=datetime.datetime.now)
    data = BlobField()

db.connect()

db.create_tables([Run])

db.close()