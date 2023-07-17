from flask import Flask,render_template,request
import pandas as pd
import mysql.connector
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score










mydb = mysql.connector.connect(host='localhost',user='root',password='',port='',database='employee_promoted')
cur = mydb.cursor()


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/logout')
def logout():
    return render_template('index.html')



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        psw = request.form['psw']
        sql = "SELECT * FROM employee1 WHERE Email=%s and Password=%s"
        val = (email, psw)
        cur = mydb.cursor()
        cur.execute(sql, val)
        results = cur.fetchall()
        mydb.commit()
        if len(results) >= 1:
            return render_template('loginhome.html', msg='login succesful')
        else:
            return render_template('login.html', msg='Invalid Credentias')

    return render_template('login.html')

@app.route('/loginhome')
def loginhome():
    return render_template('loginhome.html')






@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method == "POST":
        print('a')
        name = request.form['name']
        print(name)
        email = request.form['email']
        pws = request.form['psw']
        print(pws)
        cpws = request.form['cpsw']
        if pws == cpws:
            sql = "select * from employee1"
            print('abcccccccccc')
            cur = mydb.cursor()
            cur.execute(sql)
            all_emails = cur.fetchall()
            mydb.commit()
            all_emails = [i[2] for i in all_emails]
            if email in all_emails:
                return render_template('registration.html', msg='Account Already Exist')
            else:
                sql = "INSERT INTO employee1(name,email,password) values(%s,%s,%s)"
                values = (name, email, pws)
                cur.execute(sql, values)
                mydb.commit()
                cur.close()
                return render_template('registration.html', msg='Successfully Registered')
        else:
            return render_template('registration.html', msg='Password Not Match')

    return render_template('registration.html')


@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == "POST":
        file = request.files['file']
        print(file)
        global df
        df = pd.read_csv(file)
        print(df)
        return render_template('upload.html', columns=df.columns.values, rows=df.values.tolist(),msg='Successfully Uploaded')
    return render_template('upload.html')
@app.route('/viewdata')
def viewdata():
    print(df.columns)
    df_sample = df.head(100)
    return render_template('viewdata.html', columns=df_sample.columns.values, rows=df_sample.values.tolist())


@app.route('/preprocessing',methods=['POST','GET'])
def preprocessing():
    global X, y, X_train, X_test, y_train, y_test
    if request.method == "POST":
        size = int(request.form['split'])
        size = size / 10
        print(size)
        df.drop(['employee_id'], axis=1, inplace=True)
        df["education"].fillna(method='ffill', limit=30, inplace=True)
        df["previous_year_rating"].fillna(method='bfill', limit=30, inplace=True)
        df.replace({'Sales & Marketing': 1, 'Operations': 2, 'Technology': 3, 'Analytics': 4, 'R&D': 5, 'Procurement': 6,'Finance': 7, 'HR': 8, 'Legal': 9}, inplace=True)
        df.replace({"Master's & above": 1, "Bachelor's": 2, "Below Secondary": 3}, inplace=True)
        df.replace({'f': 0, 'm': 1}, inplace=True)
        df.replace({'sourcing': 1, 'referred': 2,'other': 3}, inplace=True)
        encoder = LabelEncoder()
        df['region'] = encoder.fit_transform(df['region'])
        df['region'].head()
        x = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        oversample = SMOTE()
        a, b = oversample.fit_resample(x, y)
        X_train, X_test, y_train, y_test = train_test_split(a, b, test_size=0.3, random_state=52)
        print(X_train)
        print(X_train.columns)
        return render_template('preprocessing.html', msg="Data preprocessing has been completed successfully, and the dataset has been split appropriately.")

    return render_template('preprocessing.html')



@app.route('/model',methods=['POST','GET'])
def model():
    if request.method=='POST':
        models = int(request.form['algo'])
        if models==1:
            print("==")
            model = DecisionTreeClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred,y_test)
            acc = acc*100
            msg = 'Accuracy  for Decision Tree is ' + str(acc) + str('%')

        elif models== 2:
            print("======")
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred, y_test)
            acc = acc * 100
            msg = 'Accuracy  for Random Forest is ' + str(acc) + str('%')

        elif models==3:
            print("===============")
            model = SVC()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred,y_test)
            acc = acc*100
            msg = 'Accuracy  for SVM is ' + str(acc) + str('%')
        return render_template('model.html',msg=msg)

    return render_template('model.html')
@app.route('/prediction',methods=['POST','GET'])
def prediction():
    print('111111')
    if  request.method == 'POST':
        print('2222')
        department = request.form['department']
        print(department)
        region =request.form['region']
        print(region)
        education =request.form['education']
        print(education)
        gender = request.form['gender']
        print(gender)
        recruitment_channel = request.form['recruitment_channel']
        print(recruitment_channel)
        no_of_trainings = request.form['no_of_trainings']
        print(no_of_trainings)
        age = request.form['age']
        print(age)
        previous_year_rating = request.form['previous_year_rating']
        print(previous_year_rating)
        length_of_service = request.form['length_of_service']
        print(length_of_service)
        KPIs_met = request.form['KPIs_met']
        print(KPIs_met)
        awards_won = request.form['awards_won']
        print(awards_won)
        avg_training_score = request.form['avg_training_score']
        print(avg_training_score)
        m = [department,region,education,gender,recruitment_channel,no_of_trainings,age,previous_year_rating,length_of_service,KPIs_met,awards_won,avg_training_score]
        model = RandomForestClassifier()
        model.fit(X_train,y_train)
        result = model.predict([m])
        print(result)
        if result == 1:
            msg = 'Employee is Promoted'
        else:
            msg = 'Employee is Not Promoted'
        return render_template('prediction.html',msg=msg)

    return render_template('prediction.html')



if __name__=="__main__":
    app.run(debug=True)