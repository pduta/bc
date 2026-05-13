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




blockchain = []


nodes = [
    {"node": "Node 1", "transaction": "Alice pays Bob 10 BTC"},
    {"node": "Node 2", "transaction": "Bob pays Charlie 5 BTC"},
    {"node": "Node 3", "transaction": "Charlie pays David 3 BTC"},
    {"node": "Node 4", "transaction": "David pays Eve 2 BTC"},
    {"node": "Node 5", "transaction": "Eve pays Alice 1 BTC"},
]


genesis = Block(0, "Genesis Block", "0" * 64)
blockchain.append(genesis)


for i, node in enumerate(nodes):
    block = Block(i + 1, node, blockchain[-1].hash)
    blockchain.append(block)


print("=" * 65)
print("  BLOCKCHAIN - 5 NODES")
print("=" * 65)


for block in blockchain:
    print(f"\n  Block Index    : {block.index}")
    if isinstance(block.data, dict):
        print(f"  Node           : {block.data['node']}")
        print(f"  Transaction    : {block.data['transaction']}")
    else:
        print(f"  Data           : {block.data}")
    print(f"  Timestamp      : {block.timestamp}")
    print(f"  Previous Hash  : {block.previous_hash}")
    print(f"  Hash           : {block.hash}")
