import logging
import Database
from Transaction import Transaction
from User import getUser, User


class Account:
    ACCOUNT = "ACCOUNT"

    def __init__(self, email, account_type, balance):
        self.account_number = Database.lastAccount() + 1
        self.email = email
        self.account_type = account_type
        self.balance = balance
        self.type = Account.ACCOUNT
        self.created_at = User.dateFormatter
        self.transactions = []


def createAccount(account):
    email = account.email
    user = getUser(email)
    if user is not None:
        logging.info("User already present... creating Account")
        new_Account = Account(account.email, account.account_type, account.balance)
        Database.add(None, new_Account.__dict__)
    else:
        raise ValueError(
            f"User is not created for the email '{email}'. Create the user using the endpoint "
            f"http://127.0.0.1:5000/createUser")


def getAccount(account_number):
    account_number = int(account_number)
    account = Database.accountDataFinder(account_number, Account.ACCOUNT)
    if account:
        return account
    else:
        raise ValueError(f"No Account found with 'Account Number' : {account_number}")


def isValid(account_number):
    account = getAccount(account_number)
    if account and account["email"]:
        if getUser(account["email"]):
            return account
    return None


def performTransaction(sender_number, receiver_number, amount: int):
    if sender_number == receiver_number:
        raise ValueError("sender and receiver are the same, so cannot perform a transaction")
    sender_valid = isValid(sender_number)
    receiver_valid = isValid(receiver_number)
    if sender_valid is None:
        raise ValueError("Sender is not valid !")
    if receiver_valid is None:
        raise ValueError("Receiver is not valid !")
    if sender_valid and receiver_valid:
        sender_balance = sender_valid["balance"]
        receiver_balance = receiver_valid["balance"]
        if sender_balance is not None and receiver_balance is not None:
            if sender_balance >= amount:
                sender_balance -= amount
                receiver_balance += amount
                if "transactions" in sender_valid and "transactions" in receiver_valid:
                    transactions_sender = sender_valid["transactions"]
                    transactions_sender.append(Transaction(receiver_number, None, amount).__dict__)

                    transactions_receiver = receiver_valid["transactions"]
                    transactions_receiver.append(Transaction(None, sender_number, amount).__dict__)

                    if (Database.updateBalanceAndTransactions(sender_valid, sender_balance,
                                                              transactions_sender) and
                            Database.updateBalanceAndTransactions(receiver_valid, receiver_balance,
                                                                  transactions_receiver)):
                        print("Updated balance and transactions")
                    else:
                        raise ValueError("Failed to update balance, transactions in Database")
            else:
                raise ValueError("Insufficient funds in Sender Account")
        else:
            raise ValueError("Balance attributes are not found in either sender or receiver")


def getAllAccounts():
    accounts = Database.getAccounts()
    if accounts:
        for account in accounts:
            account.pop("transactions")
        return accounts


def deleteAccount(email):
    is_deleted = Database.deleteUser(email, Account.ACCOUNT)
    if is_deleted:
        return True
