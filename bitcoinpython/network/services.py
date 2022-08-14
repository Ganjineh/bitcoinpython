import logging

import requests
from cashaddress import convert as cashaddress
from decimal import Decimal

from bitcoinpython.network import currency_to_satoshi
from bitcoinpython.network.meta import Unspent
from bitcoinpython.network.transaction import Transaction, TxPart

DEFAULT_TIMEOUT = 30

BCH_TO_SAT_MULTIPLIER = 100000000


def set_service_timeout(seconds):
    global DEFAULT_TIMEOUT
    DEFAULT_TIMEOUT = seconds


class InsightAPI:
    MAIN_ENDPOINT = ''
    MAIN_ADDRESS_API = ''
    MAIN_BALANCE_API = ''
    MAIN_UNSPENT_API = ''
    MAIN_TX_PUSH_API = ''
    MAIN_TX_API = ''
    MAIN_TX_AMOUNT_API = ''
    TX_PUSH_PARAM = ''

    @classmethod
    def get_tx_amount(cls, txid, txindex):
        r = requests.get(cls.MAIN_TX_AMOUNT_API.format(
            txid), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)
        return (Decimal(response['vout'][txindex]['value']) * BCH_TO_SAT_MULTIPLIER).normalize()

    @classmethod
    def broadcast_tx(cls, tx_hex):  # pragma: no cover
        r = requests.post(cls.MAIN_TX_PUSH_API, json={
                          cls.TX_PUSH_PARAM: tx_hex, 'network': 'mainnet', 'coin': 'BCH'}, timeout=DEFAULT_TIMEOUT)
        return True if r.status_code == 200 else False


