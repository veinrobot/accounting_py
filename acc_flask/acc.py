# pip install Flask-Login Flask-WTF
# pip install flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
# 登入系統
# 使用者帳戶資料
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# 假設已經有一些用戶
users = [
    User(1, 'zzzz', 'zzzzzz'),
    User(2, 'user2', 'password2')
]

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
records = {1: [{'id': 1, 'date': '2023-12-24', 'amount': 244.0, 'types': '收入', 'user_id': 1, 'categories': '工資', 'notes': '一月份薪水'}, 
               {'id': 2, 'date': '2023-12-24', 'amount': 50.0, 'types': '支出', 'user_id': 1, 'categories': '食物', 'notes': '午餐'}]}
pre_records = {'income': [0,0,0,0], 'spend': [0,0,0,0]}
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

    new_record = {'id': next_id, 'date': date, 'amount': amount, 'types': '收入', 'user_id': current_user.id, 'categories': '工資', 'notes': '一月份薪水'}
    if records.get(current_user.id) == None:
        records[current_user.id] = []
    records[current_user.id].append(new_record)
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
            return redirect(url_for('index'))
        return render_template('edit.html', record=record)
    return 'Record not found', 404

@app.route('/delete_record/<int:record_id>')
@login_required
def delete_record(record_id):
    global records
    records = [r for r in records if r['id'] != record_id or r['user_id'] != current_user.id]
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

if __name__ == '__main__':
    app.run(debug=True)
