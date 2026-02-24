from repository.account_repository import AccountRepository
from services.banking_services import BankingServices
from exceptions.base_exception import BankingException
from app.auth import generate_token
import logging
from app.config import Config
import os

#! DEPENDENCY INJECTION IS ACHIEVED HERE↓
if __name__ == "__main__":
    
    os.makedirs(os.path.dirname(Config.LOG_FILE),exist_ok=True)
    #log_setup
    logger = logging.getLogger("banking_core")
    logger.setLevel(Config.LOG_LEVEL)
    #prevent duplicate handlers
    if not logger.handlers:
        file_handlers = logging.FileHandler(Config.LOG_FILE)
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        file_handlers.setFormatter(formatter)
        logger.addHandler(file_handlers)

    admin_key  = os.getenv("ADMIN_KEY")
    

    repo = AccountRepository()
    service = BankingServices(repo,admin_key,logger)

    current_token = None
    current_account = None

    while True:
        print("\n===== BANKING SYSTEM =====")
        print("1. Create Account")
        print("2. Login")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. View Balance")
        print("6. View Transactions")
        print("7. Unlock Account")
        print("8. Logout")
        print("9. Exit")
        print("=============================")

        choice = input("Enter your choice: ")

        if choice == '1' :
            try :
                name = input('Enter the name of the account holder :')
                pin = input('Enter the pin number of the account :')
                deposit = float(input('Enter the initial deposit :'))
                account_number = service.create_account(name,pin,deposit)
                print('Your account is created successfully.!')
                print('Account Number :',account_number)
            
            except BankingException as e:
                print("Error:", e)
            except Exception as e:
                print("Unexpected system error:", e)
        
        elif choice == '2':
            try:
                account_number = int(input('Enter account number :'))
                pin = input('Enter the PIN :')
                service.authenticate(account_number,pin)
                token = generate_token(account_number)
                current_token = token
                current_account = account_number

                print('Login Successful.')
                print('JWT Token :',token)
            except BankingException as e:
                print('Error:',e)
            except Exception as e:
                print('Error:',e)

        elif choice == '3':
            try :
                if not current_token:
                    print('Please login first.')
                    continue
                deposit = float(input('Enter the deposit amount :'))
                new_balance = service.deposit(current_account,deposit)
                print('Amount is deposited successfully.!')
                print('Balance :',new_balance)
            
            except BankingException as e:
                print("Error:", e)
            except Exception as e:
                print("Unexpected system error:", e)
            
        elif choice == '4':
            try :
                if not current_token:
                    print('Please login first.')
                    continue
                withdrawn = float(input('Enter the withdraw amount :'))
                new_balance = service.withdraw(current_account,withdrawn)
                print('Amount is withdrawn successfully.!')
                print('Balance :',new_balance)
            
            
            except BankingException as e:
                print("Error:", e)
            except Exception as e:
                print('Unexpected system error :',e)
        
        elif choice == '5':
            try :
                if not current_token:
                    print('Please login first.')
                    continue
                current_balance = service.view_balance(current_account)
                print('Current Balance :',current_balance)
            
            except BankingException as e:
                print("Error:", e)
            except Exception as e:
                print('Unexpected system error :',e)
        
        elif choice == '6':
            try:
                if not current_token:
                    print('Please login first.')
                    continue
                transactions = service.view_transactions(current_account)
                if not transactions:
                    print('No transactions found.')
                    continue
                else :
                    print('\n-----Transaction History:-----')
                    for txn in transactions:
                        print(txn.transaction_type,"| Amount :",txn.amount,"| Balance After :",txn.balance_after,"| Time :",txn.timestamp)
                    print('---------------------------------\n')

            except BankingException as e:
                print("Error:", e)
            except Exception as e:
                print('Unexpected system error :',e)
        
        elif choice == '7':
            try :
                account_number=int(input('Enter the account number :'))
                admin_pin = input('Enter theadmin  pin number of the account :')
                account_number = service.unlock_account(account_number,admin_key)
                print("Account unlocked successfully.")
            except BankingException as e:
                print("Error",e)
            except Exception as e:
                print("Error:",e)
        elif choice == '8':
            if not current_token:
                print('No user is currently logged in.')
            else :
                current_token = None
                current_account = None
                print('Logged out successfully.')
        elif choice == '9':
            print("Exiting system. Goodbye!")
            break
        
        else :
            print("Invalid choice. Please try again.")