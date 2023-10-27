from passlib.context import CryptContext
    
    
context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

    
    
def verifyPassword(plainText, hashed_password):
    return context.verify(plainText, hashed_password)

    
    
    
    
    
    
    
    
   














