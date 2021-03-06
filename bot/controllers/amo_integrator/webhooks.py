import requests
from telebot import types

from bot import bot, telegraph
from bot.controllers.amo_integrator.api_requests import send_from_user
from bot.models import User, TypeAction, ProblemAction, StaticMessage, ProblemAppearance
from config import amo_user_host, amo_api_leads, amo_api_contact, bot_pipeline, telegram_file_link, bot_token
from messages import review_sent, send_to_friend
from .utils import authorize


def proceed_update(update):
    lead = _get_lead(update)
    if lead:
        pipeline_id = lead['pipeline']['id']
        if pipeline_id == bot_pipeline:
            user = _get_user(lead)
            amo_type = _get_field(lead, 'ATYPE')[0]
            amo_problems = _get_field(lead, 'Травмы')
            action = TypeAction.objects.get(action_id=amo_type)
            problems = _get_problems(amo_problems)
            try:
                need_check = _get_field(lead, 'Проверка нужна?')[0]
            except IndexError:
                need_check = False
            send = False if need_check == '1' else user.send_review
            # if send and user.payed:
            if send:
                link = _send_review(action, problems, user)
                send_from_user(user, review_sent + ' ' + link)


def _send_review(action, problems, user):
    user.send_review = False
    user.save()
    hello_message = StaticMessage.objects.get(id=1)
    last_message = StaticMessage.objects.get(id=2)
    link = _create_review_page(hello_message, last_message, action, problems, user)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(send_to_friend, switch_inline_query=link))
    bot.send_message(user.id, link, reply_markup=markup)
    return link


def _create_review_page(hello_message, last_message, action, problems, user):
    photo = bot.get_user_profile_photos(user.id).photos[0][2]
    uploaded_user_photo = _upload_telegraph_file(bot.download_file(bot.get_file(photo.file_id).file_path))
    root_node = [
        {
            'tag': 'p',
            'children': [
                'Привет, %s' % user.first_name,
            ]
        },
        {
            'tag': 'img',
            'attrs': {
                'src': uploaded_user_photo
            }
        },
        {
            'tag': 'p',
            'children': [
                hello_message.text,
            ]
        },
        {
            'tag': 'p',
            'children': [
                action.text
            ]
        },

        {
            'tag': 'br',
            'children': []
        },
        {
            'tag': 'p',
            'children': [
                last_message.text
            ]
        },
    ]
    problems_node_list = []
    for problem in problems:
        problems_node_list.append({'tag': 'p', 'children': [problem.text]})
        appearance = ProblemAppearance.objects.filter(problem_id=problem.id, type_action=action).first()
        if appearance:
            problems_node_list.append({'tag': 'p', 'children': [appearance.text]})
    root_node = root_node[:4] + problems_node_list + root_node[4:]
    page = telegraph.create_page('Результаты типирования. ДКС.', root_node)
    return page['url']


def _get_user(lead):
    contact_id = lead['main_contact']['id']
    user_contact = _get_contact_details(contact_id)
    name = user_contact['name'].split('.')
    user_id = name[-1]
    user = User.objects.get(id=user_id)
    return user


def _get_lead(update):
    if 'leads[update][0][id]' in update:
        lead_id = update['leads[update][0][id]']
        lead = _get_lead_details(lead_id)
        return lead['_embedded']['items'][0]
    else:
        return None


def _get_lead_details(lead_id):
    cookies = authorize()
    url = amo_user_host + amo_api_leads + '?id=%s' % lead_id
    r = requests.get(url, cookies=cookies)
    return r.json()


def _get_contact_details(contact_id):
    cookies = authorize()
    url = amo_user_host + amo_api_contact + '?id=%s' % contact_id
    r = requests.get(url, cookies=cookies)
    return r.json()['_embedded']['items'][0]


def _get_field(lead, name):
    custom_fields = lead['custom_fields']
    result = []
    for field in custom_fields:
        if field['name'] == name:
            values = field['values']
            for val in values:
                result.append(val['value'])
    return result


def _get_problem_text(amo_problems):
    problems = _get_problems(amo_problems)
    result = '\n\n'
    for problem in problems:
        result += problem.text + '\n\n'
    return result


def _get_problems(amo_problems):
    result = []
    for amo_problem in amo_problems:
        try:
            problem = ProblemAction.objects.get(action_id=amo_problem)
            result.append(problem)
        except:
            pass
    return result


def _upload_telegraph_file(file):
    r = requests.post(
                'http://telegra.ph/upload',
                files={'file': ('file', file, 'image/jpeg')}  # image/gif, image/jpeg, image/jpg, image/png, video/mp4
    )
    return r.json()[0]['src']