@dp.message_handler()
async def memory1(message):
    my_chat = message.chat.id
    que_text_hear = QueText.objects.get(que=quest)
    await bot.send_message(chat_id=my_chat, text=que_text_hear, reply_markup=marking(quest))
    await AnswerForm.ans.set()


@dp.message_handler(state=AnswerForm.ans)
async def memory2(message, state: FSMContext):
    user_username = message.from_user.username
    now_client = Client.objects.filter(acc_tg=user_username).first()
    answer_data = await state.get_data()
    ans = answer_data.get("ans")

    # Сохраняем данные в Django-модель
    Answer.objects.create(client=now_client, que=quest,
                          ans=ans, date=datetime.now())
    await state.finish()


def marking(que):
    menu_marking = ReplyKeyboardMarkup(resize_keyboard=True)
    if que.typy_q == 'yes_or_no':
        menu_marking.add('Да').add('Нет')
    elif que.typy_q == 'one_of_some':
        counting = que.count_marks + 1
        for i in range(counting):
            # menu_marking.add(QueText.objects.filter(que=que))
            print(QueText.objects.filter(que=que))
    else:
        menu_marking.add(QueText.objects.filter(que=que))
        print(QueText.objects.filter(que=que))
    return menu_marking
