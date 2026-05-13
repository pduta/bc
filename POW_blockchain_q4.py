import hashlib
import json
from datetime import datetime

class Block:
    """Represents a single block in the blockchain."""
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0 # Nonce is used for proof-of-work
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Generates the hash for the current block contents."""
        # Concatenate all block attributes to create a single string for hashing
        block_string = json.dumps({
            'index': self.index,
            'timestamp': str(self.timestamp),
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    """Manages the chain of blocks."""
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Creates the first block (genesis block) in the chain."""
        # The genesis block has no previous hash, so a '0' is used
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        """Adds a new block to the blockchain."""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        # Reset the list of new transactions
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        """Adds a new transaction to the list of pending transactions."""
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        # Returns the index of the block that the transaction will be added to
        return self.get_latest_block()['index'] + 1

    def get_latest_block(self):
        """Returns the last block in the chain."""
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """Creates a SHA-256 hash of a block."""
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

# Example Usage
if __name__ == '__main__':
    my_blockchain = Blockchain()

    # Add transactions
    my_blockchain.add_transaction("Alice", "Bob", 50)
    my_blockchain.add_transaction("Bob", "Charlie", 25)

    # Add a new block (mining process is simulated with simple proof)
    last_block = my_blockchain.get_latest_block()
    previous_hash = my_blockchain.hash(last_block)
    # A simple proof of work value is used here for brevity
    my_blockchain.create_block(proof=12345, previous_hash=previous_hash)

    print("Blockchain contents:")
    for block in my_blockchain.chain:
        print(json.dumps(block, indent=4))
        print("-" * 20)
