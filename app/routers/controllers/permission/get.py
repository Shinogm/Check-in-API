from fastapi import HTTPException
from app.services.db import check_db
from app.models.user.user import UserTypeEnum

async def get_permissions():
        
        get_permissions = check_db.fetch_all(
            sql="SELECT * FROM users.perms"
        )
    
        if not get_permissions:
            raise HTTPException(status_code=404, detail="Permissions not found")
        
        return {
            "status": "success",
            "message": "Permissions found",
            "permissions": get_permissions
    }

async def get_permission_user(permission: UserTypeEnum):
    
    get_user = check_db.fetch_one(
        sql="SELECT * FROM users WHERE perms = %s",
        params=(permission.value,)
    )

    if not get_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "status": "success",
        "message": "User found",
        "user": get_user
    }