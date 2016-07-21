import decimal as dec

def _convert_amount(amount):
    if isinstance(amount, int):
        amount = dec.Decimal(amount)
    elif isinstance(amount, float):
        amount = dec.Decimal(amount) // dec.Decimal('0.01') * dec.Decimal('0.01')
    else:
        raise TypeError('`amount` has to be `int` or `float`')
    return amount


class Client():
    def __init__(self, first_name='', last_name=''):
        if first_name == '' or last_name == '':
            raise ValueError('a client must have a first name and a last name')
        self.first_name = first_name
        self.last_name = last_name
        self.accessible_accounts = []


class Account():
    def __init__(self, holder=None):
        if holder is None:
            raise ValueError('an account must have at least one holder')
        self.holders = [holder]
        holder.accessible_accounts.append(self)
        self.balance = dec.Decimal('0.00')

    def deposit(self, client=None, amount=0):
        if client not in self.holders:
            raise ValueError('the client has to be a holder of the account')
        amount = _convert_amount(amount)
        if amount < dec.Decimal('0.01'):
            raise ValueError('minimal deposit amount is 0.01')
        self.balance += amount

    def withdraw(self, client=None, amount=0):
        if client not in self.holders:
            raise ValueError('the client has to be a holder of the account')
        amount = _convert_amount(amount)
        if amount < dec.Decimal('0.01'):
            raise ValueError('minimal withdrawal amount is 0.01')
        if amount > self.balance:
            raise ValueError('amount of withdrawal cannot exceed the balance of the account')
        self.balance -= amount

    def add_holder(self, client):
        if client in self.holders:
            raise ValueError('the client is already a holder of the account')
        self.holders.append(client)
        client.accessible_accounts.append(self)

    def remove_holder(self, client):
        if client not in self.holders:
            raise ValueError('the client is not a holder of the account')
        if len(self.holders) == 1:
            raise ValueError('an account must have at least one holder')
        self.holders.remove(client)
        client.accessible_accounts.remove(self)


class Transaction():
    def __init__(self, sender, sender_account, receiver, receiver_account, amount):
        if sender not in sender_account.holders or receiver not in receiver_account.holders:
            raise ValueError('the client is not a holder of the account')
        if sender_account == receiver_account:
            raise ValueError('the sender account and the receiver account have to be different')
        amount = _convert_amount(amount)
        if amount < dec.Decimal('0.01'):
            raise ValueError('minimal transaction amount is 0.01')
        if amount > sender_account.balance:
            raise ValueError('amount of transaction cannot exceed the balance of the sender account')
        self.sender = sender
        self.sender_account = sender_account
        self.receiver = receiver
        self.receiver_account = receiver_account
        self.amount = amount
        self.is_executed = False

    def execute(self):
        if self.is_executed:
            raise ValueError('this transaction has already been executed')
        self.sender_account.balance -= self.amount
        self.receiver_account.balance += self.amount
        self.is_executed = True
