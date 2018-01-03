# -*- coding: utf-8 -*-
# Copyright (c) 2018, Manqala Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import get_url
import requests



class TelebotSettings(Document):

	def validate(self):
		self.set_webhook()
	

	def set_webhook(self):
		try:
			url = "https://api.telegram.org/bot{}/setWebhook?".format(self.token)
			url += "url={}/api/method/telegram.telebot_api.get_update".format(get_url())
			r = requests.get(url,timeout=10)
		except Exception as e:
			frappe.log_error(e,'Timeout for Telebot')



