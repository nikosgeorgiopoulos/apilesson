from datetime import datetime , timedelta
from fastapi import Depends , status, HTTPException
from jose import JWTError , jwt
from fastapi.security import OAuth2PasswordBearer
from . import schemas , database , models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')




#secret key
#Algorithm
#expiration time


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expiration_minutes

def create_access_token(data: dict):
    
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm= ALGORITHM)

    return encoded_jwt



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_excpetion = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})


    token = verify_access_token(token, credentials_excpetion)

    user = db.query(models.User).filter(models.User.id == token).first()

    return  user 




def verify_access_token(token: str, credentials_exception):
    
    try:

        payload = jwt.decode(token, SECRET_KEY , algorithms= ALGORITHM)
        id: str = payload.get("user_id")

        if id is  None:    
            raise credentials_exception
        
        token_data: str = id

    except JWTError:
        raise credentials_exception
    

    return token_data # this is the id in the current case because the schema has no other data in it
    


