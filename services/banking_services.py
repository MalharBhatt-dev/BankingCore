from exceptions.account_not_found_exception import AccountNotFoundException
from exceptions.account_is_locked_exception import AccountIsLockedException
from exceptions.account_not_locked_exception import AccountNotLockedException
from exceptions.insufficient_balance_exception import InsufficientBalanceException
from exceptions.invalid_account_name_exception import InvalidAccountNameException
from exceptions.invalid_amount_exception import InvalidAmountException
from exceptions.invalid_admin_key_eception import InvalidAdminKeyException
from exceptions.invalid_pin_exception import InvalidPINException
import os
import re
import hashlib

class BankingServices:

    #! LOOSE COUPLING CONCEPT APPLIED IN __INIT__()↓
    def __init__(self,repository,admin_key,logger):
        self.repo=repository
        self.admin_key = admin_key
        self.logger = logger


    def create_account(self,name,pin,initial_deposit):
        #name validation
        if not name or not name.strip():
            raise InvalidAccountNameException('Name cannot be empty.')
        if not re.fullmatch(r"[A-Za-z ]+", name):
            raise InvalidAccountNameException('Name must only contain letters and spaces.')
        
        #pin validation
        if not pin :
            raise InvalidPINException('PIN is required')
        
        if len(pin) != 4 or not pin.isdigit():
            raise InvalidPINException('Pin must be of 4 digits.')

        #deposit validation
        if initial_deposit<=0:
            raise InvalidAmountException('Initial Deposit should be greater than 0.')
        
        #generate account_number    
        last_account_number = self.repo.get_last_account_number()
        if last_account_number is None:
            new_account_number = 1001
            print('First account is generated.')
        else :
            new_account_number = last_account_number + 1 
            print('new account is generated')
       
       #generate pin hash
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
    
        #inserting account
        try:
            self.repo.insert_account(new_account_number,name,hashed_pin,initial_deposit)
            self.repo.insert_transaction(new_account_number,"INITIAL DEPOSIT",initial_deposit,initial_deposit)
            self.repo.commit()
        except Exception as e:
            self.repo.rollback()
            raise e
        return new_account_number
    
    
    def deposit(self,account_number,amount):

        account = self.repo.get_account(account_number)
        #authentication
        if not account:
            raise AccountNotFoundException('Account Not Found.')
        #validatin amount
        if amount <= 0:
            raise InvalidAmountException('Amount should be greater than 0.')
        
        new_balance = account.balance + amount
        try:
            self.repo.update_balance(account.account_number,new_balance)
            self.repo.insert_transaction(account.account_number,"DEPOSIT",amount,new_balance)
            self.repo.commit()
            self.logger.info(f"Deposit of {amount} to account {account_number}.New balance: {new_balance}")
        except Exception as e:
            self.repo.rollback()
            raise e
        return new_balance
        
    
    def withdraw(self,account_number,amount):
        account = self.repo.get_account(account_number)
        #authentication
        if not account:
            raise AccountNotFoundException('Account Not Found.')
        #validating amount
        if amount <= 0:
            raise InvalidAmountException('Amount should be greater than 0.')
        #validating balance
        if account.balance < amount:
            raise InsufficientBalanceException('Insufficient Balance.')
       
        new_balance = account.balance - amount
        try :
            self.repo.update_balance(account.account_number,new_balance)
            self.repo.insert_transaction(account.account_number,"WITHDRAW",amount,new_balance)
            self.repo.commit()
            self.logger.info(f"Withdraw of {amount} to account {account_number}.New balance: {new_balance}")
        except Exception as e:
            self.repo.rollback()
            raise e
        return new_balance
    
    def view_transactions(self,account_number):
        account = self.repo.get_account(account_number)
        #authentication
        if not account:
            raise AccountNotFoundException('Account Not Found.')
        transactions_logs =  self.repo.get_transactions(account.account_number)
        return transactions_logs
    
    def view_balance(self,account_number):
        account = self.repo.get_account(account_number)
        #authentication
        if not account:
            raise AccountNotFoundException('Account Not Found.')        
        return account.balance
    
    def _verify_pin(self,account_number,pin):
        account = self.repo.get_account(account_number)
        #checking if account exits or not  
        if not account:
            raise AccountNotFoundException('Account Not Found.')
        #checking if account is_locked:
        if account.is_locked == 1:
            self.logger.error(f"Account {account_number} is locked due to multiple failed attempts.")
            raise AccountIsLockedException('The account is locked.')
        if pin is None:
            return account
        pin_hash = hashlib.sha256(pin.encode()).hexdigest()
        if account.pin_hash != pin_hash:
            new_attempts = account.failed_attempts + 1
            is_locked = account.is_locked
            if new_attempts >= 3:
                is_locked = 1
            self.repo.update_security_state(account_number,new_attempts,is_locked)
            self.repo.commit()
            self.logger.warning(f"Failed PIN attempt for account {account_number}")
            #pin validation
            if not pin:
                raise InvalidPINException(f"PIN is required. Attempts left :{3-new_attempts}")
            if not pin.isdigit():
                raise InvalidPINException(f"PIN must be in digits. Attempts left :{3-new_attempts}")
            if len(pin) != 4:
                raise InvalidPINException(f"Pin must be of 4 digits. Attempts left :{3-new_attempts}")
            raise InvalidPINException(f"Wrong Credentials. Attempts left :{3-new_attempts}")
        else :
            if account.failed_attempts > 0:
                reset_failed_attempts = 0
                reset_is_locked = 0
                self.repo.update_security_state(account_number,reset_failed_attempts,reset_is_locked)
                self.repo.commit()
            return account
        
    def unlock_account(self,account_number,provided_key):
        if provided_key != self.admin_key:
            self.logger.warning(f"Failed Admin Key attempt for account {account_number}")
            raise InvalidAdminKeyException('Invalid Admin Key.')
        account = self.repo.get_account(account_number)

        if not account.is_locked:
            raise AccountNotLockedException('Account is not locked.')
        
        self.repo.unlock_account(account_number)
        self.logger.info(f"Account {account_number} is unlocked successful.")
        return "Account unlocked successfully."
    
    def authenticate(self,account_number,pin):
        return self._verify_pin(account_number,pin)