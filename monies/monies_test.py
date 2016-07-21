r"""
>>> from importlib import reload

We should be able to create a client
>>> import monies
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> Anastasia.first_name
'Anastasia'
>>> Anastasia.last_name
'Kukanova'
>>> Anastasia.accessible_accounts
[]

Creating a client with no personal data is invalid
>>> monies = reload(monies)
>>> client1 = monies.Client(first_name='Nope')
Traceback (most recent call last):
ValueError: a client must have a first name and a last name
>>> monies = reload(monies)
>>> client1 = monies.Client(first_name='Nope', last_name='')
Traceback (most recent call last):
ValueError: a client must have a first name and a last name
>>> monies = reload(monies)
>>> client1 = monies.Client(last_name='Nope')
Traceback (most recent call last):
ValueError: a client must have a first name and a last name
>>> monies = reload(monies)
>>> client1 = monies.Client(last_name='Nope', first_name='')
Traceback (most recent call last):
ValueError: a client must have a first name and a last name

We should be able to create a bank account with one client having access to it.
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> Anastasia.accessible_accounts
[]
>>> account1 = monies.Account(holder=Anastasia)
>>> len(account1.holders)
1
>>> account1.holders[0].first_name
'Anastasia'
>>> account1.holders[0].last_name
'Kukanova'
>>> len(Anastasia.accessible_accounts)
1
>>> import decimal
>>> isinstance(account1.balance, decimal.Decimal)
True
>>> str(account1.balance)
'0.00'

Creating an account without a holder is invalid
>>> monies = reload(monies)
>>> account1 = monies.Account()
Traceback (most recent call last):
ValueError: an account must have at least one holder

A client should be able to deposit money to an accessible account
Integer input
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> str(account1.balance)
'0.00'
>>> account1.deposit(client=Anastasia, amount=1000)
>>> decimal = reload(decimal)
>>> isinstance(account1.balance, decimal.Decimal)
True
>>> str(account1.balance)
'1000.00'

Float input
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> str(account1.balance)
'0.00'
>>> account1.deposit(client=Anastasia, amount=1000.0)
>>> decimal = reload(decimal)
>>> isinstance(account1.balance, decimal.Decimal)
True
>>> str(account1.balance)
'1000.00'

Deposit amount has to be 0.01 or more
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=0.0001)
Traceback (most recent call last):
ValueError: minimal deposit amount is 0.01

Only a holder should be able to deposit money to the account
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account1.deposit(client=Maria, amount=1000)
Traceback (most recent call last):
ValueError: the client has to be a holder of the account

A client should be able to withdraw money from an accessible account:
Integer input
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> str(account1.balance)
'1000.00'
>>> account1.withdraw(client=Anastasia, amount=500)
>>> decimal = reload(decimal)
>>> isinstance(account1.balance, decimal.Decimal)
True
>>> str(account1.balance)
'500.00'

Float input
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> str(account1.balance)
'1000.00'
>>> account1.withdraw(client=Anastasia, amount=500.0)
>>> decimal = reload(decimal)
>>> isinstance(account1.balance, decimal.Decimal)
True
>>> str(account1.balance)
'500.00'

Withdrawal amount has to be 0.01 or more
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> account1.withdraw(client=Anastasia, amount=0.0001)
Traceback (most recent call last):
ValueError: minimal withdrawal amount is 0.01

A client can't withdraw more money than there is in the account
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.withdraw(client=Anastasia, amount=1500)
Traceback (most recent call last):
ValueError: amount of withdrawal cannot exceed the balance of the account

The client has to be a holder of the account
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account1.withdraw(client=Maria, amount=500)
Traceback (most recent call last):
ValueError: the client has to be a holder of the account

It should be possible to add another holder to the account
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> len(account1.holders)
1
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> Maria.accessible_accounts
[]
>>> account1.add_holder(Maria)
>>> len(account1.holders)
2
>>> account1.holders[-1].first_name
'Maria'
>>> account1.holders[-1].last_name
'Petrova'
>>> len(Maria.accessible_accounts)
1

If the client is already a holder of the account, he shouldn't be added again
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.add_holder(Anastasia)
Traceback (most recent call last):
ValueError: the client is already a holder of the account

We should be able to remove a holder of an account.
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account1.add_holder(Maria)
>>> len(account1.holders)
2
>>> account1.remove_holder(Anastasia)
>>> len(account1.holders)
1

We shouldn't be able to remove the last holder of the account.
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> len(account1.holders)
1
>>> account1.remove_holder(Anastasia)
Traceback (most recent call last):
ValueError: an account must have at least one holder

If the client is not a holder the account, he cannot be removed
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account1.remove_holder(Maria)
Traceback (most recent call last):
ValueError: the client is not a holder of the account

We should be able to create a valid transaction.
Integer amount input
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies.Account(holder=Maria)
>>> transaction1 = monies.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500)
>>> transaction1.is_executed
False

Float amount input
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies.Account(holder=Maria)
>>> transaction1 = monies.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500.0)
>>> transaction1.is_executed
False

The clients have to be holders of the corresponding accounts.
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account2 = monies.Account(holder=Anastasia)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> transaction1 = monies.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500)
Traceback (most recent call last):
ValueError: the client is not a holder of the account

>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account1 = monies.Account(holder=Maria)
>>> account2 = monies.Account(holder=Maria)
>>> transaction1 = monies.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500)
Traceback (most recent call last):
ValueError: the client is not a holder of the account

Sender account and receiver account have to be different.
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account1.add_holder(Maria)
>>> transaction1 = monies.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account1,
...                                   amount=500)
Traceback (most recent call last):
ValueError: the sender account and the receiver account have to be different

The amount of transaction has to be 0.01 or more
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies.Account(holder=Maria)
>>> transaction1 = monies.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=0.0001)
Traceback (most recent call last):
ValueError: minimal transaction amount is 0.01

The amount of transaction can't exceed the balance of the sender account
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies.Account(holder=Maria)
>>> transaction1 = monies.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=1500)
Traceback (most recent call last):
ValueError: amount of transaction cannot exceed the balance of the sender account

A valid transaction should be able to be executed
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> str(account1.balance)
'1000.00'
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies.Account(holder=Maria)
>>> str(account2.balance)
'0.00'
>>> transaction1 = monies.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500)
>>> transaction1.execute()
>>> str(account1.balance)
'500.00'
>>> str(account2.balance)
'500.00'
>>> transaction1.is_executed
True

An executed transaction cannot be executed again
>>> monies = reload(monies)
>>> Anastasia = monies.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies.Account(holder=Maria)
>>> transaction1 = monies.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500)
>>> transaction1.execute()
>>> transaction1.is_executed
True
>>> transaction1.execute()
Traceback (most recent call last):
ValueError: this transaction has already been executed
"""