from fastapi import HTTPException
from app.services.db import check_db
from app.models.client.membership import MembershipTypeEnum
from app.models.user.user import UserTypeEnum

async def cancel_membership(user_id: int):
    
    get_user = check_db.fetch_one(
        sql="SELECT * FROM users WHERE id = %s",
        params=(user_id,)
    )

    if not get_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if get_user["perms"] != UserTypeEnum.CLIENT.value:
        raise HTTPException(status_code=400, detail="User is not a client")
    
    get_membership = check_db.fetch_all(
        sql="SELECT * FROM memberships WHERE user_id = %s",
        params=(user_id,)
    )

    if not get_membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    if get_user["perms"] == MembershipTypeEnum.NOT_MEMBER.value:
        raise HTTPException(status_code=400, detail="User is not a member")
    
    check_db.execute(
        sql='DELETE FROM memberships WHERE user_id = %s',
        params=(user_id,)
    )

    return {
        "status": "success",
        "message": "Membership cancelled",
        "user": get_user
    }

async def cancel_membership_where_code(code: int):
        
        get_user = check_db.fetch_one(
            sql="SELECT * FROM memberships WHERE id = %s",
            params=(code,)
        )

        if not get_user:
            raise HTTPException(status_code=404, detail="Membership not found")
        
        check_db.execute(
            sql='DELETE FROM memberships WHERE id = %s',
            params=(code,)
        )

        return {
            "status": "success",
            "message": "Membership cancelled",
            "user": get_user
        }
    