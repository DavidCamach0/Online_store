from passlib.context import CryptContext


pwd_context = CryptContext(schemes= ["bcrypt"], deprecated ="auto")

def password_hash(password):

   return pwd_context.hash(password)


def verify_password(password,pass_hash):

   return pwd_context.verify(password,pass_hash)