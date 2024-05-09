from fastapi import HTTPException
from app.services.db import check_db

async def get_finger_image(user_id: int):
    finger_image = check_db.fetch_one(
        sql='''
            SELECT
                id, created_at,  user_id fingerprint
            FROM fingerprints
            WHERE user_id = %s
            ''',
        params=(user_id,)
    )

    if not finger_image:
        raise HTTPException(status_code=404, detail='Finger image not found')
    
    return {
        'status': 'success',
        'finger_image': finger_image,
    }