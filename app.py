from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_list.db'
db = SQLAlchemy(app)


class Blog(db.Model):
    # For creating blog posts as objects who's properties are stored in the database
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(5000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Blog %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        blog_content = request.form['content']
        new_blog = Blog(content=blog_content)

        try:
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your blog post'

    else:
        blogs = Blog.query.order_by(Blog.date_created).all()
        return render_template('index.html', blogs=blogs)


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

    if request.method == 'POST':
        blog.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your blog post'

    else:
        return render_template('update.html', blog=blog)


if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()
