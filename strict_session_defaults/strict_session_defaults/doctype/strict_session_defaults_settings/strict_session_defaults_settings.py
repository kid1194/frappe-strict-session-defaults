# Frappe Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt

import frappe
from frappe.model.document import Document

from strict_session_defaults.override import _CACHE_KEY


class StrictSessionDefaultsSettings(Document):
	def after_save(self):
	    frappe.cache().hdel(_CACHE_KEY)
