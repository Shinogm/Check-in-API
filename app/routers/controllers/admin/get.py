from fastapi import HTTPException
from app.services.db import check_db

async def get_all_users():

    users = check_db.fetch_all(
        sql="SELECT * FROM users"
    )

    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    
    return {
        "status": "success",
        "users": users
    }

async def get_user_id(user_id: int):
    
        user = check_db.fetch_one(
            sql="SELECT * FROM users WHERE id = %s",
            params=(user_id,)
        )
    
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "status": "success",
            "user": user
        }