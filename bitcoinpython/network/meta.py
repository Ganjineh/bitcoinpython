TX_TRUST_LOW = 1
TX_TRUST_MEDIUM = 6
TX_TRUST_HIGH = 30


class Unspent:
    """Represents an unspent transaction output (UTXO)."""
    __slots__ = ('amount', 'confirmations', 'script', 'txid', 'txindex')

    def __init__(self, amount, confirmations, txid):
        self.amount = amount
        self.confirmations = confirmations
        self.txid = txid

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in Unspent.__slots__}

    @classmethod
    def from_dict(cls, d):
        return Unspent(**{attr: d[attr] for attr in Unspent.__slots__})

    def __eq__(self, other):
        return (self.amount == other.amount and
                self.txid == other.txid )

    def __repr__(self):
        return 'Unspent(amount={}, confirmations={}, txid={})'.format(
            repr(self.amount),
            repr(self.confirmations),
            repr(self.txid),
        )
