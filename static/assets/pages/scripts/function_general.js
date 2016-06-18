function get_FormDataserialize(name_form) {
    var unindexed_array = name_form.serializeArray();
    var indexed_array = {};
    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'];
    });
    return indexed_array;
}

function resetForm($form) {
    $form.find('input:text, input:password, input:file, select, textarea').val('');
    $form.find('input:radio, input:checkbox')
         .removeAttr('checked').removeAttr('selected');
    $form.find('input[type=email]').val('');
}

function location_reload(){
    window.location.reload(false);
}


function load_translation_i18n(){
    var i18n;
    i18n = new I18n({
        directory: PATH_LANGUAGE,
        locale: CURRENT_LANGUAGE,
        extension: ".json"
    });
    return i18n

}

//function search_content_filter(div_content, event_id){
//
//    $('#page-content-inner').on('keyup','#search_reserv,ation_list', function () {
//        var filter_table_active;
//        var id_content_search_table = content_reservation_list.find("#nav_reservation_list").find('.active').find('a').attr('href');
//
//        filter_table_active = content_reservation_list.find(id_content_search_table).find("table tbody tr");
//        var rex = new RegExp($(this).val(), 'i');
//        filter_table_active.hide();
//        filter_table_active.filter(function () {
//            return rex.test($(this).text());
//        }).show();
//    });
//
//}

