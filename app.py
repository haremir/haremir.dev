from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import markdown
from werkzeug.utils import secure_filename

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'gizli-anahtar-buraya')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Upload klasörünü oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Veritabanı modelleri
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    cover_image = db.Column(db.String(200))  # Kapak fotoğrafı için yeni alan

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Blog sayfası
@app.route('/blog')
def blog():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

# Blog yazısı detay sayfası
@app.route('/blog/<slug>')
def blog_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog_post.html', post=post)

# Admin giriş
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Geçersiz kullanıcı adı veya şifre')
    return render_template('admin/login.html')

# Admin çıkış
@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

# Admin paneli
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/dashboard.html', posts=posts)

# Şifre değiştirme
@app.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash('Mevcut şifre yanlış')
            return redirect(url_for('change_password'))
            
        if new_password != confirm_password:
            flash('Yeni şifreler eşleşmiyor')
            return redirect(url_for('change_password'))
            
        current_user.set_password(new_password)
        db.session.commit()
        flash('Şifreniz başarıyla değiştirildi')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/change_password.html')

# Yeni blog yazısı oluşturma
@app.route('/admin/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        slug = title.lower().replace(' ', '-')
        
        # Görsel yükleme
        image_path = None
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename:
                filename = secure_filename(image.filename)
                image_path = os.path.join('uploads', filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        post = Post(title=title, content=content, slug=slug, cover_image=image_path)
        db.session.add(post)
        db.session.commit()
        
        flash('Blog yazısı başarıyla oluşturuldu')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/post_form.html')

# Blog yazısı düzenleme
@app.route('/admin/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.slug = post.title.lower().replace(' ', '-')
        
        # Görsel yükleme
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename:
                filename = secure_filename(image.filename)
                image_path = os.path.join('uploads', filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                # Eski görseli sil
                if post.cover_image:
                    old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(post.cover_image))
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                post.cover_image = image_path
        
        db.session.commit()
        flash('Blog yazısı başarıyla güncellendi')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/post_form.html', post=post)

# Blog yazısı silme
@app.route('/admin/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    
    # Görseli sil
    if post.cover_image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(post.cover_image))
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(post)
    db.session.commit()
    flash('Blog yazısı başarıyla silindi')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload-image', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({
            'location': url_for('static', filename=f'uploads/{filename}')
        })
    
    return jsonify({'error': 'Geçersiz dosya türü'}), 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # İlk admin kullanıcısını oluştur
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')  # Güvenli bir şifre belirleyin
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True) 