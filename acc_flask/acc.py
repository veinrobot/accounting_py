# pip install Flask-Login Flask-WTF
# pip install flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from pyngrok import ngrok
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

# 檔案名稱
users_file_name = "users_data.pkl"
records_file_name = "records.json"

# 紀錄存檔讀檔系統
import json

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_from_json(filename, default_value={}):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{filename}' not found. Returning default value.")
        return default_value

# 登入系統
# 使用者帳戶資料
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = [
    # User(1, 'zzzz', 'zzzzzz'),
    # User(2, 'user2', 'password2')
]

# 使用者存檔讀檔
import pickle
def save_users_to_file(filename, users_list):
    with open(filename, 'wb') as file:
        pickle.dump(users_list, file)

def load_users_from_file(filename, default_value=None):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"File '{filename}' not found. Returning default value.")
        return default_value

# 使用者身份驗證
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return next((user for user in users if user.id == int(user_id)), None)

# 登入表單
class LoginForm(FlaskForm):
    username = StringField('使用者名稱', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('密碼', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('登入')

# 註冊表單
class RegisterForm(FlaskForm):
    username = StringField('使用者名稱', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('密碼', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('註冊')

# 登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = next((user for user in users if user.username == username and user.password == password), None)
        if user:
            login_user(user)
            flash('登入成功', 'success')
            return redirect(url_for('index'))
        else:
            flash('無效的使用者名稱或密碼', 'error')
    return render_template('login.html', form=form)

# 註冊頁面
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(len(users) + 1, username, password)
        users.append(user)
        save_users_to_file(users_file_name, users)
        flash('註冊成功，請登入', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出', 'success')
    return redirect(url_for('login'))

## 記帳系統
# 記帳資料庫，用於存放記錄
records = {
    # 1: [{'id': 1, 'date': '2023-12-24', 'amount': 244.0, 'types': '收入', 'user_id': 1, 'categories': '工資', 'notes': '一月份薪水'}, 
    # {'id': 2, 'date': '2023-12-24', 'amount': 50.0, 'types': '支出', 'user_id': 1, 'categories': '食物', 'notes': '午餐'}]
    }
pre_records = {
    'income': [0,0,0,0], 'spend': [0,0,0,0]
    }
next_id = 3
login = False

@app.before_request
def check_login():
    allowed_routes = ['login', 'register']  # 允許訪問的路由列表
    if request.endpoint not in allowed_routes and not current_user.is_authenticated:
        return redirect(url_for('login'))

def get_user_records()->list:
    user_records = records.get(current_user.id)
    if user_records == None:
        user_records = []
        records[current_user.id] = []
    return user_records

# 首頁，顯示所有記錄
# 登入後才能進入的頁面
@app.route('/')
@login_required
def index():
    # user_records = [record for record in records if record['user_id'] == current_user.id]
    user_records = get_user_records()
    return render_template('index.html', records=user_records)

@app.route('/add_record', methods=['POST'])
@login_required
def add_record():
    global next_id
    date = request.form['date']
    amount = float(request.form['amount'])
    types = request.form['types']
    categories = request.form['categories']
    notes = request.form['notes']

    new_record = {'id': next_id, 'date': date, 'amount': amount, 'types': types, 'user_id': current_user.id, 'categories': categories, 'notes': notes}
    if records.get(current_user.id) == None:
        records[current_user.id] = []
    records[current_user.id].append(new_record)
    save_to_json(records_file_name, records)
    next_id += 1
    return redirect(url_for('index'))

@app.route('/edit_record/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    record = next((r for r in records[current_user.id] if r['id'] == record_id and r['user_id'] == current_user.id), None)
    if record:
        if request.method == 'POST':
            record['date'] = request.form['date']
            record['amount'] = float(request.form['amount'])
            record['types'] = request.form['types']
            record['categories'] = request.form['categories']
            record['notes'] = request.form['notes']
            save_to_json(records_file_name, records)
            return redirect(url_for('index'))
        return render_template('edit.html', record=record)
    return 'Record not found', 404

@app.route('/delete_record/<int:record_id>')
@login_required
def delete_record(record_id):
    global records
    records = [r for r in records if r['id'] != record_id or r['user_id'] != current_user.id]
    save_to_json(records_file_name, records)
    return redirect(url_for('index'))

@app.route('/chart')
def chart():
    user_records = get_user_records()
    return render_template('chart.html', records = user_records, pre_records = pre_records)

@app.route('/add_pre_record', methods=['POST'])
def add_pre_record():
    types = request.form['modalRadio']
    day = request.form['Damount']
    week = request.form['Wamount']
    month = request.form['Mamount']
    year = request.form['Yamount']
    if day != "": pre_records[types][0] = float(day)
    if week != "": pre_records[types][1] = float(week)
    if month != "": pre_records[types][2] = float(month)
    if year != "": pre_records[types][3] = float(year)
    return redirect(url_for('chart'))

@app.route('/showdata')
def showdata():
    user_records = get_user_records()
    return render_template('showdata.html', records=user_records)

def read_txt_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return ""

if __name__ == '__main__':
    port_number = 5000

    ngrok_key_file = "ngrok_key.txt"
    ngrok_auth_key = read_txt_file(ngrok_key_file).replace("\n", "").replace("\r", "")
    print(ngrok_auth_key)
    if ngrok_auth_key!="":
        ngrok.set_auth_token(ngrok_auth_key)
        public_url = ngrok.connect(port_number).public_url
        print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port_number))

        # load records
        records = load_from_json(records_file_name, dict())
        users = load_users_from_file(users_file_name, [])

        app.run()
        # app.run(debug=True)
        # app.run('0.0.0.0', port=port_number, debug=True)
    else:
        print("not ngrok key found")
