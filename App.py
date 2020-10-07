from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# Settings
app.secret_key = 'my_secret_key'

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()
    return render_template('index.html', contacts = data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',
            (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added Successfully')
        return redirect(url_for('index'))


@app.route('/edit/<id>')
def get_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'SELECT * FROM contacts WHERE id = {id}')
    data = cursor.fetchone()
    return render_template('edit-contact.html', contact = data)

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contact Updated Successfully')
        return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'DELETE FROM contacts WHERE id = {id}')
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
