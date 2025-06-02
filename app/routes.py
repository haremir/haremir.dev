from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .models import db, Post
from .forms import PostForm

blog = Blueprint('blog', __name__)

@blog.route('/')
def index():
    posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).all()
    return render_template('blog/index.html', posts=posts)

@blog.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('blog/post.html', post=post)

@blog.route('/admin/posts')
@login_required
def admin_posts():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('blog.index'))
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts)

@blog.route('/admin/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('blog.index'))
    
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            tags=form.tags.data,
            author=current_user,
            is_published=form.is_published.data
        )
        
        if form.cover_image.data:
            filename = secure_filename(form.cover_image.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.cover_image.data.save(filepath)
            post.cover_image = filename
        
        db.session.add(post)
        db.session.commit()
        flash('Blog yazısı başarıyla oluşturuldu.', 'success')
        return redirect(url_for('blog.admin_posts'))
    
    return render_template('admin/edit_post.html', form=form)

@blog.route('/admin/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('blog.index'))
    
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.tags = form.tags.data
        post.is_published = form.is_published.data
        
        if form.cover_image.data:
            # Eski resmi sil
            if post.cover_image:
                old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], post.cover_image)
                if os.path.exists(old_filepath):
                    os.remove(old_filepath)
            
            # Yeni resmi kaydet
            filename = secure_filename(form.cover_image.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.cover_image.data.save(filepath)
            post.cover_image = filename
        
        db.session.commit()
        flash('Blog yazısı başarıyla güncellendi.', 'success')
        return redirect(url_for('blog.admin_posts'))
    
    return render_template('admin/edit_post.html', form=form, post=post)

@blog.route('/admin/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('blog.index'))
    
    post = Post.query.get_or_404(post_id)
    
    # Kapak fotoğrafını sil
    if post.cover_image:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], post.cover_image)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.session.delete(post)
    db.session.commit()
    flash('Blog yazısı başarıyla silindi.', 'success')
    return redirect(url_for('blog.admin_posts')) 