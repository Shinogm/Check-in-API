from fastapi import HTTPException
from app.services.db import check_db
from app.models.client.membership import MembershipTypeEnum

async def get_members(member: MembershipTypeEnum):
    
    get_members = check_db.fetch_all(
        sql="SELECT * FROM memberships WHERE have_membership = %s",
        params=(member.value,)
    )

    if not get_members:
        raise HTTPException(status_code=404, detail="Members not found")
    
    for members in get_members:
        get_user_with_membership = check_db.fetch_one(
            sql='''
            SELECT 
                u.id AS user_id,
                u.first_name,
                u.last_name,
                u.email,
                m.id AS membership_id,
                m.created_at AS membership_created_at,
                m.expiration_date,
                m.have_membership
            FROM 
                users u
            JOIN 
                memberships m ON u.id = %s;
            ''',
            params=(members['user_id'],)
        )
    
    if member == MembershipTypeEnum.NOT_MEMBER:
        return {
            "status": "success",
            "message": "Non-members found",
            "members": get_user_with_membership
        }
    
    return {
        "status": "success",
        "message": "Members found",
        "members": get_user_with_membership
    }