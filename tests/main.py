from bitcoinpython import network


print(network.get_fee('fast'),network.get_fee('medium'),network.get_fee('slow'))