import hashlib


def generate_hash(input_string):
  encoded_string = input_string.encode('utf-8')
  sha256_hash = hashlib.sha256(encoded_string).hexdigest()
  return sha256_hash


def verify_hash(input_string, expected_hash):
  generated_hash = generate_hash(input_string)
  if generated_hash == expected_hash:
    return True
  else:
    return False


message = "Hello World"
hash = generate_hash(message)
result = verify_hash(message, hash)
if(result):
  print("Hash verified successfully.")
else:
  print("Hash verification failed.")
