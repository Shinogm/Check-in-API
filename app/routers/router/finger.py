from fastapi import APIRouter
from app.routers.controllers.finger import create, scan, get

router = APIRouter(prefix='/finger', tags=['fingers'])

router.post('/create/{user_id}')(create.create_client_finger)
router.post('/scan')(scan.scan_finger)
router.get('/get-all-fingers')(get.get_finger_image)
