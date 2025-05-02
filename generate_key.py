from cryptography.fernet import Fernet

key = Fernet.generate_key()

# Save the key to a file
with open("shared-key.key", "wb") as key_file:
    key_file.write(key)

print("Shared key generated and saved to shared-key.key")
