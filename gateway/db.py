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

# test = Run.create(id=114, data='{"test": "data", "test2": 34}')

# print(test)

# tes2 = Run.get(id=114)

# test3 = tes2.data.decode("utf-8")

# print(json.loads(test3))

# print(json.loads(test3)["test2"])

db.close()


# grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))