class BitcoinDotComAPI():
    """ rest.bitcoin.com API """
    MAIN_ENDPOINT = 'https://rest.bitcoin.com/v2/'
    MAIN_ADDRESS_API = MAIN_ENDPOINT + 'address/details/{}'
    MAIN_UNSPENT_API = MAIN_ENDPOINT + 'address/utxo/{}'
    MAIN_TX_PUSH_API = MAIN_ENDPOINT + 'rawtransactions/sendRawTransaction/{}'
    MAIN_TX_API = MAIN_ENDPOINT + 'transaction/details/{}'
    MAIN_TX_AMOUNT_API = MAIN_TX_API
    MAIN_RAW_API = MAIN_ENDPOINT + 'transaction/details/{}'
    TX_PUSH_PARAM = 'rawtx'

    @classmethod
    def get_balance(cls, address):
        r = requests.get(cls.MAIN_ADDRESS_API.format(address),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        data = r.json()
        balance = data['balanceSat'] + data['unconfirmedBalanceSat']
        return balance

    @classmethod
    def get_transactions(cls, address):
        r = requests.get(cls.MAIN_ADDRESS_API.format(address),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        tnxs = []
        n = 0
        for i in r.json()['transactions']:
            tnxs.append(cls.get_transaction(i))
            n += 1
            if n == 30:
                break
        return tnxs

    @classmethod
    def get_transaction(cls, txid):
        r = requests.get(cls.MAIN_TX_API.format(txid),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json()
        return response

    @classmethod
    def get_tx_amount(cls, txid, txindex):
        r = requests.get(cls.MAIN_TX_AMOUNT_API.format(
            txid), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)
        return (Decimal(response['vout'][txindex]['value']) * BCH_TO_SAT_MULTIPLIER).normalize()

    @classmethod
    def get_unspent(cls, address):
        r = requests.get(cls.MAIN_UNSPENT_API.format(address),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        outputs = []
        last_txid = ''
        for tx in r.json()['utxos']:
            if not tx['txid'] == last_txid:
                last_txid = tx['txid']
                outputs.append(Unspent(currency_to_satoshi(tx['amount'], 'bch'),
                    tx['confirmations'],
                    r.json()['scriptPubKey'],
                    tx['txid'],
                    tx['vout']))
        return outputs

    @classmethod
    def get_raw_transaction(cls, txid):
        r = requests.get(cls.MAIN_RAW_API.format(
            txid), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json(parse_float=Decimal)
        return response

    @classmethod
    def broadcast_tx(cls, tx_hex):  # pragma: no cover
        r = requests.get(cls.MAIN_TX_PUSH_API.format(tx_hex))
        return True if r.status_code == 200 else False


class FullstackDotCash():
    """ api.fullstack.cash """
    MAIN_ENDPOINT = 'https://api.fullstack.cash/v5/'
    MAIN_TX_PUSH_API = MAIN_ENDPOINT + 'rawtransactions/sendRawTransaction/{}'
    MAIN_TX_API = MAIN_ENDPOINT + 'electrumx/tx/data/{}'

    @classmethod
    def get_balance(cls, address):
        pass

    @classmethod
    def get_transactions(cls, address):
        pass

    @classmethod
    def get_transaction(cls, txid):
        r = requests.get(cls.MAIN_TX_API.format(txid),
                         timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        response = r.json()
        return response

    @classmethod
    def get_tx_amount(cls, txid, txindex):
        pass

    @classmethod
    def get_unspent(cls, address):
        pass

    @classmethod
    def get_raw_transaction(cls, txid):
        pass

    @classmethod
    def broadcast_tx(cls, tx_hex):  # pragma: no cover
        r = requests.get(cls.MAIN_TX_PUSH_API.format(tx_hex))
        return True if r.status_code == 200 else False


class BitcoreAPI(InsightAPI):
    """ Insight API v8 """
    MAIN_ENDPOINT = 'https://api.bitcore.io/api/BCH/mainnet/'
    MAIN_ADDRESS_API = MAIN_ENDPOINT + 'address/{}'
    MAIN_BALANCE_API = MAIN_ADDRESS_API + '/balance'
    MAIN_UNSPENT_API = MAIN_ADDRESS_API + '/?unspent=true&limit=1000'
    MAIN_TX_PUSH_API = MAIN_ENDPOINT + 'tx/send'
    MAIN_TX_API = MAIN_ENDPOINT + 'tx/{}'
    MAIN_TX_AMOUNT_API = MAIN_TX_API
    """ for BTC  """
    MAIN_ENDPOINT_BTC = 'https://api.bitcore.io/api/BTC/mainnet/'
    MAIN_ADDRESS_API_BTC = MAIN_ENDPOINT_BTC + 'address/{}'
    MAIN_BALANCE_API_BTC = MAIN_ADDRESS_API_BTC + '/balance'
    MAIN_UNSPENT_API_BTC = MAIN_ADDRESS_API_BTC + '/?unspent=true&limit=1000'
    MAIN_TX_PUSH_API_BTC = MAIN_ENDPOINT_BTC + 'tx/send'
    MAIN_TX_API_BTC = MAIN_ENDPOINT_BTC + 'tx/{}'
    MAIN_TX_AMOUNT_API_BTC = MAIN_TX_API_BTC

    @classmethod
    def get_unspent(cls, address):
        address = address.replace('bitcoincash:', '')
        r = requests.get(cls.MAIN_UNSPENT_API.format(
            address), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return [
            Unspent(currency_to_satoshi(tx['value'], 'satoshi'),
                    tx['confirmations'],
                    tx['script'],
                    tx['mintTxid'],
                    tx['mintIndex'])
            for tx in r.json()
        ]

    @classmethod
    def get_unspent_btc(cls, address):
        r = requests.get(cls.MAIN_UNSPENT_API_BTC.format(
            address), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return [
            Unspent(currency_to_satoshi(tx['value'], 'satoshi'),
                    tx['confirmations'],
                    tx['script'],
                    tx['mintTxid'],
                    tx['mintIndex'])
            for tx in r.json()
        ]

    @classmethod
    def get_transactions(cls, address):
        address = address.replace('bitcoincash:', '')
        r = requests.get(cls.MAIN_ADDRESS_API.format(
            address), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return [tx['mintTxid'] for tx in r.json()]

    @classmethod
    def get_transactions_btc(cls, address):
        r = requests.get(cls.MAIN_ADDRESS_API_BTC.format(
            address), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return r.json()

    @classmethod
    def get_transaction_btc(cls, txid):
        r = requests.get(cls.MAIN_TX_API_BTC.format(
            txid), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return r.json()

    @classmethod
    def get_balance(cls, address):
        r = requests.get(cls.MAIN_BALANCE_API.format(
            address), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return r.json()['balance']

    @classmethod
    def get_balance_btc(cls, address):
        r = requests.get(cls.MAIN_BALANCE_API_BTC.format(
            address), timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # pragma: no cover
        return r.json()['balance']


class TatumApi(InsightAPI):
    """ Insight API v8 """
    MAIN_ENDPOINT = 'https://api-eu1.tatum.io/v3/bcash/'
    """ for BTC  """
    MAIN_ENDPOINT_BTC = 'https://api-eu1.tatum.io/v3/bitcoin/'
    MAIN_TX_API_BTC = MAIN_ENDPOINT_BTC + 'transaction/{}'

    @classmethod
    def get_unspent(cls, address):
        pass

    @classmethod
    def get_unspent_btc(cls, address):
        pass

    @classmethod
    def get_transactions(cls, address):
        pass

    @classmethod
    def get_transactions_btc(cls, address):
        pass

    @classmethod
    def get_transaction_btc(cls, txid, x_api_key=None):
        headers = {
            "x-api-key": x_api_key
        }
        r = requests.get(cls.MAIN_TX_API_BTC.format(txid, x_api_key), timeout=DEFAULT_TIMEOUT, headers=headers)
        r.raise_for_status()
        return r.json()

    @classmethod
    def get_balance(cls, address):
        pass

    @classmethod
    def get_balance_btc(cls, address):
        pass


class NetworkAPI:
    IGNORED_ERRORS = (
        requests.exceptions.RequestException,
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.ProxyError,
        requests.exceptions.SSLError,
        requests.exceptions.Timeout,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
        requests.exceptions.TooManyRedirects,
        requests.exceptions.ChunkedEncodingError,
        requests.exceptions.ContentDecodingError,
        requests.exceptions.StreamConsumedError,
    )

    # Mainnet
    GET_BALANCE_MAIN = [BitcoinDotComAPI.get_balance,
                        BitcoreAPI.get_balance]
    GET_BALANCE_MAIN_BTC = [BitcoreAPI.get_balance_btc]
    GET_TRANSACTIONS_MAIN = [BitcoinDotComAPI.get_transactions,
                             BitcoreAPI.get_transactions]
    GET_TRANSACTIONS_MAIN_BTC = [BitcoreAPI.get_transactions_btc]
    GET_TRANSACTION_MAIN_BTC = [TatumApi.get_transaction_btc]

    GET_UNSPENT_MAIN = [BitcoinDotComAPI.get_unspent,
                        BitcoreAPI.get_unspent]
    GET_UNSPENT_MAIN_BTC = [BitcoreAPI.get_unspent_btc]
    BROADCAST_TX_MAIN = [FullstackDotCash.broadcast_tx, 
                        BitcoinDotComAPI.broadcast_tx,
                        BitcoreAPI.broadcast_tx]
    GET_TX_MAIN = [FullstackDotCash.get_transaction,
                    BitcoinDotComAPI.get_transaction]
    GET_TX_AMOUNT_MAIN = [BitcoinDotComAPI.get_tx_amount,
                          BitcoreAPI.get_tx_amount]
    GET_RAW_TX_MAIN = [BitcoinDotComAPI.get_raw_transaction]

    @classmethod
    def get_balance(cls, address):
        """Gets the balance of an address in satoshi.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``int``
        """

        for api_call in cls.GET_BALANCE_MAIN:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_balance_btc(cls, address):
        """Gets the balance of an address in satoshi.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``int``
        """

        for api_call in cls.GET_BALANCE_MAIN_BTC:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_transactions(cls, address):
        """Gets the ID of all transactions related to an address.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``list`` of ``str``
        """

        for api_call in cls.GET_TRANSACTIONS_MAIN:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_transactions_btc(cls, address):
        """Gets the ID of all transactions related to an address.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``list`` of ``str``
        """

        for api_call in cls.GET_TRANSACTIONS_MAIN_BTC:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_transaction(cls, txid):
        """Gets the full transaction details.

        :param txid: The transaction id in question.
        :type txid: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``Transaction``
        """

        for api_call in cls.GET_TX_MAIN:
            try:
                return api_call(txid)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')
    @classmethod
    def get_transaction_btc(cls, txid, x_api_key=None):
        """Gets the full transaction details.

        :param txid: The transaction id in question.
        :type txid: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``Transaction``
        """

        for api_call in cls.GET_TRANSACTION_MAIN_BTC:
            try:
                return api_call(txid, x_api_key)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_tx_amount(cls, txid, txindex):
        """Gets the amount of a given transaction output.

        :param txid: The transaction id in question.
        :type txid: ``str``
        :param txindex: The transaction index in question.
        :type txindex: ``int``
        :raises ConnectionError: If all API services fail.
        :rtype: ``Decimal``
        """

        for api_call in cls.GET_TX_AMOUNT_MAIN:
            try:
                return api_call(txid, txindex)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_unspent(cls, address):
        """Gets all unspent transaction outputs belonging to an address.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``list`` of :class:`~bitcash.network.meta.Unspent`
        """

        for api_call in cls.GET_UNSPENT_MAIN:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_unspent_btc(cls, address):
        """Gets all unspent transaction outputs belonging to an address.

        :param address: The address in question.
        :type address: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``list`` of :class:`~bitcash.network.meta.Unspent`
        """

        for api_call in cls.GET_UNSPENT_MAIN_BTC:
            try:
                return api_call(address)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def get_raw_transaction(cls, txid):
        """Gets the raw, unparsed transaction details.

        :param txid: The transaction id in question.
        :type txid: ``str``
        :raises ConnectionError: If all API services fail.
        :rtype: ``Transaction``
        """

        for api_call in cls.GET_RAW_TX_MAIN:
            try:
                return api_call(txid)
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def broadcast_tx(cls, tx_hex):  # pragma: no cover
        """Broadcasts a transaction to the blockchain.

        :param tx_hex: A signed transaction in hex form.
        :type tx_hex: ``str``
        :raises ConnectionError: If all API services fail.
        """
        success = None

        for api_call in cls.BROADCAST_TX_MAIN:
            try:
                success = api_call(tx_hex)
                if not success:
                    continue
                return
            except cls.IGNORED_ERRORS:
                pass

        if success is False:
            raise ConnectionError('Transaction broadcast failed, or '
                                  'Unspents were already used.')

        raise ConnectionError('All APIs are unreachable.')
