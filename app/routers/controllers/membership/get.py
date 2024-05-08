from fastapi import HTTPException
from app.services.db import check_db
from app.models.client.membership import MembershipTypeEnum

async def get_members(member: MembershipTypeEnum):
    
    get_members = check_db.fetch_all(
        sql="SELECT * FROM membership WHERE membership_type = %s",
        params=(member.value,)
    )

    if not get_members:
        raise HTTPException(status_code=404, detail="Members not found")
    
    for members in get_members:
        get_user = check_db.fetch_one(
            sql="SELECT * FROM users WHERE id = %s",
            params=(members["user_id"],)
        )
    
    if member == MembershipTypeEnum.NOT_MEMBER:
        return {
            "status": "success",
            "message": "Non-members found",
            "members": get_user
        }
    
    return {
        "status": "success",
        "message": "Members found",
        "members": get_user
    }