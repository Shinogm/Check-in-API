from fastapi import HTTPException
from app.services.db import check_db

async def delete_user(user_id: int):
    user = check_db.fetch_one(
        sql="SELECT * FROM users WHERE id = %s",
        params=(user_id,)
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    delete_user = check_db.execute(
        sql="DELETE FROM users WHERE id = %s",
        params=(user_id,)
    )


    
    return {
        "status": "success",
        "message": "User deleted",
        "user": user,
        "delete_user": delete_user
    }