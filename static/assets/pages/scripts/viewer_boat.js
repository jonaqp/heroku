$(document).ready(function () {

    $('#shellcatch_timeliner').timeliner({
        containerwidth: 450,
        containerheight: 450,
        timelinewidth: 370,
        timelineheight: 5,
        timelineverticalmargin: 0,
        autoplay: false,
        showtooltiptime: true,
        repeat: false,
        showtotaltime: true,
        timedisplayposition: 'below',
        transition: 'fade'
    });


    $('#id_mac').on('change', function () {
        var value = $(this).val();
        var url_group_date = URL_DATE.replace(/identifier_mac/, value.toString());

        var $select = $('#id_trip');
        $.ajax({
            url: url_group_date,
            dataType: 'json'
        }).done(function (data) {
           $select.html('');
           $select.append("<option value='0'>--Seleccione--</option>");
            $.each(data, function (key, val) {
                $select.append('<option value="' + val + '">' + val + '</option>');
            })

        }).fail(function () {
             $select.html('');
             $select.append("<option value='0'>No hay registros</option>");
        })
    });
});
