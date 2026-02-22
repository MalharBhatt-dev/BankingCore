from exceptions.account_not_found_exception import AccountNotFoundException
from exceptions.insufficient_balance_exception import InsufficientBalanceException
from exceptions.invalid_account_name_exception import InvalidAccountNameException
from exceptions.invalid_amount_exception import InvalidAmountException
from exceptions.invalid_pin_creation import InvalidPinCreationException
import re

class BankingServices:

    #! LOOSE COUPLING CONCEPT APPLIED IN __INIT__()↓
    def __init__(self,repository):
        self.repo=repository


    def create_account(self,name,pin,initial_deposit):
        #name validation
        if not name or not name.strip():
            raise InvalidAccountNameException('Name cannot be empty.')
        if not re.fullmatch(r"[A-Za-z ]+", name):
            raise InvalidAccountNameException('Name must only contain letters and spaces.')
        #deposit validation
        if len(pin) != 4 or not pin.isdigit():
            raise InvalidPinCreationException('Pin must be of 4 digits.')
        if initial_deposit<=0:
            raise InvalidAmountException('Initial Deposit should be greater than 0.')
        #generate account_number    
        last_account_number = self.repo.get_last_account_number()
        if last_account_number is None:
            new_account_number = 1001
        else :
            new_account_number = last_account_number + 1 
        #inserting account
        try:
            self.repo.insert_account(new_account_number,name,pin,initial_deposit)
            self.repo.insert_transaction(new_account_number,"INITIAL DEPOSIT",initial_deposit,initial_deposit)
            self.repo.commit()
        except Exception as e:
            self.repo.rollback()
            raise e
        return new_account_number
    
    def deposit(self,account_number,pin,amount):
        account = self.repo.get_account(account_number)
    
        if not account:
            raise AccountNotFoundException('Account Not Found.')
        if amount <= 0:
            raise InvalidAmountException('Amount should be greater than 0.')
        balance = account.balance
        new_balance = balance + amount
        
        try:
            self.repo.update_balance(account.account_number,new_balance)
            self.repo.insert_transaction(account.account_number,"DEPOSIT",amount,new_balance)
            self.repo.commit()
        except Exception as e:
            self.repo.rollback()
            raise e
        return new_balance
    
    def withdraw(self,account_number,amount):
        account = self.repo.get_account(account_number)
        
        if not account:
            raise AccountNotFoundException('Account not found')
        if amount <= 0:
            raise InvalidAmountException('Amount should be greater than 0.')
        if account.balance < amount:
            raise InsufficientBalanceException('Insufficient Balance.')
        
        old_balance = account.balance
        new_balance = old_balance - amount

        try :
            self.repo.update_balance(account.account_number,new_balance)
            self.repo.insert_transaction(account.account_number,"WITHDRAW",amount,new_balance)
            self.repo.commit()
        except Exception as e:
            self.repo.rollback()
            raise e
        
        return new_balance
    
    def view_transactions(self,account_number):
        account = self.repo.get_account(account_number)
        if not account:
            raise AccountNotFoundException('Account not found.')
        transactions_logs =  self.repo.get_transactions(account.account_number)
        return transactions_logs
    
    def view_balance(self,account_number):
        account = self.repo.get_account(account_number)
        if not account :
            raise AccountNotFoundException('Account not found.')
        return account.balance