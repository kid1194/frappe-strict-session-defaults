# Frappe Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt

import frappe
from frappe.model.document import Document

class StrictSessionDefaultsSettings(Document):
	def after_save(self):
	    frappe.cache().hdel('strict_session_defaults_settings')
