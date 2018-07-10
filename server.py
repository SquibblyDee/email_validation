from flask import Flask, render_template, request, redirect, flash
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
    print("Fetched all friends", all_emails, "\n")
    return render_template('index.html', emails = all_emails)

@app.route('/process', methods=['POST'])
def create():
    all_emails = mysql.query_db("SELECT * FROM emails")
    query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
    data =  {
            'email': request.form['emailInput'],
            }
    if '@' not in data['email']:
        flash('Email is not valid!')
        print("DATA", data['email'])
        return redirect('/')
    elif data['email'] not in all_emails:
        for email in all_emails:
            print("DATA[email]", data['email'])
            print("DATA LOOPX", data)
            print("EMAILS", all_emails)
            for val in email:
                if data['email'] not in str(email[val]):
                    print("SUCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCEEEEEEEEEEEEEEEEEEEEEEEESSSSSSSSSSSSSSSSSSSSSSSSSSSs")
                    mysql.query_db(query, data)
                    return render_template('/success.html', emails = all_emails) 
                else:
                    flash('Email already exists!')
                    return redirect('/')
        print("DATA[email]", data['email'])
        print("DATA", data)
        print("EMAILS", all_emails)
        # return redirect('/')
    # else:
        # all_emails = mysql.query_db("SELECT email, created_at FROM emails")
        # print("Fetched all friends", all_emails, "\n")
        # mysql.query_db(query, data)
        # return render_template('/success.html', emails = all_emails)

@app.route('/success')
def success():
    query = "DISPLAY * FROM emails"
    mysql.query_db(query)
    print("QUERY", query)

if __name__ == "__main__":
    app.run(debug=True)