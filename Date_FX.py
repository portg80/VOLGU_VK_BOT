from datetime import datetime, timedelta
import re



#def find_nearest_weekday(date_str, weekday):
#    # Разбираем строку с датой и временем
#    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
#
#    # Получаем день недели
#    current_weekday = date.weekday()
#
#    # Вычисляем разницу между текущим днем недели и целевым днем недели
#    difference = weekday - current_weekday
#
#    # Если разница отрицательная или равна нулю, добавляем 7 дней
#    if difference <= 0:
#        difference += 7
#
#    # Прибавляем разницу к текущей дате
#    nearest_date = date + timedelta(days=difference)
#
#    if datetime.now().strftime("%Y-%m-%d") == datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime(
#            "%Y-%m-%d") and datetime.now().time() < datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").time():
#        nearest_date = datetime.now().replace(hour=date.hour, minute=date.minute, second=date.second)
#    else:
#        nearest_date = nearest_date
#
#    return nearest_date


#date_str = "2023-10-11 11:27:00"
#
## Примеры вызова функции для каждого дня недели
#nearest_monday = find_nearest_weekday(date_str, 0)
#nearest_tuesday = find_nearest_weekday(date_str, 1)
#nearest_wednesday = find_nearest_weekday(date_str, 2)
#nearest_thursday = find_nearest_weekday(date_str, 3)
#nearest_friday = find_nearest_weekday(date_str, 4)
#nearest_saturday = find_nearest_weekday(date_str, 5)
#nearest_sunday = find_nearest_weekday(date_str, 6)
#
#print("Ближайший прошедший понедельник:", nearest_monday)
#print("Ближайший прошедший вторник:", nearest_tuesday)
#print("Ближайшая прошедшая среда:", nearest_wednesday)
#print("Ближайший прошедший четверг:", nearest_thursday)
#print("Ближайший прошедший пятница:", nearest_friday)
#print("Ближайшая прошедшая суббота:", nearest_saturday)
#print("Ближайшее прошедшее воскресенье:", nearest_sunday)
#

#def run_scheduler():
#    while True:
#        print("ПОТОК 1 ЗАПУЩЕН")
#        print("Планировщик начало")
#        fwd_Beseda = utils.get_group_by_id(msg['peer_id'])
#
#        # Function to retrieve the last stored start date
#        def get_last_start_date():
#            last_start_date = fwd_Beseda.date_rename_name_besedi
#            if last_start_date is not None:
#                return datetime.datetime.strptime(last_start_date, "%Y-%m-%d %H:%M:%S")
#            else:
#                return None
#
#        # Function to save the current start date
#        def save_start_date(date):
#            fwd_Beseda.date_start_renaming = date.strftime("%Y-%m-%d %H:%M:%S")
#            fwd_Beseda.save()
#
#        # Get the current date and time
#        current_date = datetime.datetime.now()
#
#        # Get the last stored start date
#        last_start_date = get_last_start_date()
#
#        # Calculate the next Wednesday date and time
#        next_wednesday = current_date + datetime.timedelta(days=(2 - current_date.weekday() + 7) % 7)
#        next_wednesday = next_wednesday.replace(hour=12, minute=40, second=0, microsecond=0)
#
#        # Check if the current date is less than the next Wednesday date and time
#        if current_date < next_wednesday:
#            time.sleep((next_wednesday - current_date).total_seconds())
#            continue
#
#        # Calculate the number of Wednesdays that have passed since the last start date
#        num_missed_wednesdays = 0
#        if last_start_date is not None:
#            num_missed_wednesdays = (current_date - last_start_date).days // 7
#
#        # Check if the current day is Wednesday and the time is after 11:00
#        if current_date.weekday() == 2 and (current_date.hour == 12 and current_date.minute >= 32):
#            num_missed_wednesdays += 1
#
#        # Run the function if the number of missed Wednesdays is even
#        if num_missed_wednesdays % 2 == 0:
#            editchatname_thread = threading.Thread(target=VkBot().editchatname,
#                                                   args=(event, msg['peer_id'], "хуита", 1))
#            editchatname_thread.start()
#        else:
#            editchatname_thread = threading.Thread(target=VkBot().editchatname,
#                                                   args=(event, msg['peer_id'], "хуита", 1))
#            editchatname_thread.start()
#            print("Odd number of days were missed")
#
#        # Save the current start date
#        save_start_date(current_date)
#
#        print("Планировщик конец")
#        time.sleep(10)