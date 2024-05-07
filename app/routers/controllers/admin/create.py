from fastapi import HTTPException, Depends
from app.services.db import check_db
from app.models.user.user import User, UserTypeEnum
from app.routers.controllers.admin.get import get_user_id
import bcrypt

async def create_user(user: User = Depends(User.as_form)):

    user_db = check_db.fetch_one(
        sql="SELECT * FROM users WHERE email = %s",
        params=(user.email,)
    )
    if user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    create_user = check_db.execute(
        sql="INSERT INTO users (first_name, last_name, email, password, perms) VALUES (%s, %s, %s, %s, %s)",
        params=(user.first_name, user.last_name, user.email, bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()), UserTypeEnum.ADMIN.value)
    )

    if not create_user:
        raise HTTPException(status_code=500, detail="Error creating user")
    

    return {
        "status": "success",
        "message": f"User created the perm is {UserTypeEnum.ADMIN.value}",
        "user": user
    }



