from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_list.db'
db = SQLAlchemy(app)


class Blog(db.Model):
    # For creating blog posts from contents stored in the database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_published = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    category = db.relationship('Category',
                               backref=db.backref('blogs', lazy=True))

    def __repr__(self):
        return '<Blog %r>' % self.id


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return self.name


class User(db.Model):
    # For creating admin users who can post new blogs to the website
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


@app.route('/blog/', methods=['POST', 'GET'])
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']
        blog_category = request.form['category']
        new_category = Category(name=blog_category)
        new_blog = Blog(title=blog_title, content=blog_content,
                        category=new_category)

        try:
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog/')
        except:
            return 'There was an issue adding your blog post'

    else:
        blogs = Blog.query.order_by(Blog.date_published).all()
        return render_template('blog.html', blogs=blogs)


@app.route('/signup/', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        name = request.form['new_name']
        username = request.form['new_username']
        password = request.form['new_password']

        user_db_check = User.query.filter_by(username=username).first()
        if user_db_check is True:
            return redirect('/signup/')

        new_user = User(name=name, username=username,
                        password=generate_password_hash(password, method='sha256'))
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/signup/')
        except:
            return 'There was an issue signing in. Please try again.'

    else:
        return render_template('signup.html')


@app.route('/signin/', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_db_check = User.query.filter_by(username=username).first()

        if user_db_check is None:
            return 'Username does not match our records. Please try again'
        else:
            if user_db_check.password == password:
                return render_template('home.html')
            else:
                return 'Password does not match our records. Please try again'

    else:
        return render_template('signin.html')


@app.route('/delete/<int:id>')
def delete(id):
    blog_to_delete = Blog.query.get_or_404(id)

    try:
        db.session.delete(blog_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that blog post'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    blog = Blog.query.get_or_404(id)
    category = Category.query.get_or_404(id)

    if request.method == 'POST':
        blog.title = request.form['title']
        blog.content = request.form['content']
        category.name = request.form['category']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your blog post'

    else:
        return render_template('update.html', blog=blog)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home/')
def home():
    return render_template('index.html')


@app.route('/blog/')
def blog():
    blogs = Blog.query.order_by(Blog.date_published).all()
    return render_template('blog.html', blogs=blogs)


@app.route('/createblog/')
def createblog():
    return render_template('createblog.html')


@app.route('/videos/')
def videos():
    return render_template('videos.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/signin/')
def signin():
    return render_template('signin.html')


@app.route('/signout')
def signout():
    return 'Signed Out'


@app.route('/signup/')
def signup():
    return render_template('signup.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


if __name__ == "__main__":
    app.run(debug=True)
