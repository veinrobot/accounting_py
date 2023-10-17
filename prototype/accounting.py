import datetime

# 初始化餘額
balance = 0

# 創建一個交易紀錄字典，其中每筆交易包含金額、類型、時間
transactions = []

def save_transactions():
    with open("transactions.txt", "w") as file:
        for transaction in transactions:
            file.write(f"{transaction['type']},{transaction['amount']},{transaction['time']}\n")

def load_transactions():
    global balance
    try:
        with open("transactions.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 3:
                    print(f"警告：無效的交易記錄行: {line}")
                    continue
                trans_type, trans_amount_str, trans_time_str = parts
                try:
                    trans_amount = float(trans_amount_str)
                    trans_time = datetime.datetime.strptime(trans_time_str, "%Y-%m-%d %H:%M:%S.%f")
                    if trans_type == "支出":
                        balance -= trans_amount
                    else:
                        balance += trans_amount
                    transactions.append({"type": trans_type, "amount": trans_amount, "time": trans_time})
                except (ValueError, TypeError) as e:
                    print(f"警告：無法解析交易記錄行: {line}, 錯誤: {e}")
    except FileNotFoundError:
        pass

load_transactions()
print("歡迎使用簡易記帳系統！")
count = 0
while True:
    if count>0:
        print("\n\n")
    count+=1
    print("記帳程式")
    print("1. 新增支出")
    print("2. 新增收入")
    print("3. 顯示餘額")
    print("4. 顯示交易紀錄")
    print("5. 編輯交易")
    print("6. 退出")
    
    choice = input("請選擇操作 (1/2/3/4/5/6): ")
    
    if choice == "1":
        expense = float(input("請輸入支出金額: "))
        # 要求使用者輸入時間
        transaction_time = input("請輸入交易時間 (年-月-日 時:分:秒，按Enter使用當前時間): ")

        # 如果使用者按Enter，使用當前時間
        if not transaction_time:
            transaction_time = datetime.datetime.now()
        else:
            # 解析使用者輸入的時間
            transaction_time = datetime.datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
       
        transactions.append({"type": "支出", "amount": -expense, "time": transaction_time})
        balance -= expense
        print("支出已記錄")
    elif choice == "2":
        income = float(input("請輸入收入金額: "))
        transaction_time = input("請輸入交易時間 (按Enter使用當前時間): ")
        if not transaction_time:
            transaction_time = datetime.datetime.now().replace(microsecond=0)
        else:
            transaction_time = datetime.datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
        
        transactions.append({"type": "收入", "amount": income, "time": transaction_time})
        balance += income
        print("收入已記錄")
    elif choice == "3":
        print(f"目前餘額: {balance}")
    elif choice == "4":
        print("\n\n")
        print("交易紀錄:")
        for i, transaction in enumerate(transactions, start=1):
            print(f"{i}. 類型: {transaction['type']}, 金額: {abs(transaction['amount'])}, 時間: {transaction['time']}")
    elif choice == "5":
        edit_choice = int(input("請輸入要編輯的交易編號: "))
        if 1 <= edit_choice <= len(transactions):
            edit_transaction = transactions[edit_choice - 1]
            print(f"編輯交易 {edit_choice}: 類型: {edit_transaction['type']}, 金額: {abs(edit_transaction['amount'])}, 時間: {edit_transaction['time']}")
            new_amount = float(input("請輸入新金額: "))
            new_type = input("請輸入新類型 (支出/收入): ")
            new_time = input("請輸入新時間 (按Enter使用原時間): ")
            
            if not new_time:
                new_time = edit_transaction['time']
            else:
                new_time = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")
            
            balance -= edit_transaction['amount']
            balance += new_amount
            edit_transaction['amount'] = new_amount
            edit_transaction['type'] = new_type
            edit_transaction['time'] = new_time
            print(f"交易 {edit_choice} 已編輯")
        else:
            print("無效的交易編號")
    elif choice == "6":
        save_transactions()
        print("感謝使用記帳程式，再見！")
        break
    else:
        print("無效的選項。請重新輸入。")
