from fastapi import APIRouter
from app.routers.controllers.admin import create, get, modify, delete
from app.utils import login

router = APIRouter(prefix='/admin', tags=['admin'])


router.post('/user/create')(create.create_user)
router.post('/login')(login.verify_password)
router.post('/user/update/{user_id}')(modify.modify_user)

router.get('/users/get-all-users')(get.get_all_users)
router.get('/user/get-user/{user_id}')(get.get_user_id)

router.delete('/user/delete/{user_id}')(delete.delete_user)
