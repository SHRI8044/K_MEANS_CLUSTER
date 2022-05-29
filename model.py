from flask import Flask,render_template,request
import numpy as np
import pickle
from flask_mysqldb import MySQL


with open("scaler.pkl","rb") as scaler_file:
    scaler = pickle.load(scaler_file)



with open("model.pkl","rb") as model_file:
    model = pickle.load(model_file)



app = Flask(__name__)


######MY SQL COnfiguration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "shri8044"
app.config["MYSQL_DB"] = "shri"

mysql = MySQL(app)



@app.route("/")
def index():
    return render_template("cluster.html")



@app.route("/predict",methods = ["GET","POST"])
def predict():
    age = request.form['age']
    annual_income = request.form['annual_income']
    spending_score = request.form['spending_score']
    
    user_data = np.zeros(3)
    
    user_data[0] = age
    user_data[1] = annual_income
    user_data[2] = spending_score
    
    user_data_scale = scaler.transform([user_data])
    
    res = model.predict(user_data_scale)
    print(res)
    result = res[0]



    cursor = mysql.connection.cursor()
    query = "CREATE TABLE IF NOT EXISTS userinput(age VARCHAR(10),annual_income VARCHAR(10),spending_score VARCHAR(10),result VARCHAR(10))"
    cursor.execute(query)
    cursor.execute("INSERT INTO userinput(age,annual_income,spending_score,result) VALUES(%s,%s,%s,%s)",(age,annual_income,spending_score,result))

    mysql.connection.commit()
    cursor.close()
    




    if result == 0:
        result = "user is from Premiun"

    return render_template("disply.html",cluster = result)





if __name__ == "__main__":
    app.run(debug=True) 