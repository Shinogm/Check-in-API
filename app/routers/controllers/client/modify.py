from fastapi import HTTPException, Depends
from app.services.db import check_db
from app.models.user.user import UserTypeEnum, ModifyUser

async def modify_client(client_id: int, user: ModifyUser = Depends()):

    get_user = check_db.fetch_one(
        sql='SELECT * FROM users WHERE id = %s',
        params=(client_id,)
    )

    if get_user['perms'] != UserTypeEnum.CLIENT.value:
        raise HTTPException(status_code=403, detail='You are not authorized to perform this action')

    if not get_user:
        raise HTTPException(status_code=404, detail='User not found')
    
    update_user = check_db.execute(
            sql=
            '''
            UPDATE users
            SET first_name = %s, last_name = %s, email = %s
            WHERE id = %s
            ''',
            params=(
                user.first_name if user.first_name is not None else get_user['first_name'],
                user.last_name if user.last_name is not None else get_user['last_name'],
                user.email if user.email is not None else get_user['email'],
            )
        )
    
    return {
        'status': 'success',
        'message': 'User updated successfully',
        'old_data': get_user,
        'new_data': {
            'first_name': user.first_name if user.first_name is not None else '',
            'lastname': user.last_name if user.last_name is not None else '',
            'email': user.email if user.email is not None else '',
        }
    }