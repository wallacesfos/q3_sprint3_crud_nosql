from flask import Flask

def init_app(app: Flask):
    from app.views.posts_route import posts_route
    posts_route(app)