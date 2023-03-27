from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .forms import CreatePostForm, UpdatePostForm
from ..models import Post

ig = Blueprint('ig', __name__, template_folder='ig_templates')

@ig.route('/posts/create', methods=['GET', 'POST'])
@login_required
def createPost():
    form = CreatePostForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            body = form.body.data

            new = Post(title, img_url, body, current_user.id)
            new.savePost()
            print('NEW POST MADE!!!!')
            return redirect(url_for('homePage'))

    return render_template('create_post.html', form=form)

@ig.route('/posts/feed')
@login_required
def feed():
    posts = Post.query.order_by(Post.date_created).all()[::-1]
    print(posts)
    return render_template('feed.html', posts=posts)


@ig.route('/posts/<int:post_id>')
def indPost(post_id):
    post = Post.query.get(post_id)
    if post:
        return render_template('post.html', p=post)
    else:
        return redirect(url_for('ig.feed'))
    
@ig.route('/posts/update/<int:post_id>', methods=['GET', 'POST'])
def updatePost(post_id):
    post = Post.query.get(post_id)
    if post.user_id != current_user.id:
        flash('Hey buddy, this is not yours to modify!')
        return redirect(url_for('ig.feed'))

    form = UpdatePostForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            body = form.body.data

            post.title = title
            post.img_url = img_url
            post.body = body
            print(post.title, post.body)
            post.saveChanges()

            return redirect(url_for('ig.indPost', post_id=post.id))

    return render_template('update_post.html', form=form, post=post)

@ig.route('/posts/delete/<int:post_id>')
def deletePost(post_id):
    post = Post.query.get(post_id)
    if post.user_id == current_user.id:
        post.deletePost()
    else:
        print("You cannot delete a post that isn't yours")
    return redirect(url_for('ig.feed'))