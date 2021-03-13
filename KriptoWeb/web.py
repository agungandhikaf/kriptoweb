from flask import Flask, render_template, request
import sqlalchemy as db
import hashlib
engine = db.create_engine('mysql://root@localhost/kriptoweb')


app = Flask(__name__)

connection = engine.connect()
metadata = db.MetaData()
user = db.Table('user', metadata, autoload=True, autoload_with=engine)




@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        no_hp = request.form['no_hp']
        alamat = request.form['alamat']
        password = request.form['password']
        enc1 = hashlib.sha1(password.encode())
        result1 = enc1.hexdigest()
        enc2 = hashlib.md5(password.encode())
        result2 = enc2.hexdigest()
        enc3 = result1 + result2
        query = db.insert(user).values(username=username, email=email, no_hp=no_hp, alamat=alamat, password=enc3) 
        ResultProxy = connection.execute(query)
        return render_template('login.html')
        
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        enc1 = hashlib.sha1(password.encode())
        result1 = enc1.hexdigest()
        enc2 = hashlib.md5(password.encode())
        result2 = enc2.hexdigest()
        enc3 = result1 + result2
        findUsername = db.select([user]).where(user.columns.username == username)
        ResultUsername = connection.execute(findUsername)
        findPassword = db.select([user]).where(user.columns.password == enc3)
        ResultPassword = connection.execute(findPassword)
        if username == ResultUsername.fetchone().username:
            if enc3 == ResultPassword.fetchone().password:
                return render_template('welcome.html')
            elif enc3 != ResultPassword.fetchone().password:
                return render_template('login.html')
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run()