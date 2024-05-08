from fastapi import APIRouter
from app.routers.controllers.permission import get, delete

router = APIRouter(prefix='/perms', tags=['permission'])

router.get('/get-permissions')(get.get_permissions)

router.get('/get-permission/{permission}')(get.get_permission_user)

router.delete('/delete-permission')(delete.delete_users)
