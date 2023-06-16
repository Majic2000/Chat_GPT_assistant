import openai
from decouple import config
from django.shortcuts import render
from openai import ChatCompletion

from pathlib import Path


def process_chatbot_response(prompts, conversation):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompts,
        api_key=config('OPENAI_API_KEY')
    )

    chatbot_replies = [
        message['message']['content']
        for message in response['choices'] if message['message']['role'] == 'assistant'
    ]

    for reply in chatbot_replies:
        conversation.append({'role': 'assistant', 'content': reply})

    return conversation, chatbot_replies


def chatbot_view(request):

    # request.session.flush()
    # request.session.clear()

    conversation = request.session.get('conversation', [])
    tasks = request.session.get('tasks', [])
    prompts = request.session.get('prompts', [])
    flag = request.session.get('flag', False)

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        task_query = request.POST.get('task_query')
        task_complete = request.POST.get('task_complete_flag')

        if user_input is not None and not user_input.isspace() and user_input:
            if user_input.startswith('/chat'):
                user_input = user_input.replace('/chat ', '')

                if user_input:
                    conversation.append(
                        {'role': 'user', 'content': f"Task: {user_input.capitalize()}"})

                if not tasks:
                    prompts.append({
                        'role': 'user',
                        'content': f"{user_input}, {config('PROMPT_1')}"
                    })
                else:
                    str_inp = ', '.join(
                        [f"{task['name']} - {task['progress']}" for task in tasks])

                    prompts.append({
                        'role': 'user',
                        'content': f"{user_input}. {config('PROMPT_2_1')} {str_inp}. {config('PROMPT_2_2')}"
                    })

                conversation, chatbot_replies = process_chatbot_response(
                    prompts, conversation)

                request.session['conversation'] = conversation

                context = {
                    'user_input': user_input,
                    'chatbot_replies': chatbot_replies,
                    'conversation': conversation
                }
                return render(request, 'chat.html', context=context)

            else:
                print("Attempting to set task")

                if user_input:
                    conversation.append(
                        {'role': 'tasks', 'content': f"Task: {user_input.capitalize()}"})

                tasks.append({'name': user_input, 'progress': 'in progress'})

                request.session['tasks'] = tasks
                request.session['conversation'] = conversation

                context = {'user_input': user_input,
                           'conversation': conversation}
                print(f"reached 3 - {conversation}")
                return render(request, 'chat.html', context=context)

        elif task_complete:
            for task in tasks:
                if task['name'] == task_complete[6:].lower():
                    task['progress'] = 'complete'

            request.session['tasks'] = tasks

            context = {'conversation': conversation}
            return render(request, 'chat.html', context=context)

        else:
            request.session['tasks'] = [
                i for i in tasks if not (i['name'] == task_query[6:].lower())
            ]

            context = {'conversation': conversation}
            return render(request, 'chat.html', context=context)

    else:
        if not flag:
            request.session.flush()
            request.session.clear()

            prompts.append({
                'role': 'user',
                'content': config('PROMPT_3')
            })

            conversation, chatbot_replies = process_chatbot_response(
                prompts, conversation)

            prompts.extend(conversation)

            request.session['conversation'] = conversation
            request.session['prompts'] = prompts

            print("reached 5")

            flag = True
            request.session['flag'] = flag

            return render(request, 'chat.html', {'conversation': conversation})

        print("GET request")
        return render(request, 'chat.html', {'conversation': conversation})
