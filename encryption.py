from cryptography.fernet import Fernet
import bcrypt  
import base64
import json

salt = b'$2b$12$jhAosZcGLWvaIAHW2pn4a.'

def encrypting(password, salt):
  hashed_password = bcrypt.hashpw(password.encode(), salt)

  key = base64.urlsafe_b64encode(hashed_password[:32])

  cipher = Fernet(key)

  # Reading the passwords
  with open("passwords.json") as f:
    text = json.dumps(json.load(f))
  text = bytes(text, 'utf-8')

  # Encrypting and storing the passwords
  encrypted_passwords = cipher.encrypt(text)
  with open("encrypted_passwords.txt", "w") as f:
    f.write(encrypted_passwords.decode('utf-8'))


def decrypting(password, salt):
  try:
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    key = base64.urlsafe_b64encode(hashed_password[:32])

    cipher = Fernet(key)

    with open("encrypted_passwords.txt") as f:
      text = bytes(f.read(), 'utf-8')

    decrypted_passwords = cipher.decrypt(text)
    return json.loads(decrypted_passwords)
  except:
    return -1