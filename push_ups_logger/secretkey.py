import secrets

def generate_secret_key(length=64):
    return secrets.token_hex(length)

# Generate a default secret key
default_secret_key = generate_secret_key()
print(default_secret_key)
