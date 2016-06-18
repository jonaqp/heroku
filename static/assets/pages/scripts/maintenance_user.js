$(document).ready(function () {

    var div_page_content_inner = $('.page-content-inner');

    div_page_content_inner.on('click', '.view_user_edit', function () {
        var user_email = $(this).attr('data-email');
        var parameter = {
            'user_email': user_email
        };
        $.ajax({
            type: "GET",
            url: URL_USER_EDIT,
            data: parameter,
            success: function (data) {
                $('#load_user_add').html(data)
            }
        });

    });

    div_page_content_inner.on('click', '#view_user_update', function () {
        var email = $('#id_user_email').val();
        var form_pk = $(this).attr('data-id');

        var email_errors = $('#email_errors');
        switch (email) {
            case '':
                email_errors.addClass('has-error');
                return false;
            default:
                email_errors.removeClass('has-error');
                break;
        }

        var form = $('#form_user_profile');

        var parameter = {
            'form': get_FormDataserialize(form),
            'form_pk': form_pk
        };

        $.ajax({
            type: "POST",
            url: URL_USER_EDIT,
            data: JSON.stringify(parameter),
            success: function (data) {
                $('#load_user_add').html(data);
                $.ajax({
                    type: "GET",
                    url: URL_USER_LIST,
                    success: function (data) {
                        $('#load_user_list').html(data);
                    }
                });
            }
        });


    });


    div_page_content_inner.on('click', '.clean_field', function () {
        var form = $('#form_user_profile');
        resetForm(form)
    });

    div_page_content_inner.on('click', '.reload_page', function () {
        var i18n = load_translation_i18n();
        var form = $('#form_user_profile');
        resetForm(form);
        $('.reload_page').text(i18n.__("msg_cancel"));
         $('#view_user_update').text(i18n.__("msg_submit"));

        $(this).removeClass('reload_page').addClass('clean_field');
        $('#view_user_update').removeAttr('type').removeAttr('data-id')
            .removeAttr('id').attr('type', 'submit');

    });


});

