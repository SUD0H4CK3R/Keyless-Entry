from flask import Flask, render_template, request, redirect, session, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Used for session security

# CTF-style user database
users = {
    "1": {"name": "John Doe", "account_number": "1234567890", "ifsc": "BK0001", "balance": "$10,000", "flag": "No flag for you!"},
    "2": {"name": "Alice Smith", "account_number": "9876543210", "ifsc": "BK0002", "balance": "$5,500", "flag": "No flag for you!"},
    "3": {"name": "Bob Johnson", "account_number": "1122334455", "ifsc": "BK0003", "balance": "$20,000", "flag": "No flag for you!"},
    "4": {"name": "Charlie Brown", "account_number": "5566778899", "ifsc": "BK0004", "balance": "$15,300", "flag": "No flag for you!"},
    "5": {"name": "Eve Adams", "account_number": "6677889900", "ifsc": "BK0005", "balance": "$8,000", "flag": "SSEC{4lw4y5_ch3ck_u53r_4uth3nt1c4t10n}"},
    "6": {"name": "Frank White", "account_number": "7788990011", "ifsc": "BK0006", "balance": "$12,700", "flag": "No flag for you!"},
    "7": {"name": "Grace Hopper", "account_number": "8899001122", "ifsc": "BK0007", "balance": "$25,000", "flag": "No flag for you!"},
    "8": {"name": "Hank Green", "account_number": "9900112233", "ifsc": "BK0008", "balance": "$5,200", "flag": "No flag for you!"},
    "9": {"name": "Isaac Newton", "account_number": "0011223344", "ifsc": "BK0009", "balance": "$18,400", "flag": "No flag for you!"},
    "10": {"name": "Julia Roberts", "account_number": "1122334455", "ifsc": "BK0010", "balance": "$9,900", "flag": "No flag for you!"},
}


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')  # Accepts any email/password

        # Assign a random user ID
        session['user_id'] = str(random.choice(list(users.keys())))

        # Redirect to account page with user ID in the URL (IDOR vulnerability)
        return redirect(url_for('account', id=session['user_id']))
    
    return render_template('login.html')

@app.route('/account')
def account():
    user_id = request.args.get('id')  # IDOR vulnerability: fetch user by ID in the URL

    # If ID is invalid, redirect to login
    if not user_id or user_id not in users:
        return redirect(url_for('login'))

    return render_template('account.html', user=users[user_id])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
