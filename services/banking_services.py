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


    def create_account(self,name,pin,initial_deposit,account_type):
        #name validation
        if not name or not name.strip():
            raise InvalidAccountNameException('Name cannot be empty.')
        if not re.fullmatch(r"[A-Za-z ]+", name):
            raise InvalidAccountNameException('Name must only contain letters and spaces.')
        
        if(account_type not in ["SAVINGS","CURRENT"]):
            raise Exception("Invalid Account type")

        #pin validation
        if not pin :
            raise InvalidPINException('PIN is required')
        
        if len(pin) != 4 or not pin.isdigit():
            raise InvalidPINException('Pin must be of 4 digits.')

        #deposit validation
        if initial_deposit<=0:
            raise InvalidAmountException('Initial Deposit should be greater than 0.')
        
        self.account_rules(account_type,"INITIAL_DEPOSIT",initial_deposit,0)
        
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
        role="user"
        try:
            self.repo.insert_account(new_account_number,name,hashed_pin,initial_deposit,role,account_type)
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

        self.account_rules(account.account_type,"WITHDRAW",amount,account.balance)

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
    
    def update_account_holder_name(self,account_number,account_holder_name):
        account= self.repo.get_account(account_number)
       
        #authentication
        if not account:
            raise AccountNotFoundException('Account Not Found.')
        
        #validating account_holder_name
        if not account_holder_name or not account_holder_name.strip():
            raise InvalidAccountNameException('Name cannot be empty.')
        if not re.fullmatch(r"[A-Za-z ]+", account_holder_name):
            raise InvalidAccountNameException('Name must only contain letters and spaces.')
        if account.account_holder_name == account_holder_name:
            raise InvalidAccountNameException('Account Holder\'s name is same as the previous holder.')
        
        try :
            self.repo.update_account_holder_name(account_number,account_holder_name)
            self.repo.commit()
            self.logger.info(f"Updation of account_holder_name to account_number {account_number} with new name :{account_holder_name}")
        except Exception as e:
            self.repo.rollback()
            raise e
    
    def update_pin_number(self,account_number,pin_number):
        account = self.repo.get_account(account_number)

        #authentication
        if not account:
            raise AccountNotFoundException("Account not found")
        
        #validating PIN number
        if not pin_number :
            raise InvalidPINException("PIN number is required")
        if len(pin_number) != 4 or not pin_number.isdigit():
            raise InvalidPINException("PIN number must be of 4 digits")
        
        new_hashed_pin = hashlib.sha256(pin_number.encode()).hexdigest()
        
        if account.pin_hash == new_hashed_pin:
            raise InvalidPINException("PIN number should be different")
        try :
            self.repo.update_pin(account_number,new_hashed_pin)
            self.repo.commit()
            self.logger.info(f"Updation of PIN number to account_number {account_number} with new pin is successful")
        except Exception as e:
            self.repo.rollback()
            raise e
        
    #NOTE : #h UNDER DEVELOPMENT
    def update_contact(self,account_number):
        #~ UNDER DEVELOPMENT.
        #! ADD ANOTHER COLUMN NAMED contact_details IN THE ACCOUNTS DATABASE.
        return False
    
    #NOTE : #h UNDER DEVELOPMENT
    def update_kyc(self,account_number):
        #~ UNDER DEVELOPMENT.
        #! ADD ANOTHER COLUMN NAMED kyc_details IN THE ACCOUNTS DATABASE.
        return False
    
    def transfer(self,from_account,to_account,amount):
        if amount <= 0:
            raise InvalidAmountException("Invalid Transfer Amount")
        if from_account == to_account:
            raise AccountNotFoundException("Cannot transfer to same account")
        
        sender = self.repo.get_account(from_account)
        receiver = self.repo.get_account(to_account)

        if sender is None or receiver is None:
            raise AccountNotFoundException("Account not found")
        
        if sender.balance < amount:
            raise InsufficientBalanceException("Insufficient balance")
        
        new_sender_balance = sender.balance - amount
        new_receiver_balance = receiver.balance + amount

        try:
            self.repo.update_balance(from_account,new_sender_balance)
            self.repo.update_balance(to_account,new_receiver_balance)
            self.repo.insert_transaction(from_account,"TRANSFER_OUT",amount,new_sender_balance)
            self.repo.insert_transaction(to_account,"TRANSFER_IN",amount,new_receiver_balance)
            self.repo.commit()
        except Exception:
            self.repo.rollback()
            raise

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
                self.repo.insert_transaction(account_number,"ACCOUNT_LOCKED",0,account.balance)
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
        try :
            self.repo.unlock_account(account_number)
            self.repo.insert_transaction(account_number,"ACCOUNT_UNLOCKED",0,account.balance)
            self.logger.info(f"Account {account_number} is unlocked successful.")
            self.repo.commit()
        except Exception as e:
            return {"error":str(e)}
        return "Account unlocked successfully."
    
    #NOTE : #h UNDER DEVELOPMENT
    def account_close(self,account_number):
        #~ UNDER DEVELOPMENT.
        #! ADD ANOTHER COLUMN NAMED is_closed IN THE ACCOUNTS DATABASE.
        return False
    

    def account_rules(self,account_type,method,amount,balance):
        if account_type == "SAVINGS":
            if method == "INITIAL_DEPOSIT":
                if amount < 500:
                    raise Exception("Minimum balance for savings account is ₹500")
            elif method == "WITHDRAW":
                if (balance - amount)<500:
                    raise Exception("Minimum balance for savings account is ₹500")
        elif account_type == "CURRENT":
            if method == "WITHDRAW":
                OVERDRAFT_LIMIT = 10000
                if (balance+OVERDRAFT_LIMIT)<amount:
                       raise Exception("Overdraft limit exceeded")

    def get_account_type(self,account_number):
        account = self.repo.get_account(account_number)
        return account.account_type            
    
    def get_total_balance(self):
        return self.repo.get_total_balance()
    
    def get_total_accounts_count(self):
        return self.repo.get_total_accounts_count()
    
    def get_locked_accounts_count(self):
        return self.repo.get_locked_accounts_count()
    
    def get_locked_accounts(self):
        return self.repo.get_locked_accounts()
    
    def get_last_lock_event(self):
        return self.repo.get_last_account_lock_event()
    
    def get_security_events(self):
        return self.repo.get_security_events()
    
    def authenticate(self,account_number,pin):
        return self._verify_pin(account_number,pin)
    
    def is_blacklisted(self,jti):
        return self.repo.is_token_blacklisted(jti)
    
    def black_list_token(self,jti):
        self.repo.blacklist_jti(jti)
        self.repo.commit()