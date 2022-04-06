from flask import Flask, render_template, request, redirect
import sqlite3

con = sqlite3.connect('StudentManagement.db', check_same_thread=False)

cursor = con.cursor()

listOfTables = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='STUDENT'").fetchall()

if listOfTables:
    print("Table Already Exists ! ")
else:
    con.execute(''' CREATE TABLE STUDENT(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT,
                            COLLEGE TEXT,
                            ADMNO INTEGER,
                            BRANCH TEXT,
                            DOB TEXT,
                            USERNAME TEXT,
                            PASSWORD TEXT ); ''')
    print("Table has created")

app = Flask(__name__)


@app.route("/")
def Login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def collect_data():
    if request.method == "POST":
        getName = request.form["sname"]
        getColName = request.form["cname"]
        getadmno = request.form["admno"]
        getBranch = request.form["branch"]
        getDOB = request.form["dob"]
        getUsername = request.form["username"]
        getPswd = request.form["pswd"]

        print(getName)
        print(getColName)
        print(getadmno)
        print(getBranch)
        print(getDOB)
        print(getUsername)
        print(getPswd)
        try:
            data = (getName, getColName, getadmno, getBranch, getDOB, getUsername, getPswd)
            insert_query = '''INSERT INTO STUDENT(NAME,COLLEGE,ADMNO,BRANCH,DOB,USERNAME,PASSWORD) 
                                VALUES (?,?,?,?,?,?,?)'''

            cursor.execute(insert_query, data)
            con.commit()
            print("Data added successfully")
            return redirect("/view_all")

        except Exception as e:
            print(e)
    return render_template("collect_form.html")


@app.route("/view_all")
def View_All():
    cursor.execute("SELECT * FROM STUDENT")
    result = cursor.fetchall()
    return render_template("View.html", students=result)


@app.route("/search")
def Search():
    return render_template("Search.html")


@app.route("/delete")
def Delete():
    return render_template("Delete.html")


if __name__ == "__main__":
    app.run()
