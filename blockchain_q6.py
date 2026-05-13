import hashlib
import json
from datetime import datetime




class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now().isoformat()


    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }


    def __repr__(self):
        return f"Transaction({self.sender} → {self.receiver}: {self.amount})"




class Block:
    def __init__(self, index: int, transactions: list[Transaction], previous_hash: str):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()


    def compute_hash(self) -> str:
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


    def mine(self, difficulty: int = 3):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()


    def __repr__(self):
        return (
            f"\n{'='*60}\n"
            f"  Block #{self.index}\n"
            f"{'='*60}\n"
            f"  Created At    : {self.timestamp}\n"
            f"  Hash          : {self.hash}\n"
            f"  Previous Hash : {self.previous_hash}\n"
            f"  Nonce         : {self.nonce}\n"
            f"  Transactions  : {len(self.transactions)}\n"
        )




class Blockchain:
    DIFFICULTY = 3


    def __init__(self):
        self.chain: list[Block] = []
        self.pending_transactions: list[Transaction] = []
        self._create_genesis_block()


    def _create_genesis_block(self):
        genesis = Block(index=0, transactions=[], previous_hash="0" * 64)
        genesis.mine(self.DIFFICULTY)
        self.chain.append(genesis)
        print(f"[Genesis block created] Hash: {genesis.hash[:20]}...")


    @property
    def last_block(self) -> Block:
        return self.chain[-1]


    def add_transaction(self, sender: str, receiver: str, amount: float):
        tx = Transaction(sender, receiver, amount)
        self.pending_transactions.append(tx)
        print(f"  + Transaction queued: {tx}")
        return tx


    def mine_block(self) -> Block | None:
        if not self.pending_transactions:
            print("  No pending transactions to mine.")
            return None


        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions[:],
            previous_hash=self.last_block.hash,
        )
        print(f"\n  Mining block #{block.index}...", end=" ", flush=True)
        block.mine(self.DIFFICULTY)
        print(f"Done! Nonce={block.nonce}")


        self.chain.append(block)
        self.pending_transactions.clear()
        return block


    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]


            if current.hash != current.compute_hash():
                print(f"  [INVALID] Block #{i} hash mismatch!")
                return False


            if current.previous_hash != previous.hash:
                print(f"  [INVALID] Block #{i} is not linked to Block #{i-1}!")
                return False


        return True


    def print_chain(self):
        print("\n" + "=" * 60)
        print("  BLOCKCHAIN LEDGER")
        print("=" * 60)
        for block in self.chain:
            print(block)
            if block.transactions:
                print("  Transaction History:")
                for tx in block.transactions:
                    print(
                        f"    [{tx.timestamp}]  {tx.sender} → {tx.receiver}  |  {tx.amount} coins"
                    )
            else:
                print("  Transaction History: (Genesis — no transactions)")
            print()


    def get_balance(self, address: str) -> float:
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.receiver == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= tx.amount
        return balance




if __name__ == "__main__":
    print("\n🔗 Initializing Blockchain...\n")
    bc = Blockchain()


    print("\n📦 Preparing Block 1 transactions:")
    bc.add_transaction("Alice", "Bob", 50)
    bc.add_transaction("Bob", "Charlie", 20)
    bc.mine_block()


    print("\n📦 Preparing Block 2 transactions:")
    bc.add_transaction("Charlie", "Alice", 10)
    bc.add_transaction("Alice", "David", 30)
    bc.add_transaction("David", "Bob", 5)
    bc.mine_block()


    print("\n📦 Preparing Block 3 transactions:")
    bc.add_transaction("Bob", "Alice", 15)
    bc.mine_block()


    bc.print_chain()


    print("=" * 60)
    valid = bc.is_valid()
    print(f"  Chain Integrity : {'✅ Valid' if valid else '❌ Tampered!'}")
    print("=" * 60)


    print("\n💰 Account Balances:")
    for name in ["Alice", "Bob", "Charlie", "David"]:
        print(f"  {name:10s}: {bc.get_balance(name):+.2f} coins")


    print("\n⚠️  Tampering with Block 1 data...")
    bc.chain[1].transactions[0].amount = 9999
    valid = bc.is_valid()
    print(f"  Chain Integrity : {'✅ Valid' if valid else '❌ Tampered — chain is broken!'}")
