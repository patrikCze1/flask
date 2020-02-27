from flask import Blueprint, render_template, url_for, request, redirect, flash, abort, session
from flask_login import current_user, login_required
from fl import db
from fl.models import Post
from fl.posts.forms import CreatePost, UpdatePost
from fl.admin.utils import checkUnapprovedPosts

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def createPost():
    form = CreatePost()
    if request.method == 'POST' and form.validate_on_submit():
        #print(form.category.data)
        post = Post(title=form.title.data, content=form.text.data, author=current_user, category_id=form.category.data.id)
        db.session.add(post)
        db.session.commit()
        flash('Post was send to approval', 'success')

        posts = checkUnapprovedPosts().count()
        session['newPostNotify'] = posts
        return redirect(url_for('main.home'))
    else:
        print(session['newPostNotify'])
        return render_template('./post/create.html', title='New post', form=form)


@posts.route('/post/<int:id>')
def showPost(id):
    post = Post.query.get_or_404(id)
    return render_template('./post/show.html', title='Post', post=post)


@posts.route('/post/update/<int:id>', methods=['GET', 'POST'])
@login_required
def updatePost(id):
    form = UpdatePost(request.form)
    post = Post.query.get_or_404(id)
    if request.method == 'POST' and form.validate():
        post.title = form.title.data
        post.content = form.text.data
        db.session.commit()#save
        flash('Post has been updated', 'success')
        return redirect(url_for('posts.showPost', id=id))
    else:
        form.title.data = post.title
        form.text.data = post.content
        return render_template('./post/update.html', title='Update post', form=form, id=id)


@posts.route('/post/delete/<int:id>')
@login_required
def deletePost(id):
    post = Post.query.get_or_404(id)
    if current_user.id == post.author.id:
        db.session.delete(post)
        db.session.commit()
        flash('Post has been deleted', 'success')
        return redirect(url_for('main.home'))
    else:
        abort(403)
        #flash('You dont have rights for this action', 'danger')
        #return redirect(url_for('home'))
#todo metoda pro posty

@posts.route('/post/waiting/')
@login_required
def waitingPosts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(approved=False).paginate(page=page, per_page=5)
    return render_template('./post/waiting.html', title='Waiting posts', posts=posts)
#todo notifikace
#admin.required
@posts.route('/post/approve/<int:id>')
@login_required
def approvePost(id):
    post = Post.query.get(id)
    post.approved = True
    db.session.commit()
    flash('Post has been approved', 'success')
    posts = checkUnapprovedPosts().count()
    session['newPostNotify'] = posts
    return redirect(url_for('posts.waitingPosts'))