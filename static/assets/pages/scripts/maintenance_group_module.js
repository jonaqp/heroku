$(document).ready(function () {

    var div_page_content_inner = $('.page-content-inner');

    div_page_content_inner.on('change', '#id_group_module_group, #id_group_module_module', function () {
        $('#load_formset_group_module').html('')
    });

    div_page_content_inner.on('click', '.validate_group_module', function () {
        var group = $('#id_group_module_group').val();
        var module = $('#id_group_module_module').val();
        var group_errors = $('#group_errors');
        var module_errors = $('#module_errors');

        switch (group) {
            case '':
                group_errors.addClass('has-error');
                return false;
            default:
                group_errors.removeClass('has-error');
                break;
        }

        switch (module) {
            case '':
                module_errors.addClass('has-error');
                return false;
            default:
                module_errors.removeClass('has-error');
                break;
        }

        var parameter = {
            'group': group,
            'module': module
        };

        $.ajax({
            type: "GET",
            url: URL_FORMSET_SUBMODULE,
            data: parameter,
            success: function (data) {
                $('#load_formset_group_module').html(data);
            }
        });

    });

    div_page_content_inner.on('click', '.submit_group_module', function () {
        var i18n = load_translation_i18n();
        var i18n_text;
        var complete1 = false;
        var complete2 = false;
        var complete3 = false;
        var total_count = $(this).attr('data-count');
        var prefix = $(this).attr('data-prefix');
        var count_submodule = $('#content_'+prefix).find('.dynamic-form');

        i18n_text = i18n.__("msg_total_sub_module %s", total_count);
        if (count_submodule.length > total_count){
           $('#load_msg').html("<div class='alert alert-warning'>" +
               "<strong>Warning! </strong>" + i18n_text +
               "</div>").show();
            return false;
        }else{
            complete1 = true;
            $('#load_msg').hide();
        }

        var text_list =[];
        count_submodule.find('select option:selected').each(function() {
            text_list.push(this.value);
        });
        var uniqueArray = text_list.filter(function(elem, pos,arr) {
            return arr.indexOf(elem) == pos;
        });
        if (text_list.length != uniqueArray.length){
            i18n_text = i18n.__("msg_choose_repeat");
            $('#load_msg').html("<div class='alert alert-warning'>" +
                   "<strong>Warning! </strong>" + i18n_text +
                   "</div>").show();
            return false;
        }else{
            complete2 = true;
        }

        var continue_ = 0;
        count_submodule.find('select option:selected').each(function(index, value) {
            var text_choose = i18n.__("msg_choose");
            i18n_text = i18n.__("msg_choose_change");
            if (this.text == text_choose){
               complete3 = false;
               continue_ = 1
            }else{
                complete3 = true;
            }

            if (continue_ == 1){
               continue_ = 1;
               complete3 = false;
               $('#load_msg').html("<div class='alert alert-warning'>" +
                   "<strong>Warning! </strong>" + i18n_text +
                   "</div>").show();
            }
        });

        if (complete1 && complete2 && complete3){
            $('#form_group_module').submit();
        }

    });

    div_page_content_inner.on('click', '.view_group_module_edit', function () {
        var group_module = $(this).attr('data-id');
        var module = $(this).attr('data-module');
        var parameter = {
            'group_module_pk': group_module,
            'module': module
        };
        $.ajax({
            type: "GET",
            url: URL_GROUP_MODULE_EDIT,
            data: parameter,
            success: function (data) {
                $('#load_group_module_add').html(data)
            }
        });

    });


    div_page_content_inner.on('click', '#view_group_module_update', function () {
        var form_pk = $(this).attr('data-id');
        var form = $('#form_group_module');
        var group = $('#id_group_module_group').val();
        var module = $('#id_group_module_module').val();
        var group_errors = $('#group_errors');
        var module_errors = $('#module_errors');

        switch (group) {
            case '':
                group_errors.addClass('has-error');
                return false;
            default:
                group_errors.removeClass('has-error');
                break;
        }

        switch (module) {
            case '':
                module_errors.addClass('has-error');
                return false;
            default:
                module_errors.removeClass('has-error');
                break;
        }

        var i18n = load_translation_i18n();
        var i18n_text;
        var complete1 = false;
        var complete2 = false;
        var complete3 = false;
        var total_count = $(this).attr('data-count');
        var prefix = $(this).attr('data-prefix');

        var count_submodule = $('#content_'+prefix).find('.dynamic-form').not(':hidden') ;

        i18n_text = i18n.__("msg_total_sub_module %s", total_count);
        if (count_submodule.length > total_count){
           $('#load_msg').html("<div class='alert alert-warning'>" +
               "<strong>Warning! </strong>" + i18n_text +
               "</div>").show();
            return false;
        }else{
            complete1 = true;
            $('#load_msg').hide();
        }

        var text_list =[];
        count_submodule.find('select option:selected').each(function() {
            text_list.push(this.value);
        });
        var uniqueArray = text_list.filter(function(elem, pos,arr) {
            return arr.indexOf(elem) == pos;
        });
        if (text_list.length != uniqueArray.length){
            i18n_text = i18n.__("msg_choose_repeat");
            $('#load_msg').html("<div class='alert alert-warning'>" +
                   "<strong>Warning! </strong>" + i18n_text +
                   "</div>").show();
            return false;
        }else{
            complete2 = true;
        }

        var continue_ = 0;
        count_submodule.find('select option:selected').each(function(index, value) {
            var text_choose = i18n.__("msg_choose");
            i18n_text = i18n.__("msg_choose_change");
            if (this.text == text_choose){
               complete3 = false;
               continue_ = 1
            }else{
                complete3 = true;
            }

            if (continue_ == 1){
               continue_ = 1;
               complete3 = false;
               $('#load_msg').html("<div class='alert alert-warning'>" +
                   "<strong>Warning! </strong>" + i18n_text +
                   "</div>").show();
            }
        });

        if (complete1 && complete2 && complete3){
            var parameter = {
                'formset': get_FormDataserialize(form),
                'form_pk': form_pk,
                'module': $('#id_group_module_module option:selected').text()
            };
            $.ajax({
                type: "POST",
                url: URL_GROUP_MODULE_EDIT,
                data: JSON.stringify(parameter),
                success: function (data) {
                    $('#load_group_module_add').html(data);

                    $.ajax({
                        type: "GET",
                        url: URL_GROUP_MODULE_LIST,
                        success: function (data) {
                            $('#load_group_module_list').html(data);
                        }
                    });
                }
            });

        }


    });


    div_page_content_inner.on('click', '.clean_field', function () {
        var form = $('#form_group_module');
        resetForm(form);
        $('#load_formset_group_module').html('');
        $('#load_msg').hide()
    });

    div_page_content_inner.on('click', '.reload_page', function () {
        var i18n = load_translation_i18n();
        var form = $('#form_group_module');
        resetForm(form);
        $('.reload_page').text(i18n.__("msg_cancel"));
         $('#view_group_module_update').text(i18n.__("msg_submit"));

        $(this).removeClass('reload_page').addClass('clean_field');
        $('#view_group_module_update').removeAttr('type').removeAttr('data-id')
            .removeAttr('id').attr('type', 'submit');

        $('#id_group_module_group').removeAttr('disabled');
        $('#id_group_module_module').removeAttr('disabled');
        $('.btn_principal').removeClass('hidden');
        $('#load_formset_group_module').html('');
        $('#load_msg').hide()
    });

});
