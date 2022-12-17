# Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from . import __version__ as app_version
from frappe import __version__ as frappe_version


app_name = "strict_session_defaults"
app_title = "Strict Session Defaults"
app_publisher = "Ameen Ahmed (Level Up)"
app_description = "Frappe plugin that enforces and manages the session defaults popup."
app_icon = "octicon octicon-unlock"
app_color = "blue"
app_email = "kid1194@gmail.com"
app_license = "MIT"


is_frappe_above_v13 = int(frappe_version.split(".")[0]) > 13


app_include_js = [
    "strict_session_defaults.bundle.js"
] if is_frappe_above_v13 else [
    "/assets/strict_session_defaults/js/strict_session_defaults.js"
]


after_migrate = "strict_session_defaults.setup.after_migrate"


on_login = ["strict_session_defaults.override.on_login"]
on_logout = ["strict_session_defaults.override.on_logout"]