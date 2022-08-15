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


def get_transactions(txs):
    """Fetches transaction history.

    :rtype: ``list`` of ``str`` transaction IDs
    """
    transactions = NetworkAPI.get_transactions(txs)
    return transactions


def get_transaction(txid, x_api_key=None):
    transaction = NetworkAPI.get_transaction(txid, x_api_key)
    return transaction


def get_transaction_btc(txid, x_api_key=None):
    transaction = NetworkAPI.get_transaction_btc(txid, x_api_key)
    return transaction


def get_transactions_btc(address):
    transactions = []
    """Fetches transaction history.

    :rtype: ``list`` of ``str`` transaction IDs
    """
    transactions[:] = NetworkAPI.get_transactions_btc(address)
    return transactions

def get_block_number_btc(x_api_key=None):

    block_number = NetworkAPI.get_block_number_btc(x_api_key)
    return block_number

def get_block_number(x_api_key=None):

    block_number = NetworkAPI.get_block_number(x_api_key)
    return block_number
