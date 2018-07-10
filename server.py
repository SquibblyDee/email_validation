from flask import Flask, render_template, request, redirect, flash, session
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key="islandcrabdanceparty"
# invoke the connectToMySQL function and pass it the name of the database we're usingcopy
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('mydb')
# now, we may invoke the query_db method
# print("all the users", mysql.query_db("SELECT * FROM users;"))

@app.route('/')
def index():
    all_emails = mysql.query_db("SELECT * FROM emails")
    # print("Fetched all friends", all_emails, "\n")
    return render_template('index.html', emails = all_emails)

@app.route('/process', methods=['POST'])
def create():
    all_emails = mysql.query_db("SELECT * FROM emails")
    # print("ALL EMAILS: ", all_emails)
    query = "INSERT INTO emails (email, date_created, date_updated) VALUES (%(email)s, NOW(), NOW());"
    data =  {
            'email': request.form['emailInput'],
            }
    # This handles basic form validation only checks for @ sign
    if '@' not in data['email']:
        flash('Email is not valid!')
        return redirect('/')

    # This iterates through all emails returned by the database and returns a flash error if a dupe exists
    for email in all_emails:
        if data['email'] == email['email']:
            flash('Email is already taken!')
            return redirect('/')

    # if none of our errors kick off them render success.html and pass all out emails over for display
    else:
        session['email'] = data['email']
        mysql.query_db(query, data)
        desired_columns = mysql.query_db("SELECT email, date_created FROM emails ORDER BY date_created DESC")
        return render_template('/success.html', emails=desired_columns)


if __name__ == "__main__":
    app.run(debug=True)