from peewee import *
import datetime as dt
from peewee import fn
import time

db = SqliteDatabase('data.db')


class User(Model):
    class Meta:
        database = db
        db_table = 'Users'

    vk_id = IntegerField()
    warns = IntegerField()


class Group_reg(Model):
    class Meta:
        database = db
        db_table = 'Groups_reg'

    group_name = CharField(null=True, max_length=25, help_text="ИМЯ ГРУППЫ УНИВЕРА (ИВТб-221)")
    created_date = DateTimeField(null=True)
    date_rename_name_besedi = CharField(null=True, help_text="ДАТА КОГДА НУЖНО ПЕРЕИМЕНОВЫВАТЬ БЕСЕДУ "
                                                                 "(например каждое воскресенье)")
    nearest_date_rename_name_besedi = CharField(null=True, help_text="ДАТА ближайшего переименования "
                                                             "(например каждое воскресенье)")
    date_start_renaming = DateTimeField(null=True,
                                        help_text="ДАТА ЗАПУСКА СИСТЕМУ смены имени беседы В КОНКРЕТНОЙ БЕСЕДЕ")
    userid_launched_renaming = IntegerField(null=True, help_text="ID пользователя, который зарегистрировал БЕСЕДУ и "
                                                                 "ГРУППУ В СИСТЕМЕ")
    beseda_id = IntegerField(null=True, help_text="ID беседы при регистрации беседы в системе смены имени беседы")
    beseda_name_PriReg = CharField(null=True, help_text="Имя БЕСЕДЫ при регистрации в системе смены имени беседы")
    beseda_last_name = CharField(null=True, help_text="Последнее установленное ИМЯ БЕСЕДЫ - СИСТЕМОЙ")
    date_last_change_Beseda_Name = DateTimeField(null=True, help_text="ДАТА последнего смены имени - СИСТЕМОЙ")


if __name__ == '__main__':
    db.create_tables([User, Group_reg])
