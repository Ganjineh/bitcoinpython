from bitcoinpython import Key, PrivateKeyTestnet
from cashaddress import convert


k = Key('L3KavUvcjBj7pzKBMS4doKyJpBY4nJJbm31VnVwhcC26mTvCP3Lh')
# k = PrivateKeyTestnet('cPW1zL9JJzgTKwQyHYeQ8KE5Cdo33fGE15QcZiWDCWKHhU43KsU2')
# print(k.public_key)
print(k.address)
# print(k._public_key)
# print(k.public_point)
address = convert.to_legacy_address(k.address)
print(address)
# bchaddr = convert.to_cash_address(address)
# print(bchaddr)
# print(k.to_wif())
print(k.get_balance(currency='satoshi'))
# print(k.unspents)
# print(k.transactions)
print(k.get_unspents())
# tx = k.create_transaction([('bitcoincash:qqz4lzmnqwq3ducsqp2mgxaptqv2v6gcyvdxxlz95j', 0.0001, 'bch')])

# print(tx)