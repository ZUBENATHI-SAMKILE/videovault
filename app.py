from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from flask import send_from_directory
from datetime import datetime
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "name-secrete"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'videos')


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    videos = db.relationship('Video', backref='owner', lazy=True)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form["email"]
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('register'))
        
    
        if not username or not email or not password or not confirm_password:
            flash("All fields are required!")
            return redirect(url_for("register"))

        try:
            valid = validate_email(email)
            email = valid.email  
        except EmailNotValidError as e:
            flash(f"Invalid email: {str(e)}")
            return redirect(url_for("register"))
        

        if User.query.filter_by(email=email).first():
            flash("Email already taken.")
            return redirect(url_for('register'))
        
        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Account created! Please log in.")
        return redirect(url_for('login'))
    return render_template("register.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
    return render_template("login.html")


@app.route('/dashboard')
@login_required
def dashboard():
    videos = Video.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", videos=videos)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['video']
    title = request.form.get("title")

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        new_video = Video(filename=file.filename, title=title, user_id=current_user.id)
        db.session.add(new_video)
        db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/delete/<int:video_id>', methods=['POST'])
@login_required
def delete(video_id):
    video = Video.query.get_or_404(video_id)
    if video.owner != current_user:
        flash("You cannot delete this video!")
        return redirect(url_for("dashboard"))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(video)
    db.session.commit()
    return redirect(url_for("dashboard"))



@app.route('/download/<int:video_id>')
@login_required
def download(video_id):
    video = Video.query.get_or_404(video_id)
    if video.owner != current_user:
        flash("You cannot download this video!")
        return redirect(url_for("dashboard"))

    return send_from_directory(app.config['UPLOAD_FOLDER'], video.filename, as_attachment=True) 


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    if not os.path.exists("site.db"):
        with app.app_context():
            db.create_all()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host="0.0.0.0", port=5000)
 