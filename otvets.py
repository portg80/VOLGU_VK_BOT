help_otvet = (
    "\n'!пред' \\ '!репорт' \\ '!report' - команда отправки жалобы на пересланное сообщение или упоминание (в разраб) пользователя, может применятся со знаком '=' после которого следует число, которое принудительно изменит число варнов пользователя\nНапример: '!Пред=3' установит кол-во варнов пользователя на 3 "
    "\n\n'!бан' \\ '!кик' - в ответ на сообщение исключит пользователя из беседы"
    "\n\n'zxc' - запускает функцию переименования"
    "\n"
    "\n"
    "\n"
    "\n"
    "\n"
    "\n")
varnCmd_1 = r"!пред(=\d+)?"
varnCmd_2 = r"!репорт(=\d+)?"
varnCmd_3 = r"!report(=\d+)?"

kikUserCmd = '!кик'
banUserCmd = '!бан'
helpCmd ="!help"

startNamingProccesCmdRu = 'ячс'
startNamingProccesCmdEng = 'zxc'