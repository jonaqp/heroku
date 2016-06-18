$(document).ready(function () {

    var div_page_content_inner = $('.page-content-inner');

    div_page_content_inner.on('click', '.view_container_edit', function () {
        var container_id = $(this).attr('data-id');
        var parameter = {
            'container_id': container_id
        };
        $.ajax({
            type: "GET",
            url: URL_CONTAINER_EDIT,
            data: parameter,
            success: function (data) {
                $('#load_container_add').html(data)
            }
        });

    });

    div_page_content_inner.on('click', '#view_container_update', function () {

        var form_pk = $(this).attr('data-id');
        var form = $('#form_container');

        var parameter = {
            'form': get_FormDataserialize(form),
            'form_pk': form_pk
        };

        $.ajax({
            type: "POST",
            url: URL_CONTAINER_EDIT,
            data: JSON.stringify(parameter),
            success: function (data) {
                $('#load_container_add').html(data);
                $.ajax({
                    type: "GET",
                    url: URL_CONTAINER_LIST,
                    success: function (data) {
                        $('#load_container_list').html(data);
                    }
                });
            }
        });


    });


    div_page_content_inner.on('click', '.clean_field', function () {
        var form = $('#form_container');
        resetForm(form);
        // window.location.href = window.location.pathname;
    });

    div_page_content_inner.on('click', '.reload_page', function () {
        var i18n = load_translation_i18n();
        var form = $('#form_container');
        resetForm(form);
        $('.reload_page').text(i18n.__("msg_cancel"));
         $('#view_container_update').text(i18n.__("msg_submit"));

        $(this).removeClass('reload_page').addClass('clean_field');
        $('#view_container_update').removeAttr('type').removeAttr('data-id')
            .removeAttr('id').attr('type', 'submit');

    });


});

