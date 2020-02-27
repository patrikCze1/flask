from fl import db
from fl.models import Post
from flask_login import current_user


def checkUnapprovedPosts():
    #if current_user.role is 0:
    posts = Post.query.filter_by(approved=False)
    return posts

    #return None