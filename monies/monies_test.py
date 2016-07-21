r"""
>>> from importlib import reload

It is be possible to create a client object.
>>> import monies.monies_main as monies_main
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> Anastasia.first_name
'Anastasia'
>>> Anastasia.last_name
'Kukanova'
>>> Anastasia.accessible_accounts
[]

Creating a client object with no first name or no last name is invalid.
>>> monies_main = reload(monies_main)
>>> client1 = monies_main.Client(first_name='Nope')
Traceback (most recent call last):
monies.monies_exc.InvalidClientName: a client must have a first name and a last name
>>> monies_main = reload(monies_main)
>>> client1 = monies_main.Client(first_name='Nope', last_name='')
Traceback (most recent call last):
monies.monies_exc.InvalidClientName: a client must have a first name and a last name
>>> monies_main = reload(monies_main)
>>> client1 = monies_main.Client(last_name='Nope')
Traceback (most recent call last):
monies.monies_exc.InvalidClientName: a client must have a first name and a last name
>>> monies_main = reload(monies_main)
>>> client1 = monies_main.Client(last_name='Nope', first_name='')
Traceback (most recent call last):
monies.monies_exc.InvalidClientName: a client must have a first name and a last name

It is be possible to create a bank account with exactly one client having access to it.
Adding more account holders is implemented as a method.
Balance is stored as a number with a fixed point.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> Anastasia.accessible_accounts
[]
>>> account1 = monies_main.Account(holder=Anastasia)
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

Creating an account without a holder is invalid.
>>> monies_main = reload(monies_main)
>>> account1 = monies_main.Account()
Traceback (most recent call last):
monies.monies_exc.ZeroHolders: an account must have at least one holder


A client can deposit money to an accessible account.
The deposit amount input can be of `int` type.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> str(account1.balance)
'0.00'
>>> account1.deposit(client=Anastasia, amount=1000)
>>> decimal = reload(decimal)
>>> isinstance(account1.balance, decimal.Decimal)
True
>>> str(account1.balance)
'1000.00'

It can also be of `float` type.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> str(account1.balance)
'0.00'
>>> account1.deposit(client=Anastasia, amount=1000.0)
>>> decimal = reload(decimal)
>>> isinstance(account1.balance, decimal.Decimal)
True
>>> str(account1.balance)
'1000.00'

Deposit amount has to be 0.01 or more.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=0.0001)
Traceback (most recent call last):
monies.monies_exc.MinimalAmountNotMet: minimal deposit amount is 0.01

Only a holder can deposit money to the account.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account1.deposit(client=Maria, amount=1000)
Traceback (most recent call last):
monies.monies_exc.NotHolder: the client has to be a holder of the account

A client can withdraw money from an accessible account.
The withdrawal amount input can be of `int` type.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> str(account1.balance)
'1000.00'
>>> account1.withdraw(client=Anastasia, amount=500)
>>> decimal = reload(decimal)
>>> isinstance(account1.balance, decimal.Decimal)
True
>>> str(account1.balance)
'500.00'

It can also be of `float` type.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> str(account1.balance)
'1000.00'
>>> account1.withdraw(client=Anastasia, amount=500.0)
>>> decimal = reload(decimal)
>>> isinstance(account1.balance, decimal.Decimal)
True
>>> str(account1.balance)
'500.00'

Withdrawal amount has to be 0.01 or more.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> account1.withdraw(client=Anastasia, amount=0.0001)
Traceback (most recent call last):
monies.monies_exc.MinimalAmountNotMet: minimal withdrawal amount is 0.01

A holder can't withdraw more money than the account stores.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.withdraw(client=Anastasia, amount=1500)
Traceback (most recent call last):
monies.monies_exc.BalanceExceeded: amount of withdrawal cannot exceed the balance of the account

Only a holder can withdraw money from the account.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account1.withdraw(client=Maria, amount=500)
Traceback (most recent call last):
monies.monies_exc.NotHolder: the client has to be a holder of the account

It is possible to add another holder to an account.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> len(account1.holders)
1
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
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

If the client is already a holder of the account, he will not added again.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.add_holder(Anastasia)
Traceback (most recent call last):
monies.monies_exc.AlreadyHolder: the client is already a holder of the account

It is possible to remove a holder of an account.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account1.add_holder(Maria)
>>> len(account1.holders)
2
>>> account1.remove_holder(Anastasia)
>>> len(account1.holders)
1

However, it is not to remove the last holder of the account.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> len(account1.holders)
1
>>> account1.remove_holder(Anastasia)
Traceback (most recent call last):
monies.monies_exc.ZeroHolders: an account must have at least one holder

If the client is not a holder the account, he cannot be removed.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account1.remove_holder(Maria)
Traceback (most recent call last):
monies.monies_exc.NotHolder: the client is not a holder of the account

It is possible to create a valid transaction.
The transaction amount input can be of `int` type.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies_main.Account(holder=Maria)
>>> transaction1 = monies_main.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500)
>>> transaction1.is_executed
False

It can also be of `float` type.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies_main.Account(holder=Maria)
>>> transaction1 = monies_main.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500.0)
>>> transaction1.is_executed
False

The clients have to be holders of the corresponding accounts.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account2 = monies_main.Account(holder=Anastasia)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> transaction1 = monies_main.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500)
Traceback (most recent call last):
monies.monies_exc.NotHolder: the clients has to be holders of the corresponding accounts

>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account1 = monies_main.Account(holder=Maria)
>>> account2 = monies_main.Account(holder=Maria)
>>> transaction1 = monies_main.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500)
Traceback (most recent call last):
monies.monies_exc.NotHolder: the clients has to be holders of the corresponding accounts

The sender account and the receiver account have to be different.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account1.add_holder(Maria)
>>> transaction1 = monies_main.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account1,
...                                   amount=500)
Traceback (most recent call last):
monies.monies_exc.SameAccountTransaction: the sender account and the receiver account have to be different

The amount of transaction has to be 0.01 or more.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies_main.Account(holder=Maria)
>>> transaction1 = monies_main.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=0.0001)
Traceback (most recent call last):
monies.monies_exc.MinimalAmountNotMet: minimal transaction amount is 0.01

The amount of transaction cannot exceed the balance of the sender account.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies_main.Account(holder=Maria)
>>> transaction1 = monies_main.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=1500)
Traceback (most recent call last):
monies.monies_exc.BalanceExceeded: amount of transaction cannot exceed the balance of the sender account

A valid transaction can be executed.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> str(account1.balance)
'1000.00'
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies_main.Account(holder=Maria)
>>> str(account2.balance)
'0.00'
>>> transaction1 = monies_main.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500)
>>> transaction1.execute()
>>> str(account1.balance)
'500.00'
>>> str(account2.balance)
'500.00'
>>> transaction1.is_executed
True

An executed transaction cannot be executed again.
>>> monies_main = reload(monies_main)
>>> Anastasia = monies_main.Client(first_name='Anastasia', last_name='Kukanova')
>>> account1 = monies_main.Account(holder=Anastasia)
>>> account1.deposit(client=Anastasia, amount=1000)
>>> Maria = monies_main.Client(first_name='Maria', last_name='Petrova')
>>> account2 = monies_main.Account(holder=Maria)
>>> transaction1 = monies_main.Transaction(sender=Anastasia, sender_account=account1,
...                                   receiver=Maria, receiver_account=account2,
...                                   amount=500)
>>> transaction1.execute()
>>> transaction1.is_executed
True
>>> transaction1.execute()
Traceback (most recent call last):
monies.monies_exc.ExecutedTransaction: this transaction has already been executed
"""

if __name__ == '__main__':
    import doctest
    doctest.testmod()
