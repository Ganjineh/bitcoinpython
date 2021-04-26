from bitcoinpython.network import NetworkAPI, get_fee, satoshi_to_currency_cached



def get_balance(address, currency='satoshi'):
    unspents = []
    balance = 0
    unspents[:] = NetworkAPI.get_unspent(address)
    balance = sum(unspent.amount for unspent in unspents)    
    return satoshi_to_currency_cached(balance, currency.lower())

def get_balance_btc(address, currency='satoshi'):
    unspents = []
    balance = 0
    unspents[:] = NetworkAPI.get_unspent_btc(address)
    balance = sum(unspent.amount for unspent in unspents)    
    return satoshi_to_currency_cached(balance, currency.lower())


def get_transactions(address):
    transactions = []
    """Fetches transaction history.

    :rtype: ``list`` of ``str`` transaction IDs
    """
    transactions[:] = NetworkAPI.get_transactions(address)
    return transactions

def get_transactions_btc(address):
    transactions = []
    """Fetches transaction history.

    :rtype: ``list`` of ``str`` transaction IDs
    """
    transactions[:] = NetworkAPI.get_transactions_btc(address)
    return transactions