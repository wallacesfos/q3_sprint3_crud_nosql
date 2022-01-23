from flask import jsonify, Flask
from app.controllers.posts_controller import get_post_controller, create_post_controller, delete_post_controller, patch_post_controller, JsonNotAccepted
import json
from bson import json_util

from app.exc import ValueNullError
from app.models.post_model import PostsDb


def posts_route(app: Flask):

    @app.get('/posts')
    def read_posts():
        data = get_post_controller()
        return {"data": json.loads(json_util.dumps(data))}

    @app.get('/posts/<id>')
    def read_posts_by_id(id):
        try:
            data = get_post_controller(int(id))
            return {"data": json.loads(json_util.dumps(data))}
        except ValueNullError as err:
            return {"error": f"{err}"}, 404
        except Exception as err:
            return {"error": f'{err}'}, 400
    
    @app.post('/posts')
    def create_post():
        return create_post_controller(), 201
    
    @app.delete('/posts/<id>')
    def delete_post(id):
        try:
            data = get_post_controller(int(id))
            delete_post_controller(int(id))
            return {"data": json.loads(json_util.dumps(data))}
        except ValueNullError as err:
            return {"error": f'{err}'}, 404
    
    @app.patch('/posts/<id>')
    def update_post(id):
        try:
            data = patch_post_controller(int(id))
            return {"data": json.loads(json_util.dumps(data))}, 200
        except ValueNullError as err:
            return {"error": f"{err}"}, 404
        except JsonNotAccepted as err:
            return {"error": f"{err}"}, 400


        

        