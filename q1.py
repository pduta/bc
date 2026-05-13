import hashlib

message = "Blockchain Developer"
digest = hashlib.sha256(message.encode()).hexdigest()
print(digest)
