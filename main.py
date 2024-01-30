from flask import Flask, request, jsonify
from flask_cors import CORS
import Transaction
from Account import createAccount, Account, getAccount, performTransaction, getAllAccounts, deleteAccount
from User import User, createUser, getUser, getAllUsers, deleteUser

app = Flask(__name__)
cors = CORS(app)


@app.route('/createUser', methods=['POST'])
def create_user_endpoint():
    try:
        data = request.get_json()
        mandatory_fields = {"name", "age", "phone", "email", "address", "city", "state", "pincode", "country"}
        for field in mandatory_fields:
            if field not in data:
                return jsonify({"error": f"Field '{field}' is mandatory"}), 400
        name = data.get('name')
        age = data.get('age')
        try:
            ag = int(age)
            if ag > 100:
                return jsonify({"error": "age number is invalid"}), 400
            age = ag
        except ValueError:
            return jsonify({"error": f"Invalid age '{age}'"}), 400
        phone = data.get('phone')
        try:
            ph = int(phone)
            if ph > 9999999999:
                return jsonify({"error": "Phone number is more than 10 numbers"}), 400
        except ValueError:
            return jsonify({"error": f"Invalid phone number format '{phone}'"}), 400
        email = data.get('email')

        address = data.get('address')
        city = data.get("city")
        state = data.get("state")
        pincode = data.get("pincode")
        try:
            pin = int(pincode)
            if pin > 999999:
                return jsonify({"error": "pincode is invalid"}), 400
        except ValueError:
            return jsonify({"error": f"pincode is invalid '{pincode}'"}), 400
        country = data.get("country")
        createUser(User(name, age, phone, email, address, city, state, pin, country))

        return jsonify({"message": "User created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/getUser", methods=['GET'])
def get_user():
    try:
        email = request.args.get("email")
        if not email:
            return jsonify({"error": "Email parameter is required"}), 400
        user = getUser(email)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found !"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/createAccount", methods=['POST'])
def create_account():
    try:
        data = request.get_json()
        mandatory_fields = ['email', 'account_type', 'balance']
        for field in mandatory_fields:
            if field not in data:
                return jsonify({"error": f"Field '{field}' is mandatory"}), 400
        email = data.get("email")
        account_type = data.get("account_type")
        if account_type not in {"FIXED", "CURRENT", "SAVING"}:
            return jsonify({"error": "unknown account_type"}), 400
        balance = data.get("balance", 0.0)
        createAccount(Account(email, account_type, balance))
        return jsonify({"message": "Account created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/getAccount", methods=['GET'])
def get_account():
    try:
        account_number = request.args.get("account_number")
        if not account_number:
            return jsonify({"error": "Account Number is required"}), 400
        account = getAccount(account_number)
        if account:
            return jsonify(account), 200
        else:
            return jsonify({"error": "Account not Found !"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/deleteUser", methods=['DELETE'])
def delete_user():
    try:
        email = request.args.get("email")
        if email:
            is_deleted = deleteUser(email)
            if is_deleted:
                return jsonify({"message": f"User '{email}' is deleted successfully"}), 200
            else:
                return jsonify({"error": f"No User found with email {email}"}), 404
        else:
            return jsonify({"error": "email is mandatory for deleting User"}), 400
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/deleteAccount", methods=['DELETE'])
def delete_account():
    try:
        email = request.args.get("email")
        if email:
            is_deleted = deleteAccount(email)
            if is_deleted:
                return jsonify({"message": f"Account '{email}' is deleted successfully"}), 200
            else:
                return jsonify({"error": f"No account found with email {email}"}), 404
        else:
            return jsonify({"error": "email is mandatory for deleting Account"}), 400
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/send", methods=['POST'])
def send_transaction():
    try:
        transactionData = request.get_json()
        mandatory_fields = ['sender', 'receiver', 'amount']
        for field in mandatory_fields:
            if field not in transactionData:
                return jsonify({"error": f"Field '{field}' is mandatory"}), 400
        sender = transactionData.get("sender")
        receiver = transactionData.get("receiver")
        amount = transactionData.get("amount")
        performTransaction(sender, receiver, amount)
        return jsonify({"message": "Transaction successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/transaction", methods=['GET'])
def get_transaction():
    try:
        transaction_param = request.args.get("transaction_id")
        if transaction_param:
            transaction = Transaction.getTransaction(transaction_param)
            if transaction:
                return jsonify(transaction), 200
            else:
                return jsonify({"error": f"No Transaction found with the transaction_id: {transaction_param}"}), 404
        else:
            return jsonify({"error": "transaction_id is mandatory !"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/allAccounts", methods=['GET'])
def get_all_accounts():
    try:
        accounts = getAllAccounts()
        if accounts:
            return jsonify(accounts), 200
        else:
            return jsonify({"error": f"No Accounts found !"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/allUsers", methods=['GET'])
def get_all_Users():
    try:
        users = getAllUsers()
        if users:
            return jsonify(users), 200
        else:
            return jsonify({"error": f"No Users found !"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/allTransactions", methods=['GET'])
def get_all_Transactions():
    try:
        transactions = Transaction.getAllTransactions()
        if transactions:
            return jsonify(transactions), 200
        else:
            return jsonify({"error": f"No Transactions found !"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
