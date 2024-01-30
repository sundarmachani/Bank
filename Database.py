import logging
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017")
dbData = client.Bank.BankDemo


def userDataFinder(email, doc_type):
    found_user = dbData.find_one({"email": email, "type": doc_type}, {"_id": 0})
    if found_user:
        return found_user
    else:
        return None


def add(user, account):
    if user:
        dbData.insert_one(user)
        logging.info("New User created")
    elif account:
        dbData.insert_one(account)
        logging.info("New Account created")


def accountDataFinder(number, doc_type):
    found_account = dbData.find_one({"account_number": number, "type": doc_type}, {"_id": 0})
    if found_account:
        return found_account
    else:
        return None


def lastAccount():
    first_account_number = 1000
    try:
        max_account = dbData.find_one({"type": "ACCOUNT"}, sort=[("account_number", -1)])
        if max_account:
            return max_account['account_number']
        else:
            return first_account_number
    except Exception as e:
        print(f"Error: {str(e)}")
        return first_account_number


def updateBalanceAndTransactions(account, balance, transaction_list):
    updated = dbData.update_one({"account_number": account["account_number"]},
                                {"$set": {"balance": balance, "transactions": transaction_list}})
    return updated.matched_count > 0


def getTransaction(transaction_id):
    try:
        transactions = getTransactions()
        print(transactions)
        for transaction in transactions:
            if transaction["transaction_id"] == transaction_id:
                return transaction
        return None
    except Exception as e:
        print(f"Error from DB while calling getTransaction(): {str(e)}")


def getTransactions():
    try:
        accounts = getAccounts()
        transactions = []
        if accounts:
            for account in accounts:
                account_transactions = account.get("transactions")
                if account_transactions:
                    for transaction in account_transactions:
                        transactions.append(transaction)
                else:
                    print(f"No Transactions in the account: {account}")
            return transactions
        else:
            print("No accounts in DB")
    except Exception as e:
        print(f"Error while retrieving transactions from DB: {str(e)}")


def getAccounts():
    try:
        accounts = dbData.find({"type": "ACCOUNT"}, {"_id": 0})
        if accounts:
            return list(accounts)
    except Exception as e:
        print(f"Error while fetching Accounts from DB: {str(e)}")


def getUsers():
    try:
        users = dbData.find({"type": "USER"}, {"_id": 0})
        if users:
            return list(users)
    except Exception as e:
        print(f"Error while fetching Users from DB: {str(e)}")


def deleteUser(email, doc_type):
    try:
        user = dbData.delete_one({"email": email, "type": doc_type})
        if user.deleted_count == 1:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error while deleting user from DB: {str(e)}")


def deleteAccount(email, doc_type):
    try:
        account = dbData.delete_one({"email": email, "type": doc_type})
        if account.deleted_count == 1:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error while deleting Account from DB: {str(e)} ")
