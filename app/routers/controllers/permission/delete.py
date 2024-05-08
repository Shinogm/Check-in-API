from fastapi import HTTPException
from app.services.db import check_db
from app.models.user.user import UserTypeEnum

async def delete_users(enum: UserTypeEnum):
    
    get_users = check_db.fetch_all(
        sql="SELECT * FROM users WHERE perms = %s", params=(enum.value,)
    )

    if not get_users:
        raise HTTPException(status_code=404, detail="No users found")
    
    for user in get_users:
        check_db.execute(
            sql="DELETE FROM users WHERE id = %s", params=(user['id'],)
        )

    return {
        "message": "Users deleted successfully",
        'users': get_users,
    }