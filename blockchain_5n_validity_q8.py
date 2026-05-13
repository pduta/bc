import hashlib
import json
from datetime import datetime




class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()


    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()




class Blockchain:
    def __init__(self):
        self.chain = []
        genesis = Block(0, "Genesis Block", "0" * 64)
        self.chain.append(genesis)


    def add_block(self, data):
        block = Block(len(self.chain), data, self.chain[-1].hash)
        self.chain.append(block)


    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]


            if current.hash != current.compute_hash():
                return False, f"Block {i} hash is corrupted."


            if current.previous_hash != previous.hash:
                return False, f"Block {i} is not linked to Block {i - 1}."


        return True, "Blockchain is valid."


    def print_chain(self):
        print("=" * 65)
        print("  BLOCKCHAIN - 5 NODES")
        print("=" * 65)
        for block in self.chain:
            print(f"\n  Block Index    : {block.index}")
            print(f"  Data           : {block.data}")
            print(f"  Timestamp      : {block.timestamp}")
            print(f"  Previous Hash  : {block.previous_hash}")
            print(f"  Hash           : {block.hash}")
            print("-" * 65)




bc = Blockchain()


nodes = [
    "Alice pays Bob 10 BTC",
    "Bob pays Charlie 5 BTC",
    "Charlie pays David 3 BTC",
    "David pays Eve 2 BTC",
    "Eve pays Alice 1 BTC",
]


for node in nodes:
    bc.add_block(node)


bc.print_chain()


print("\n  VALIDITY CHECK")
print("=" * 65)
valid, message = bc.is_valid()
print(f"  Status : {'✅ VALID' if valid else '❌ INVALID'}")
print(f"  Detail : {message}")
print("=" * 65)


print("\n  TAMPERING BLOCK 2...")
bc.chain[2].data = "Bob pays Charlie 9999 BTC"
print("  Block 2 data changed.\n")


print("  VALIDITY CHECK AFTER TAMPERING")
print("=" * 65)
valid, message = bc.is_valid()
print(f"  Status : {'✅ VALID' if valid else '❌ INVALID'}")
print(f"  Detail : {message}")
