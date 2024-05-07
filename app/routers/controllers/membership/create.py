from fastapi import HTTPException
from app.services.db import check_db
from datetime import datetime, timedelta
from app.models.user.user import UserTypeEnum
from app.models.client.membership import MembershipTypeEnum

async def have_membership(client_id: int, membership_month: int = 30):

        get_client = check_db.fetch_one(
            sql='SELECT * FROM users WHERE id = %s',
            params=(client_id,)
        )

        if not get_client:
            raise HTTPException(status_code=404, detail='Client not found')
        
        if get_client['perm'] != UserTypeEnum.CLIENT.value:
            raise HTTPException(status_code=400, detail='The user is not a client')
        
        client_membership = check_db.fetch_one(
            sql='SELECT * FROM memberships WHERE user_id = %s ',
            params=(client_id,)
        )
        
        if client_membership['have_membership'] == MembershipTypeEnum.NOT_MEMBER.value:

            expiration_date = datetime.now() + timedelta(days=membership_month)

            membership_enum = MembershipTypeEnum.IS_MEMBER.value

            put_membership = check_db.execute(
                sql='INSERT INTO membership (user_id, have_membership, expiration_date) VALUES (%s, %s, %s)',
                params=(client_id, membership_enum, expiration_date)
            )

            client_db = check_db.fetch_one(
                sql='SELECT * FROM users WHERE id = %s',
                params=(client_id,)
            )

            return {
                "message": "The client has a membership now",
                "client_db": client_db,
                "membership_id": f'Tiene membresia por {membership_month} dias',
                "expiration_date": expiration_date
            }
        
        get_client_db = check_db.fetch_one(
            sql='SELECT * FROM clients WHERE id = %s',
            params=(client_id,)
        )

        return {
                    "message": "The client already has a membership",
                    "client_id": client_id,
                    "client_db": get_client_db
        }




