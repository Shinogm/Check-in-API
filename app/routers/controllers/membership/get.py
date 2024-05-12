from fastapi import HTTPException
from app.services.db import check_db
from app.models.client.membership import MembershipTypeEnum

async def get_members():

    all_memberships = check_db.fetch_all(
        sql='SELECT * FROM memberships'
    )
    if not all_memberships:
        raise HTTPException(status_code=404, detail='Memberships not found')

    all_clients_info = []
    all_clients_info.clear()
    for membership in all_memberships:
        user_id = membership['user_id']
        # Obtener la información del usuario directamente en una sola consulta SQL
        all_clients = check_db.fetch_all(
            sql='SELECT * FROM users WHERE id = %s',
            params=(user_id,)
        )

        # Agregar información del cliente a la lista
        all_clients_info.append({
            "membership": membership,
            "client_info": all_clients
        })

    length = len(all_clients_info)


    return {
        "message": "verified all memberships",
        "length": length,
        "memberships": all_clients_info
    }

async def get_clients_no_membership():
    all_clients = check_db.fetch_all(
        sql="""
                SELECT u.*
                    FROM users u
                    LEFT JOIN memberships m ON u.id = m.user_id
                    WHERE m.user_id IS NULL
                    AND u.perms = 'client';

            """
    )
    if not all_clients:
        raise HTTPException(status_code=404, detail='Clients not found')

    return {
        "message": "clients without membership",
        "length": len(all_clients),
        "clients": all_clients
    }


