from flask import Flask, render_template, redirect, url_for, flash, request
app=Flask(__name__)
app.secret_key='supersecretkey'

#Modelo Account
class Account:
    def __init__(self, name, initial_balance):
        self.name = name
        self.balance = initial_balance
        self.transactions = [f"Cuenta creada con saldo inicial de {initial_balance}"]
    
    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Depósito: {amount}")

    def withdraw(self, amount):
        if self.balance >= amount and amount > 0:
            self.balance -= amount
            self.transactions.append(f"Retiro: {amount}")
        else:
            flash(f"Fondos insuficientes o cantidad inválida en la cuenta de {self.name}")

    def check_balance(self):
        return self.balance
    
    def generate_statement(self):
        return self.transactions

#Modelo Bank
class Bank:
    def __init__(self):
        self.accounts = {}
    
    def create_account(self, name, initial_balance):
        if name in self.accounts:
            flash("La Cuenta ya Existe")
        else:
            self.accounts[name] = Account(name, initial_balance)
            flash(f"Cuenta Creada para {name} con saldo inicial de {initial_balance}")
    
    def transfer(self, from_account, to_account, amount):
        if from_account in self.accounts and to_account in self.accounts:
            if self.accounts[from_account].balance >= amount and amount > 0:
                self.accounts[from_account].withdraw(amount)
                self.accounts[to_account].deposit(amount)
                flash(f"Se ha transferido {amount} de {from_account} a {to_account}.")
            else:
                flash("Fondos insuficientes en la cuenta de Origen")
        else:
            flash("Una o Ambas cuentas no existen")
    
#INICIALIZAR EL BANK
bank= Bank()

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/create_account', methods= ['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        account= request.form['name']
        amount = float(request.form['initial_balance'])
        if account in bank.accounts:
            flash(f"La Cuenta Ya Existe")
        else:
            bank.create_account(account, amount)
        return redirect(url_for('index'))
    return render_template('create_account.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        account = request.form['account']
        amount = float(request.form['amount'])
        if account in bank.accounts:
            bank.accounts[account].deposit(amount)
            flash(f"Se ha depositado {amount} en la cuenta de {account}")
        else:
            flash("La Cuenta No Existe")
        return redirect(url_for('index'))
    accounts = list(bank.accounts.keys())
    return render_template('deposit.html', accounts=accounts)

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method=='POST':
        account= request.form['account']
        amount= float(request.form['amount'])
        if account in bank.accounts:
            bank.accounts[account].withdraw(amount)
            flash(f"Se ha retirado {amount} de la cuenta de {account}")
        else:
            flash("La Cuenta No Existe")
        return redirect(url_for('index'))
    accounts = list(bank.accounts.keys())
    return render_template('withdraw.html', accounts=accounts)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method== 'POST':
        from_account = request.form['from_account']
        to_account = request.form['to_account']
        amount = float(request.form['amount'])
        if from_account in bank.accounts and to_account in bank.accounts:
            bank.transfer(from_account, to_account, amount)
        return redirect(url_for('index'))
    accounts = list(bank.accounts.keys())
    return render_template('transfer.html', accounts=accounts)

@app.route('/check_balance', methods=['GET', 'POST'])
def check_balance():
    if request.method == 'POST':
        account = request.form['account']
        if account in bank.accounts:
            balance = bank.accounts[account].check_balance()
            flash(f"El Saldo de {account} es: {balance}")
        else:
            flash("La Cuenta No Existe")
        return redirect(url_for('index'))
    accounts = list(bank.accounts.keys())
    return render_template('check_balance.html', accounts=accounts)

@app.route('/generate_statement', methods=['GET', 'POST'])
def generate_statement():
    if request.method == 'POST':
        account = request.form['account']
        if account in bank.accounts:
            transactions = bank.accounts[account].generate_statement()
            return render_template('statement.html', transactions=transactions, account=account)
        else:
            flash("La Cuenta No Existe")
        return redirect(url_for('index'))
    accounts = list(bank.accounts.keys())
    return render_template('generate_statement.html', accounts=accounts)

if __name__=="__main__":
    app.run(debug=True)