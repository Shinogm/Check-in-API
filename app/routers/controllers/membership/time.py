from fastapi import HTTPException
from app.services.db import check_db
from datetime import datetime

async def comparar_fechas_y_calcular_dias_restantes(fecha_expiracion: str):
    try:
        fecha_proporcionada = datetime.strptime(fecha_expiracion, "%Y-%m-%d")

        fecha_actual = datetime.now()
        
        dias_restantes = (fecha_proporcionada - fecha_actual).days
        print("Días restantes:", dias_restantes)
        
        
        if fecha_proporcionada > fecha_actual:
            return {
                "message": f"Tu membresía expira el {fecha_proporcionada} y faltan {dias_restantes} días."
            }
        elif fecha_proporcionada < fecha_actual:
            dias_caducado = abs(dias_restantes)
            return {
                "message": f"Tu membresía expiró el {fecha_proporcionada} hace {dias_caducado} días."
            }
        
        else:
            return {
                "message": f"Tu membresía expira hoy {fecha_proporcionada}."
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="error to compare dates and calculate remaining days")
    
    
async def check_all_membership_is_out():
    try:

        all_memberships = check_db.fetch_all(
            sql='SELECT * FROM membership'
        )
        if not all_memberships:
            raise HTTPException(status_code=404, detail='Memberships not found')
        
        for membership in all_memberships:
            print(membership['expiration_date'])
            response = await comparar_fechas_y_calcular_dias_restantes(str(membership['expiration_date']))
            client_db = check_db.fetch_one(
                sql='SELECT * FROM users WHERE id = %s',
                params=(membership['user_id'],)
            )
            
        return {
                "message": "All memberships",
                "memberships": client_db,
                "response": response
            }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="error to check all memberships")
    

from app.routers.controllers.client.identify import indentity

async def membership_is_out_finger():
    try:
        res = await indentity()

        membership = check_db.fetch_all(
            sql='SELECT * FROM membership WHERE id = %s',
            params=(res['id'],)
        )
        
        if not membership:
            raise HTTPException(status_code=404, detail='Memberships not found')
        
        print(membership['expiration_date'])
        response = await comparar_fechas_y_calcular_dias_restantes(str(membership['expiration_date']))
        client_db = check_db.fetch_one(
                sql='SELECT * FROM users WHERE id = %s',
                params=(res['id'],)
            )
            
        return {
                "message": "verified membership by codeS",
                "memberships": client_db,
                "response": response
            }
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="error to checkmemberships")
