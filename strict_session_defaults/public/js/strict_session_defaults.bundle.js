frappe.provide('frappe.strict_session_defaults');
frappe.provide('frappe.ui.toolbar');

frappe.strict_session_defaults.init = function() {
    frappe.call({
        type: 'GET',
        method: 'strict_session_defaults.override.get_status',
    }).then(function(res) {
        let data = res.message;
        if (!data.is_ready && !frappe.strict_session_defaults._is_checked) {
            frappe.call({
                type: 'GET',
                method: 'strict_session_defaults.override.get_settings',
            }).then(function(res) {
                frappe.strict_session_defaults._is_checked = true;
                frappe.strict_session_defaults.init();
            });
            return;
        }
        if (!data.is_ready || !data.show) return;
        frappe.strict_session_defaults.show();
    });
};

frappe.strict_session_defaults.show = function() {
    if (frappe.strict_session_defaults._is_shown) return;
    if (!frappe.ui.toolbar.setup_session_defaults) {
        window.setTimeout(function() {
            frappe.strict_session_defaults.show();
        }, 200);
        return;
    }
    frappe.strict_session_defaults._is_shown = true;
    frappe.call({
        method: 'frappe.core.doctype.session_default_settings.session_default_settings.get_session_default_values',
        callback: function(data) {
            let fields = JSON.parse(data.message);
            var d = new frappe.ui.Dialog({
                fields: fields,
                title: __('Session Defaults'),
                'static': true
            });
            d.set_primary_action(__('Save'), function() {
                var values = d.get_values();
                if (!values) {
                    d.hide();
                    frappe.throw(_('An error occurred while setting Session Defaults'));
                    return;
                }
                // if default is not set for a particular field in prompt
                let count = 0;
                fields.forEach(function(d) {
                    if (!values[d.fieldname]) values[d.fieldname] = "";
                    else count++;
                });
                if (!count) {
                    frappe.show_alert({
                        'message': __('Please fill the form of Session Defaults.'),
                        'indicator': 'orange'
                    });
                    return;
                }
                frappe.call({
                    method: 'frappe.core.doctype.session_default_settings.session_default_settings.set_session_default_values',
                    args: {
                        default_values: values,
                    },
                    callback: function(data) {
                        d.hide();
                        if (data.message == "success") {
                            frappe.show_alert({
                                'message': __('Session Defaults Saved'),
                                'indicator': 'green'
                            });
                            frappe.ui.toolbar.clear_cache();
                            frappe.call({
                                type: 'GET',
                                method: 'strict_session_defaults.override.update_status',
                            });
                        } else {
                            frappe.throw(__('An error occurred while setting Session Defaults'));
                        }
                    }
                });
            });
            d.header.find('.modal-actions').remove();
            d.show();
        }
    });
};

frappe.ready(function() {
    if (frappe.get_route_str().includes('/login')) return;
    frappe.strict_session_defaults.init();
});
