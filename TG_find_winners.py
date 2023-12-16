# def winner(update, context):
#     # а вот это долно отправить победителя в указанную дату, скорее всего придется
#     # удалить и делать через send_message
#     update.message.reply_text(
#         Message.objects.get(name='Победитель').text
#     )