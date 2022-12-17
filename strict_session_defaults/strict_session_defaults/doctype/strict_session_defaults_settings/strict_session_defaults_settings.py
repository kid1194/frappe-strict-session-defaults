# Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from frappe.model.document import Document

from strict_session_defaults.override import clear_document_cache


class StrictSessionDefaultsSettings(Document):
	def before_save(self):
	    clear_document_cache(self.doctype)