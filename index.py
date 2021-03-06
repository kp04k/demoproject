from flask import Flask, session, redirect, url_for, escape, request, render_template
import mysql.connector

# Create an instance of the Flask class that is the WSGI application.
app = Flask(__name__)

#   DATABASE CONFIG   #
db = mysql.connector.connect(host="maintenancedemo-mysqldbserver.mysql.database.azure.com", user="mysqldbuser@maintenancedemo-mysqldbserver", password="Mytestpwd1", database="maintenance_db")
cur = db.cursor()

@app.route('/')
def index():
    if 'username' in session:
        cur.execute("SELECT asset_code, asset_name, asset_status, installed_date, commissioned_date, last_inspected_date, inspected_employee_name FROM assets;") # Fetch data from ASSETS table
        data = cur.fetchall()        
        return render_template('index.html', data=data)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT COUNT(1) FROM users WHERE user_id = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT user_password FROM users WHERE user_id = %s;", [username_form]) # FETCH PASSWORD
            for row in cur.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
     app.run('localhost', 4449)
#    app.run(debug=True)