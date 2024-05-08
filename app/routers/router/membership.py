from fastapi import APIRouter
from app.routers.controllers.membership import create, get, time, delete

router = APIRouter(prefix='/membership', tags=['membership'])

router.post('/create')(create.have_membership)

router.get('/get-members/{member}')(get.get_members)

router.get('/check-all-membership')(time.check_all_membership_is_out)
router.get('/finger/check-membership')(time.membership_is_out_finger)

router.delete('/cancel/{user_id}')(delete.cancel_membership)