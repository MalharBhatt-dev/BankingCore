from repository.account_repository import AccountRepository
from services.banking_services import BankingServices
from exceptions.base_exception import BankingException

#! DEPENDENCY INJECTION IS ACHIEVED HERE↓
if __name__ == "__main__":
    repo = AccountRepository()
    service = BankingServices(repo)

    while True:
        print("\n===== BANKING SYSTEM =====")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. View Balance")
        print("5. View Transactions")
        print("6. Exit")
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
            try :
                account_number=int(input('Enter the account number :'))
                pin = input('Enter the pin number of the account :')
                deposit = float(input('Enter the deposit amount :'))
                new_balance = service.deposit(account_number,pin,deposit)
                print('Amount is deposited successfully.!')
                print('Balance :',new_balance)
            
            except BankingException as e:
                print("Error:", e)
            except Exception as e:
                print("Unexpected system error:", e)
            
        elif choice == '3':
            try :
                account_number=int(input('Enter the account number :'))
                pin = input('Enter the pin number of the account :')
                withdrawn = float(input('Enter the withdraw amount :'))
                new_balance = service.withdraw(account_number,pin,withdrawn)
                print('Amount is withdrawn successfully.!')
                print('Balance :',new_balance)
            
            
            except BankingException as e:
                print("Error:", e)
            except Exception as e:
                print('Unexpected system error :',e)
        
        elif choice == '4':
            try :
                account_number=int(input('Enter the account number :'))
                pin = input('Enter the pin number of the account :')
                current_balance = service.view_balance(account_number,pin)
                print('Current Balance :',current_balance)
            
            except BankingException as e:
                print("Error:", e)
            except Exception as e:
                print('Unexpected system error :',e)
        
        elif choice == '5':
            try:
                account_number=int(input('Enter the account number :'))
                pin = input('Enter the pin number of the account :')
                transactions = service.view_transactions(account_number,pin)
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
        
        elif choice == '6':
            print("Exiting system. Goodbye!")
            break
        
        else :
            print("Invalid choice. Please try again.")