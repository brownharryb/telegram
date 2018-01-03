# -*- coding: utf-8 -*-
# Copyright (c) 2018, Manqala Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineQueryResultArticle, InputTextMessageContent


class Telebot(Document):
	
	def get_token(self):
		if self.bot_token:
			return self.bot_token


	def set_webhook(self):
		pass







#estate
TOKEN = "425544203:AAGwY9PuWf8lWTK4gvlnOO6vrfCOfYGZxeo"


bot = telepot.Bot(TOKEN)
EXPIRE = 240


@frappe.whitelist(allow_guest=True)
def get_update():
    try:
        form_dict = frappe.local.form_dict
        data = json.loads(form_dict.data)
        message_data = data.get('message') or data.get('edited_message')
        inline = handle_inline(data)
        if inline:
            return
        chat_id = message_data["chat"]["id"]
        #message = "dhsfbhdf"
        message = handle_response(chat_id, message_data)
        if message:
            reply_markup = None
            if isinstance(message, tuple)  and len(message) == 2:
                message, reply_markup = message
            bot.sendMessage(chat_id, message, reply_markup=reply_markup, parse_mode="HTML")
    except:
        frappe.logger().info(frappe.get_traceback())


def get_estates():
        return   [
                   {'estate_name':'Estate One', 'code':'/100'},
                   {'estate_name':'Estate Two', 'code':'/101'},
                   {'estate_name':'Estate Two', 'code':'/102'},
                        ]

def get_estate_info(code):
    estates = get_estates()
    for estate in estates:
        if code == estate['code']:
            return estate

def get_estate_services(code):
        return [
                    {'label':'Register Visitor', 'link':'http://rivtaf.01101960.xyz/login?redirect-to=/new_visit'},
                    {'label':'My Property Units', 'link':'http://rivtaf.01101960.xyz/login?redirect-to=/estate_units'},
                ]

def get_estate_services_html(code):
    services_html = ""
    estate_services = get_estate_services(code)
    for service in estate_services:
        services_html += "\n<a href='{}'>{}</a>".format(service['link'], service['label'])
    return services_html



def handle_0(chat_id, message_data):
    '''Expects estate code in incoming messsage.'''
    new_message = message_data['text']
    if new_message in ["","/start _"]:
        return
    new_message = new_message.strip()
    new_message = new_message.replace("  ","")
    estate_info = get_estate_info(new_message)
    if estate_info:
        #frappe.cache().set("{}_count".format(chat_id),"1")
        #frappe.cache().expire("{}_count".format(chat_id), EXPIRE)
        #frappe.cache().set("{}_1".format(chat_id), new_message)
        #frappe.cache().expire("{}_1".format(chat_id), EXPIRE)
        #reply_markup = reply_markup_for_mobile_number()
        services = get_estate_services_html(new_message)
        msg = "{} accepted \nPlease select a service for this estate to proceed..\n".format(estate_info['estate_name'])
        msg += services
        return msg
    return "Sorry,I can't find that estate please try again \xF0\x9F\x98\x94"

def handle_1(chat_id, message_data):
        '''Expects Phone Number.'''
        contact = message_data.get("contact")
        if contact and contact.get("phone_number"):
            phone_number = contact.get("phone_number")
            frappe.cache().set("{}_count".format(chat_id),"2")
            frappe.cache().expire("{}_count".format(chat_id), EXPIRE)
            frappe.cache().set("{}_2".format(chat_id), str(phone_number))
            frappe.cache().expire("{}_2".format(chat_id), EXPIRE)
            return "{} accepted, I found two property units for you {} and {}, please select one.".format(str(phone_number),"T48","T47")
        return ("I didn't catch that, please click the button to confirm your number", reply_markup_for_mobile_number())

def handle_2(chat_id, message_data):
        '''Expects Property Unit.'''
        new_message = message_data['text']
        new_message = new_message.strip()
        new_message = new_message.replace("  ","")
        if new_message in ["T48","T47"]:
            frappe.cache().set("{}_count".format(chat_id),"3")
            frappe.cache().expire("{}_count".format(chat_id), EXPIRE)
            frappe.cache().set("{}_3".format(chat_id), str(new_message))
            frappe.cache().expire("{}_3".format(chat_id), EXPIRE)
            return "{} Accepted, Please enter your visitor details".format(new_message)
        return "Please make a choice"

def handle_3(chat_id, message_data):
        new_message = message_data['text']
        new_message = new_message.strip()
        new_message = new_message.replace("  ","")
        frappe.cache().set("{}_count".format(chat_id),"4")
        frappe.cache().expire("{}_count".format(chat_id), EXPIRE)
        frappe.cache().set("{}_4".format(chat_id), str(new_message))
        frappe.cache().expire("{}_4".format(chat_id), EXPIRE)
        return "Visit Updated and visitor alerted, token is 12345678"

def handle_4(chat_id, message_data):
        return "Handler 4"

def handle_5(chat_id, message_data):
        return "Handler 5"

def reply_markup_for_mobile_number():
    reply_markup = ReplyKeyboardMarkup(keyboard=[
                            [KeyboardButton(text='Send Phone Number', request_contact=True)],
                        ])
    return reply_markup



def get_estate_codes():
    estates_html = ""
    estate_codes = get_estates()
    for estate in estate_codes:
        estates_html += "{} <pre>{}</pre>\n".format(estate['code'], estate['estate_name'])
    return estates_html



def handle_response(chat_id, message_data):
    message = None
    message_count_key = "{}_count".format(chat_id)
    count = frappe.cache().get(message_count_key)
    handlers = [handle_0, handle_1, handle_2, handle_3]
    text = message_data['text']
    first_name = message_data['from']['first_name']
    #bot.sendMessage(chat_id, text)
    if text in ['/start','/start _'] or not count:
        message = "Hi {} \nPlease send me the code of your estate from the list below..\n".format(first_name)
        message += get_estate_codes()
        bot.sendMessage(chat_id, message, parse_mode="HTML")
        frappe.cache().set(message_count_key, "0")
        frappe.cache().expire(message_count_key, EXPIRE)
        return
    count = int(count)
    message = handlers[count](chat_id, message_data)
    return message

def handle_inline(data):
    inline = data.get('inline_query')
    if not inline:
        return
    update_id = inline.get('id')
    bot.answerInlineQuery(update_id, [], switch_pm_text="Start Private Chat", switch_pm_parameter="_")
    return True
