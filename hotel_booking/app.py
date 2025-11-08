from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --- Create DB and table ---
def init_db():
    conn = sqlite3.connect("hotel.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  room_no TEXT,
                  days INTEGER,
                  amount REAL)''')
    conn.close()

init_db()

# --- Home page: show all bookings ---
@app.route('/')
def index():
    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings")
    data = cur.fetchall()
    conn.close()
    return render_template("index.html", bookings=data)

# --- Add booking ---
@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        room = request.form['room']
        days = int(request.form['days'])
        amount = days * 1000  # ₹1000 per day
        conn = sqlite3.connect("hotel.db")
        conn.execute("INSERT INTO bookings(name, room_no, days, amount) VALUES(?,?,?,?)",
                     (name, room, days, amount))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("add.html")

# --- Edit booking ---
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        room = request.form['room']
        days = int(request.form['days'])
        amount = days * 1000
        conn.execute("UPDATE bookings SET name=?, room_no=?, days=?, amount=? WHERE id=?",
                     (name, room, days, amount, id))
        conn.commit()
        conn.close()
        return redirect('/')
    cur.execute("SELECT * FROM bookings WHERE id=?", (id,))
    data = cur.fetchone()
    conn.close()
    return render_template("edit.html", booking=data)

# --- Delete booking ---
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect("hotel.db")
    conn.execute("DELETE FROM bookings WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# --- Print Bill ---
@app.route('/bill/<int:id>')
def bill(id):
    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings WHERE id=?", (id,))
    data = cur.fetchone()
    conn.close()
    if not data:
        return "No such booking!"
    return render_template("bill.html", booking=data)

if __name__ == '__main__':
    app.run(debug=True)
