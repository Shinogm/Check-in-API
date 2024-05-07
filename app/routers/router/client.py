from fastapi import APIRouter
from app.routers.controllers.client import create, get, modify, delete, identify

router = APIRouter(prefix='/client', tags=['client'])

router.post('/create')(create.create_user)
router.post('/identify')(identify.indentity)

router.get('/get-client/{client_id}')(get.get_one_client)
router.get('/get-all-clients')(get.get_all_clients)

