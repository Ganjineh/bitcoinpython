from bitcoinpython import Key
from cashaddress import convert
from bitcoinpython import get_balance, get_balance_btc,get_transactions_btc



k = Key('L3KavUvcjBj7pzKBMS4doKyJpBY4nJJbm31VnVwhcC26mTvCP3Lh')
# k = PrivateKeyTestnet('cPW1zL9JJzgTKwQyHYeQ8KE5Cdo33fGE15QcZiWDCWKHhU43KsU2')
# print(k.public_key)
print(k.address)
# print(k._public_key)
# print(k.public_point)
address = convert.to_legacy_address(k.address)
print(address)
bchaddr = convert.to_cash_address('13A8QNwEeuYyvcPSJwR4F5xDr6RUryLVfw')
# print(bchaddr)
# print(k.to_wif())
print(k.get_balance(currency='satoshi'))
# print(k.unspents)
# print(k.transactions)
print(k.get_transactions())
print(k.get_unspents())
txid = k.send([('13A8QNwEeuYyvcPSJwR4F5xDr6RUryLVfw', 0.01001, 'bch')],fee=452)
print(txid)

print(get_balance('qz7xc0vl85nck65ffrsx5wvewjznp9lflgktxc5878', currency='bch'))
print(get_balance_btc('bc1q5j8j9y55mc05ws84smk36ndau4ptj9yj72eldz', currency='BTC'))

print(get_transactions_btc('38UmuUqPCrFmQo4khkomQwZ4VbY2nZMJ67'))