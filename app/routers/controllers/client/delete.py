from fastapi import HTTPException
from app.services.db import check_db
from app.models.user.user import UserTypeEnum

async def delete_client(client_id: int):

    client_enum = UserTypeEnum.CLIENT.value

    get_client = check_db.fetch_one(
        sql='SELECT * FROM users WHERE id = %s',
        params=(client_id,)
    )

    if not get_client:
        raise HTTPException(status_code=404, detail='Client not found')
    
    if get_client['perms'] != client_enum:
        raise HTTPException(status_code=400, detail='The user is not a client')
    
    delete_client = check_db.execute(
        sql='DELETE FROM users WHERE id = %s',
        params=(client_id,)
    )

    return {
        "status": "success",
        "message": "Client deleted",
        "old_client": get_client
    }
