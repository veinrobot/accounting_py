from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# 記帳資料庫，用於存放記錄
records = [
    {'id': 1, 'date': '2023-11-15', 'amount': 50, 'types': '收入'},
    {'id': 2, 'date': '2023-11-14', 'amount': 30, 'types': '收入'},
    {'id': 3, 'date': '2023-11-13', 'amount': 20, 'types': '支出'}
]
pre_records = {'income': [0,0,0,0], 'spend': [0,0,0,0]}
next_id = 4

# 首頁，顯示所有記錄
@app.route('/')
def index():
    return render_template('index.html', records=records)

# 新增記錄
@app.route('/add_record', methods=['POST'])
def add_record():
    global next_id
    date = request.form['date']
    amount = float(request.form['amount'])

    records.append({'id': next_id, 'date': date, 'amount': amount, 'types': '收入'})
    next_id += 1

    return redirect(url_for('index'))

# 修改記錄
@app.route('/edit_record/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    record = next((r for r in records if r['id'] == record_id), None)
    if record:
        if request.method == 'POST':
            record['date'] = request.form['date']
            record['amount'] = float(request.form['amount'])
            return redirect(url_for('index'))
        return render_template('edit.html', record=record)
    return 'Record not found', 404

# 刪除記錄
@app.route('/delete_record/<int:record_id>')
def delete_record(record_id):
    global records
    records = [r for r in records if r['id'] != record_id]
    return redirect(url_for('index'))

@app.route('/chart')
def chart():
    return render_template('chart.html', records = records, pre_records = pre_records)

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

if __name__ == '__main__':
    app.run(debug=True)
