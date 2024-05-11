from fastapi import HTTPException
from app.services.db import check_db
from app.models.client.membership import MembershipTypeEnum
async def get_members(member: MembershipTypeEnum):

    print(member.value)

    get_members_query = check_db.fetch_all(
        sql="SELECT * FROM memberships WHERE have_membership = %s",
        params=(member.value,)
    )

    if not get_members_query and member.value == "no":
        user_not_member_query = check_db.fetch_all(
            sql='''
            SELECT 
                u.id AS user_id,
                u.first_name,
                u.last_name,
                u.email
            FROM 
                users u
            LEFT JOIN 
                memberships m ON u.id = m.user_id
            WHERE 
                m.user_id IS NULL;
            '''
        )
        if not user_not_member_query:
            raise HTTPException(
                status_code=404,
                detail="No members found"
            )
        
        return {
            "status": "success",
            "message": "Members found",
            "members": user_not_member_query
        }

    all_members = []

    for member_row in get_members_query:
        get_user_with_membership_query = check_db.fetch_all(
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
                memberships m ON u.id = m.user_id
            WHERE
                u.id = %s;
            ''',
            params=(member_row['user_id'],)
        )
        all_members.extend(get_user_with_membership_query)

    return {
        "status": "success",
        "message": "Members found",
        "members": all_members
    }
