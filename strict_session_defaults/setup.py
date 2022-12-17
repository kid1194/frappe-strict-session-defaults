# Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from strict_session_defaults.override import (
    _SETTINGS_DOCTYPE,
    _LOG_DOCTYPE,
    clear_user_cache,
    clear_document_cache
)


def after_migrate():
    clear_user_cache()
    clear_document_cache(_SETTINGS_DOCTYPE)
    clear_document_cache(_LOG_DOCTYPE)