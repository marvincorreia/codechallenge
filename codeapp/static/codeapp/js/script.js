/**
 * default scripts
 * */

$(document).ready(function () {
    $('[data-toggle="popover"]').popover();

    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle=modal]').click(function () {
        $(".modal").modal();
    });
    $("li.nav-item").on('click', function () {
        $("li.nav-item").removeClass('active');
        $(this).addClass("active")
    });
    $("li.nav-item").each(function () {
        var item = $(this);
        item.find('a').each(function () {
            if ($(this).attr('href') === window.location.pathname)
                item.addClass("active")
        });

    });
});