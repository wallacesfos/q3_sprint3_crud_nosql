from unittest.mock import patch
from webbrowser import get
from flask import request, jsonify
from app.models.post_model import PostsDb
from app.exc import ValueNullError, JsonNotAccepted
import os
import json

def get_post_controller(id = None):
    if id != None:
        response = PostsDb.get_post_model({"id": id})
        
        if response == []:
            raise ValueNullError("Post não existe")

        return response
    else:
        return PostsDb.get_post_model() 


def create_post_controller():
    id = None
    if not os.path.exists("./ids.json"):
        with open("./ids.json", 'w') as ids_file:
            json.dump(1, ids_file)
            id = 1
    else: 
        with open("./ids.json", 'r') as ids_file:
            id = json.load(ids_file) + 1
        
        with open("./ids.json", 'w') as ids_file:
            json.dump(id, ids_file)
        
    data = request.get_json()
    poster = PostsDb(id, **data)
    poster.post_model()

    data["id"] = id
    return data


def delete_post_controller(id):
    PostsDb.delete_model(id)


def patch_post_controller(id):
    data = request.get_json()
    params = ["author", "content", "tags", "title"]
    verification = False

    for key, value in data.items():
            for i in params:
                if key == i:
                    verification = True
                
    if not verification:
        raise JsonNotAccepted("O JSON deve conter apenas esses: 'author', 'content', 'tags', 'title'")

    response = PostsDb.get_post_model({"id": id})
        
    if response == []:
        raise ValueNullError("Post não existe")

    for key, item in data.items():
        PostsDb.put_model(id, {key: item})

    response = get_post_controller(id)

    return {"data": response}
    