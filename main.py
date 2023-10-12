import vk_api
import utils
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import re
import time
import threading
from threading import *
import otvets


access_token = "vk1.a.K0JCI9N8utAHXJ85DWhl8YLfjZ1jzTzTz8fJSQk5oyXaeU-WHZutV9iVJVObi1NgPpDDgeOWkIaW6_xBSIzgqZEio3QY1aAUApPYl3gweuo-Vv3STHCLiweMMShHu4cxdmpwWJ7yqSwVyWQ2kbqNYN0lISHoNEFchEC92lNhFnzwAVZeGn6Ti5rM_kvnd-VpZ8F2mxm-xWy4CvtzuZIO6A"
groupID = 222880805
admin_id = 363469220

Day_Nedeli_Count: int = 0

NameGroupStr = "ИВТб–221"
Chat_ChangeName_Id = -1
Current_NameBes = "Пирамида жопы"


class MyLoongPooll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print(e)


class VkBot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=access_token)
        self.longpooll = MyLoongPooll(self.vk_session, groupID)

    def sendMessage(self, event, text):
        msg = event.object.message
        self.vk_session.method('messages.send', {
            'chat_id': msg['peer_id'] - 2000000000,
            'message': text,
            'random_id': 0
        })

    def kikBanPred(self, event):
        msg = event.object.message

        user_id = msg['from_id']

        user = utils.get_user_by_id(user_id)
        text = msg['text']

        try:
            fwd = self.vk_session.method('messages.getByConversationMessageId', {
                'conversation_message_ids': msg['conversation_message_id'],
                'peer_id': msg['peer_id']
            })['items'][0]
        except Exception as ex:
            if "list index out of range" in str(ex):
                VkBot().sendMessage(event,
                                    "Произошла какая то непонятная херня рядом с индексами в методе:  \nfwd = self.vk_session.method('messages.getByConversationMessageId'\n проверьте консоль")
            else:
                VkBot().sendMessage(event,
                                    "Произошла какая то непонятная херня рядом с индексами в методе:  \nfwd = self.vk_session.method('messages.getByConversationMessageId'\n, но не \"list index out of range\"")
            print(ex,
                  "ERROR !2 Произошла какая то непонятная херня с индексом в \\fwd = self.vk_session.method('messages.getByConversationMessageId'\\")
            return -11

        conversation_info = self.vk_session.method("messages.getConversationMembers",{
            'peer_id': msg['peer_id'] - 2000000000})

        # Проверка прав отправителя сообщения
        for member in conversation_info['profiles']:
            if member['id'] == msg['from_id']:
                if member['is_admin']:
                    if user.vk_id == admin_id:
                        try:
                            if text.lower() == otvets.kikUserCmd or text.lower() == otvets.banUserCmd:

                                if 'reply_message' in fwd:
                                    fwd = fwd['reply_message']
                                else:
                                    fwd = None
                                    VkBot().sendMessage(event,
                                                        "Неправильное использование команды. Человек для призыва не найден 👀")
                                    return -11

                                if fwd['from_id'] != admin_id:
                                    self.vk_session.method('messages.removeChatUser', {
                                        'user_id': fwd['from_id'],
                                        'chat_id': msg['peer_id'] - 2000000000
                                    })
                                else:
                                    VkBot().sendMessage(event, "Это админ, его нельзя в бан, ибо он бессмертный..")
                                    return -11

                            ### r"!пред(=\d+)?"
                            ### r"!репорт(=\d+)?"
                            ### r"!report(=\d+)?"
                            elif re.match(otvets.varnCmd_1, text.lower()) or re.match(otvets.varnCmd_2, text.lower()) or re.match(
                                    otvets.varnCmd_3, text.lower()):
                                if 'reply_message' in fwd:
                                    fwd = fwd['reply_message']
                                else:
                                    fwd = None
                                    VkBot().sendMessage(event,
                                                        "Неправильное использование команды. Человек для призыва не найден 👀")
                                    return -11

                                if not re.search(r"=\d+", text.lower()):
                                    if fwd['from_id'] != admin_id:

                                        fwd_user = utils.get_user_by_id(fwd['from_id'])
                                        fwd_user.warns += 1
                                        fwd_user.save()
                                        user_name = self.vk_session.method('users.get', {'user_id': fwd_user.vk_id})[0][
                                            'first_name']
                                        print(user_name)
                                        self.vk_session.method('messages.send', {
                                            'chat_id': msg['peer_id'] - 2000000000,
                                            'message': f'{user_name}, ты, шавка, ловишь повестку!\nВсего повесток: {fwd_user.warns}/5 🥳',
                                            'random_id': 0
                                        })

                                        if fwd_user.warns >= 5:
                                            self.vk_session.method('messages.removeChatUser', {
                                                'user_id': fwd_user.vk_id,
                                                'chat_id': msg['peer_id'] - 2000000000
                                            })

                                    else:
                                        VkBot().sendMessage(event, "Это админ, его нельзя в бан, ибо он бессмертный..")
                                        return -11
                                else:
                                    fwd_user = None
                                    fwd_user = utils.get_user_by_id(fwd['from_id'])
                                    try:
                                        split_text = text.split("=")
                                        number = int(split_text[1])
                                    except (IndexError, ValueError):
                                        number = 0

                                    if number >= 1:
                                        fwd_user.warns = number
                                        print("Число после '=':", number)
                                        fwd_user.save()
                                    else:
                                        fwd_user.warns = 0
                                        print("Число после '=':", number)
                                        VkBot().sendMessage(event, "значение репортов обнулено")
                                        fwd_user.save()
                                        return -11

                                    user_name = self.vk_session.method('users.get', {'user_id': fwd_user.vk_id})[0]['first_name']
                                    print(user_name)
                                    self.vk_session.method('messages.send', {
                                        'chat_id': msg['peer_id'] - 2000000000,
                                        'message': f'{user_name}, Военком тут немного подумал..!\nВсего повесток: {fwd_user.warns}/5 🥳',
                                        'random_id': 0
                                    })
                                    if fwd_user.warns >= 5:
                                        self.vk_session.method('messages.removeChatUser', {
                                            'user_id': fwd['from_id'],
                                            'chat_id': msg['peer_id'] - 2000000000
                                        })
                        except Exception as ex:
                            if "935" in str(ex):
                                VkBot().sendMessage(event, "пользователя нет в группе")
                            else:
                                VkBot().sendMessage(event, "Робот? Человек? Птеродактиль?")
                            print(ex, "ERROR !1 Попытка использовать функции репорта не на человека")
                            return -11

    def CHECK_MESSAGE(self):
        print("фоновая проверка сообщений активирована")
        for event in self.longpooll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_chat:
                    msg = event.object.message
                    text = msg['text']

                    if otvets.helpCmd in text.lower():
                        VkBot().sendMessage(event, otvets.help_otvet)

                    VkBot().kikBanPred(event)
                    time.sleep(1)

    def CHECK_DAY(self):
        global Chat_ChangeName_Id
        print("фоновая проверка ДНЯ активирована")

        ###chat_ids = []  # Создаем список для хранения идентификаторов бесед
        ##
        def run_scheduler():

            print("ПОТОК 1 ЗАПУЩЕН")
            print("Планировщик начало")
            fwd_Beseda = utils.get_group_by_id(msg['peer_id'])
            editchatname_thread = threading.Thread(target=VkBot().editchatname,
                                                   args=(event, msg['peer_id'], "хуита", 1))
            # Создаем экземпляр планировщика
            scheduler = BlockingScheduler()
            # Задаем расписание выполнения функции
            trigger = CronTrigger(day_of_week='sun', hour=18, minute=0)

            scheduler.add_job(editchatname_thread.start, trigger)
            # Запускаем планировщик
            # scheduler.start()
            scheduler_thread = threading.Thread(target=scheduler.start,
                                                args=(event, msg['peer_id'], "хуита", 1))
            print("Планировщик конец")
            time.sleep(10)

        for event in self.longpooll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.object.message
                user_id = msg['from_id']

                user = utils.get_user_by_id(user_id)
                text_CMD_Day = msg['text']
                fwd = self.vk_session.method('messages.getByConversationMessageId', {
                    'conversation_message_ids': msg['conversation_message_id'],
                    'peer_id': msg['peer_id']
                })['items'][0]

                if user.vk_id == admin_id:
                    if text_CMD_Day.lower() == "m" or text_CMD_Day.lower() == "ь":
                        VkBot.REG_GROUP(self, event, msg, msg['from_id'])

                if user.vk_id == admin_id:
                    if text_CMD_Day.lower() == "qwe" or text_CMD_Day.lower() == "йцу":
                        run_scheduler()

                if user.vk_id == admin_id:  # ЗАПУСКАЕМ ОТСЛЕЖИВАНИЕ
                    if text_CMD_Day.lower() == otvets.startNamingProccesCmdRu or text_CMD_Day.lower() == otvets.startNamingProccesCmdEng:
                        ###chat_ids.append(msg['peer_id'])  # Добавляем идентификатор беседы в список
                        ###VkBot().sendMessage(event, chat_ids)
                        ###time.sleep(1)
                        fwd_Beseda = utils.get_group_by_id(msg['peer_id'])

                        # date_str_now = fwd_Beseda.date_rename_name_besedi
                        # nearest_wednesday = Date_FX.find_nearest_weekday(date_str_now, 2)
                        # print("Наступающая СРЕДА: ", nearest_wednesday)

                        # fwd_Beseda.nearest_date_rename_name_besedi = nearest_wednesday
                        # fwd_Beseda.date_start_renaming = time.strftime("%Y-%m-%d %H:%M:%S")
                        editchatname_thread = threading.Thread(target=VkBot().editchatname,
                                                               args=(event, msg['peer_id'], "хуита", 1))
                        editchatname_thread.start()
                    # run_scheduler_thread = threading.Thread(target=run_scheduler)
                    # run_scheduler_thread.start()

    ###ПЕРЕДЕЛАТЬ ВСЁ НАХУЙ ПОД MSQL
    def REG_GROUP(self, event, msg, user_id):

        print("REG_GROUP запущена")
        chat = self.vk_session.method('messages.getConversationsById', {
            'peer_ids': msg['peer_id'],
            'access_token': access_token,
            'extended': 1,
            'fields': 'title',
            'v': '5.154'
        })  # print(chat)

        Current_NameBes = chat['items'][0]['chat_settings']['title']

        VkBot().sendMessage(event, "ВВЕДИТЕ НАЗАВНИЕ ВАШЕЙ ГРУППЫ:")

        group_name = "шщз"

        is_group_name_received = False
        while not is_group_name_received:
            for event in self.longpooll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    received_msg = event.object.message
                    print("popa")
                    if received_msg['from_id'] == user_id:
                        print("jojo")
                        group_name_inout = received_msg['text']
                        fwd_Beseda = utils.get_group_by_id(msg['peer_id'])
                        fwd_Beseda.group_name = group_name_inout
                        fwd_Beseda.beseda_name_PriReg = Current_NameBes
                        fwd_Beseda.save()
                        print("Срать подано: " + str(msg['peer_id']))

                        VkBot().sendMessage(event, "Записано в group_name: " + group_name_inout)
                        VkBot().sendMessage(event, "В БД теперь: " + fwd_Beseda.group_name)
                        is_group_name_received = True
                        break

            while not is_group_name_received:
                for event in self.longpooll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        received_msg = event.object.message
                        print("popa")
                        if received_msg['from_id'] == user_id:
                            print("jojo")
                            group_name_inout = received_msg['text']
                            fwd_Beseda = utils.get_group_by_id(msg['peer_id'])
                            fwd_Beseda.group_name = group_name_inout
                            fwd_Beseda.save()
                            print("Срать подано: " + str(msg['peer_id']))

                            VkBot().sendMessage(event, "Записано в group_name: " + group_name_inout)
                            VkBot().sendMessage(event, "В БД теперь: " + fwd_Beseda.group_name)
                            is_group_name_received = True
                            break

            time.sleep(1)

        print("END REG_GROUP")

    def editchatname(self, event, _ids, _mes, change_one_iter_start):

        global Current_NameBes
        msg = event.object.message

        if msg is None or 'text' not in msg:
            print("Ошибка: сообщение не содержит текст")
            time.sleep(1)
            return
        if msg['peer_id'] < 2000000000:
            print("Ошибка: сообщение не из беседы")
            time.sleep(1)
            return

        groups = utils.Group_reg.select()

        for group in groups:
            id_besedi = group.beseda_id
            chat = self.vk_session.method('messages.getConversationsById', {
                'peer_ids': id_besedi,
                'access_token': access_token,
                'extended': 1,
                'fields': 'title',
                'v': '5.154'
            })  # print(chat)

            Current_NameBes = chat['items'][0]['chat_settings']['title']
            print("Имя беседы:", Current_NameBes)

            # if _mes == ""
            _Current_NameBes = "Попал       (л)"
            _mes = re.sub(r'\s+', ' ', Current_NameBes.rstrip())  # удаление только лишних пробелов в конце строки

            if "(Знаменатель)" in Current_NameBes:
                _mes = _mes.replace("(Знаменатель)", "")
                _mes = str(str(_mes) + "(Числитель)")
                print("Числитель")
            elif ("(Числитель)" in Current_NameBes):
                _mes = _mes.replace("(Числитель)", "")
                _mes = str(str(_mes) + "(Знаменатель)")
                print("Знаменатель")
            else:
                _mes = str(str(_mes) + "(Знаменатель)")
                print("Знаменатель2")
            # api_url = 'https://api.vk.com/method/messages.editChat'
            # params = {
            #    'chat_id': _ids,
            #    'title': _mes,
            #    'access_token': access_token,
            #    'v': '5.154'
            # }
            # response = requests.post(api_url, params=params)
            while True:
                try:
                    # Проверка, что название беседы отличается от нового названия
                    if Current_NameBes != _mes:
                        # Изменение названия беседы
                        self.vk_session.method('messages.editChat', {
                            'chat_id': id_besedi - 2000000000,  # msg['peer_id'] - 2000000000,
                            'title': _mes
                        })
                        fwd_Beseda = utils.get_group_by_id(msg['peer_id'])
                        fwd_Beseda.date_last_change_Beseda_Name = time.strftime("%Y-%m-%d %H:%M:%S")
                        fwd_Beseda.save()
                        print("Название беседы успешно изменено")
                        time.sleep(5)
                        break  # Выходим из цикла while, если название беседы успешно изменено
                    else:
                        print("Название беседы уже совпадает с новым названием")
                        time.sleep(5)
                        break  # Выходим из цикла while, если название беседы уже совпадает
                except vk_api.exceptions.ApiError as e:
                    print("Ошибка при изменении названия беседы:", e)
                    if "9" in str(e):
                        VkBot().sendMessage(event, "КАПЧА МЕШАЕТ МНЕ ВЫБРАТЬСЯ...\nПОМОГИТЕЕ")
                        time.sleep(30)  # Пауза 30 секунд перед повторной попыткой


if __name__ == '__main__':
    print("БОТ ЗАПУЩЕН")
    t1 = Thread(target=VkBot().CHECK_MESSAGE)
    t1.start()
    t2 = Thread(target=VkBot().CHECK_DAY)
    t2.start()
    input()
    # from vkwave.bots import SimpleLongPollBot, SimpleBotEvent
    # from vkwave.bots.utils.uploaders import PhotoUploader
