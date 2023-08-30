from flask import Flask, render_template, request, redirect, url_for
import sqlite3

#create Database
conn = sqlite3.connect("scheduler.db")

#create Table
try:
    conn.execute("create table TASKS (id Integer Primary Key AUTOINCREMENT, Task Varchar not NULL, Priority not NULL )")
    print("table created")
except:
    print("table already created")
print("database created")
conn.commit()
conn.close()
#create Instance 
app = Flask(__name__)

#landing page
@app.route('/')
def world():
    return redirect(url_for('display'))

#insert data
@app.route('/add')
def add_task():
    return render_template('index.html')

@app.route('/save', methods=['POST','GET'])
def save_details():
    if request.method =='POST':
        task = request.form['Task']
        priority = request.form['Priority']
        with sqlite3.connect("scheduler.db") as conn:
            cursor = conn.cursor()
            cursor.execute("insert into TASKS (Task, Priority) values(?,?)", (task, priority))
            conn.commit()
    return redirect(url_for('display'))

#display all the tasks ordered by priority 
@app.route('/display')
def display():
    conn = sqlite3.connect("scheduler.db")
    cursor = conn.cursor()
    cursor.execute("select * from TASKS WHERE Priority='5'")
    tasks_1 = cursor.fetchall()
    cursor.execute("select * from TASKS WHERE Priority='4'")
    tasks_2 = cursor.fetchall()
    cursor.execute("select * from TASKS WHERE Priority='3'")
    tasks_3 = cursor.fetchall()
    cursor.execute("select * from TASKS WHERE Priority='2'")
    tasks_4 = cursor.fetchall()
    cursor.execute("select * from TASKS WHERE Priority='1'")
    tasks_5 = cursor.fetchall()
    conn.close
    return render_template("display.html", tasks_1 = tasks_1,tasks_2=tasks_2,tasks_3=tasks_3,tasks_4=tasks_4,tasks_5=tasks_5)

#delete completed tasks
@app.route('/delete/<int:task_id>', methods=['GET'])
def complete(task_id):
    with sqlite3.connect("scheduler.db") as conn:
        cursor = conn.cursor()
        cursor.execute("delete from TASKS where id=?",(task_id,))
        conn.commit()
    return redirect(url_for('display'))

#update tasks
@app.route('/update/<int:task_id>', methods=['POST','GET'])
def update(task_id):
    if request.method == 'POST':
        conn = sqlite3.connect("scheduler.db")
        cursor = conn.cursor()
        updated_task = request.form['Task']
        updated_priority = request.form['Priority']
        cursor.execute("UPDATE TASKS SET Task=?, Priority=? WHERE id=?",(updated_task, updated_priority, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('display'))

    conn = sqlite3.connect("scheduler.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TASKS WHERE id=?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return render_template("update.html", task=task)


if __name__ == '__main__':
    app.run()