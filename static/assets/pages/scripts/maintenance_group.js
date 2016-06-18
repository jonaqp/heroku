$(document).ready(function () {

    var div_page_content_inner = $('.page-content-inner');

    div_page_content_inner.on('click', '.view_group_edit', function () {
        var group_id = $(this).attr('data-id');
        var parameter = {
            'group_id': group_id
        };
        $.ajax({
            type: "GET",
            url: URL_GROUP_EDIT,
            data: parameter,
            success: function (data) {
                $('#load_group_add').html(data)
            }
        });

    });

    div_page_content_inner.on('click', '#view_group_update', function () {
        var name = $('#id_group_name').val();
        var status = $('#id_group_current_status').val();
        var form_pk = $(this).attr('data-id');
        var name_errors = $('#name_errors');
        var current_status_errors = $('#current_status_errors');
        switch (name) {
            case '':
                name_errors.addClass('has-error');
                return false;
            default:
                name_errors.removeClass('has-error');
                break;
        }

        switch (status) {
            case '':
                current_status_errors.addClass('has-error');
                return false;
            default:
                current_status_errors.removeClass('has-error');
                break;
        }

        var form = $('#form_group_state');

        var parameter = {
            'form': get_FormDataserialize(form),
            'form_pk': form_pk
        };

        $.ajax({
            type: "POST",
            url: URL_GROUP_EDIT,
            data: JSON.stringify(parameter),
            success: function (data) {
                $('#load_group_add').html(data);
                $.ajax({
                    type: "GET",
                    url: URL_GROUP_LIST,
                    success: function (data) {
                        $('#load_group_list').html(data);
                    }
                });
            }
        });


    });


    div_page_content_inner.on('click', '.clean_field', function () {
        var form = $('#form_group_state');
        resetForm(form)
    });

    div_page_content_inner.on('click', '.reload_page', function () {
        var i18n = load_translation_i18n();
        var form = $('#form_group_state');
        resetForm(form);
        $('.reload_page').text(i18n.__("msg_cancel"));
         $('#view_group_update').text(i18n.__("msg_submit"));

        $(this).removeClass('reload_page').addClass('clean_field');
        $('#view_group_update').removeAttr('type').removeAttr('data-id')
            .removeAttr('id').attr('type', 'submit');

    });




});
