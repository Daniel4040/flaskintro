from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
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


@app.route('/', methods=['POST', 'GET'])
def index():
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
            return redirect('/')
        except:
            return 'There was an issue adding your blog post'

    else:
        return render_template('index.html')


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
    category = Category.query.get_or_404(id)  # this could be the wrong id

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


@app.route('/blog/')
def blog():
    blogs = Blog.query.order_by(Blog.date_published).all()
    return render_template('blog.html', blogs=blogs)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
