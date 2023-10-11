from datetime import datetime

from models import User, Group_reg


def get_user_by_id(user_id):
    try:
        return User.get(vk_id=user_id)
    except:
        User(
            vk_id=user_id,
            warns=0
        ).save()
        return User.get(vk_id=user_id)


def get_group_by_id(group_id):
    try:
        return Group_reg.get(beseda_id=group_id)
    except:
        Group_reg(
            created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            beseda_id=group_id,
            #date_rename_name_besedi="saturday",
            time_rename_name_besedi="18:00"
        ).save()
        return Group_reg.get(beseda_id=group_id)

def get_group_by_id_all():
    return Group_reg.select().execute()
