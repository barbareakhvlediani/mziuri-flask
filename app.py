from flask import Flask, render_template, redirect, url_for, flash
import sqlite3
from forms import PostForm

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mziuri.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        content TEXT,
                        date_created DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    cursor.close()
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:id>')
def post_detail(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    if post is None:
        return 'Post not found!'
    return render_template('post_detail.html', post=post)


@app.route('/add', methods=('GET', 'POST'))
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        flash('Post added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_post.html', form=form)


@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    if post is None:
        return 'Post not found!'
    form = PostForm(data={'title': post['title'], 'content': post['content']})
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_post.html', form=form)


@app.route('/delete/<int:id>', methods=('POST',))
def delete_post(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('index'))


app.secret_key = 'yufuyfyuf234'

if __name__ == '__main__':
    app.run(debug=True)

