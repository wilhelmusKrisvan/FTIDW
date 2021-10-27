from werkzeug.security import generate_password_hash

hashed = generate_password_hash('wilhelmus',method='sha256')

print(hashed)