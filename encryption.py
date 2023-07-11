from cryptography.fernet import Fernet
import bcrypt  
import base64
import json

""" decrypting will save, using password as the encryption key, the encrypted 
    version of d if the input d isn't None, other wise it will encrypt the 
    dictionary found in source_file"""
def encrypting(password, d= None, source_file = "passwords.json", save_file="encrypted_passwords.txt", salt = b'$2b$12$jhAosZcGLWvaIAHW2pn4a.'):
  if source_file=="" and d==None:
    raise TypeError("Either source_file or d should not be empty")
  
  hashed_password = bcrypt.hashpw(password.encode(), salt)

  key = base64.urlsafe_b64encode(hashed_password[:32])

  cipher = Fernet(key)

  # Reading the input
  if d==None:
    with open(source_file) as f:
      d = json.load(f)

  text = bytes(json.dumps((d)), 'utf-8')

  # Encrypting and storing the passwords
  encrypted_passwords = cipher.encrypt(text)
  with open(save_file, "w") as f:
    f.write(encrypted_passwords.decode('utf-8'))


""" If the password is correct, the json file is decrypted and a dictionary is 
    returned. If the password is incorrect, the function returns 1
"""
def decrypting(password, salt = b'$2b$12$jhAosZcGLWvaIAHW2pn4a.'):
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