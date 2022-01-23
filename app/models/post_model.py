from flask import jsonify
import pymongo
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["posts_db"]

class PostsDb:
    
    def __init__(self, id, title, author, tags, content):
        self.id = id
        self.created_at = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.updated_at = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content
    

    @staticmethod
    def get_post_model(where = None):
        data_list = db.posts.find(where)        
        return list(data_list)

    def post_model(self):
        db.posts.insert_one(self.__dict__)

    @staticmethod
    def put_model(id, where):
        data = db.posts.find_one({"id": id})
        db.posts.update_one(data, {"$set": {"updated_at": str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), **where}})
    
    @staticmethod
    def delete_model(id):
        db.posts.delete_one({"id": id})
    
    



