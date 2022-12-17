/*
*  Strict Session Defaults © 2022
*  Author:  Ameen Ahmed
*  Company: Level Up Marketing & Software Development Services
*  Licence: Please refer to LICENSE file
*/


frappe.provide('frappe.ui.toolbar');
frappe.provide('frappe.router');


class StrictSessionDefaults {
    constructor() {
        this._fields = null;
        this._reqds = null;
        this.init();
    }
    error(text, args, _throw) {
        if (_throw == null && args === true) {
            _throw = args;
            args = null;
        }
        if (_throw) {
            frappe.throw(__(text, args));
            return this;
        }
        frappe.msgprint({
            title: __('Error'),
            indicator: 'Red',
            message: __(text, args),
        });
        return this;
    }
    init() {
        if (this._reqds) {
            this.get_fields();
            return this;
        }
        var me = this;
        frappe.call({
            method: 'strict_session_defaults.override.get_status',
            'async': true,
        }).then(function(ret) {
            if (ret && $.isPlainObject(ret)) ret = ret.message || ret;
            if (!$.isPlainObject(ret)) {
                me.error('The data received from Strict Session Defaults is invalid.');
                return;
            }
            if (!ret.show) return;
            me._reqds = ret.reqds;
            me.get_fields();
        });
    }
    get_fields() {
        if (this._fields) {
            this.show();
            return this;
        }
        var me = this;
        frappe.call({
            method: 'frappe.core.doctype.session_default_settings.session_default_settings.get_session_default_values',
            'async': true,
            callback: function(ret) {
                if (ret && $.isPlainObject(ret)) ret = ret.message || ret;
                if (typeof ret !== 'string' && !$.isArray(ret)) {
                    me.error('The fields received from session default settings are invalid.');
                    return;
                }
                let fields = null;
                try {
                    fields = JSON.parse(ret);
                } catch(e) {
                    fields = ret;
                }
                if (!$.isArray(fields)) {
                    me.error('The fields received from session default settings are invalid.');
                    reject();
                    return;
                }
                me._fields = fields;
                me._fields.unshift({
                    fieldname: 'error_message',
                    fieldtype: 'HTML',
                    label: '',
                    read_only: 1
                });
                me.show();
            }
        });
    }
    show() {
        if (this._dialog) {
            this._dialog.show();
            return;
        }
        
        var me = this;
        if (!frappe.ui.toolbar.setup_session_defaults) {
            window.setTimeout(function() {
                me.show();
            }, 200);
            return;
        }
        this._dialog = new frappe.ui.Dialog({
            fields: this._fields,
            title: __('Session Defaults'),
            indicator: 'green',
        });
        
        this._dialog.$wrapper.modal({
			backdrop: 'static',
			keyboard: false,
			show: false
		});
		
        var error_message = this._dialog.get_field('error_message');
        error_message.$wrapper.append(`<div class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong class="error-message"></strong>
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`);
        
        var error_alert = error_message.$wrapper.find('.alert'),
        error_msg = error_alert.find('.error-message');
        error_alert.alert();
        
        this._dialog.set_primary_action(__('Save'), function() {
            var values = me._dialog.get_values();
            if (!values) {
                me._dialog.hide();
                me.error('An error occurred while setting Session Defaults');
                return;
            }
            
            error_alert.alert('close');
            error_msg.html('');
            
            var count = 0;
            me._fields.forEach(function(fd) {
                let name = fd.fieldname;
                if (
                    (!me._reqds || !me._reqds.length || me._reqds.indexOf(fd) >= 0)
                    && !!values[name]
                ) {
                    count++;
                }
                else if (!values[name]) values[name] = "";
            });
            
            if (me._reqds && me._reqds.length && count !== me._reqds.length) {
                error_msg.html(__('Please fill at least all the required fields.'));
                error_alert.alert('show');
                frappe.ui.scroll(error_alert);
                return;
            } else if (!count) {
                error_msg.html(__('Please fill at least one field.'));
                error_alert.alert('show');
                frappe.ui.scroll(error_alert);
                return;
            }
            
            me._dialog.hide();
            me.send(values);
        });
        this._dialog.header.find('.modal-actions').remove();
        this._dialog.show();
    }
    send(values) {
        var me = this;
        frappe.call({
            method: 'frappe.core.doctype.session_default_settings.session_default_settings.set_session_default_values',
            args: {default_values: values},
            'async': true,
            callback: function(ret) {
                if (ret.message == "success") {
                    frappe.show_alert({
                        message: __('Session Defaults Saved'),
                        indicator: 'green'
                    });
                    frappe.call({
                        method: 'strict_session_defaults.override.update_status',
                        'async': true,
                    });
                    frappe.ui.toolbar.clear_cache();
                } else {
                    me.error('An error occurred while setting Session Defaults');
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    let route = frappe.router.current_route;
    if (!$.isArray(route) || !route.length
    || route[0].toLowerCase() === 'login'
    || (route[1] && route[1].toLowerCase() === 'login')) return;
    
    new StrictSessionDefaults();
});