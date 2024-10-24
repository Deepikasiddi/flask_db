from flask import Flask,render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    entries = cursor.fetchall()
    conn.close()
    return render_template('index.html',entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
    title = request.form['title']
    content = request.form['content']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entries (title,content) VALUES (?,?)", (title,content))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/int<id>')
def delete_entry(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE id = ?",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   content TEXT NOT NULL
         )
     ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db() 
    app.run(debug=True)    
            