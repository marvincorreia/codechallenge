$(document).ready(function () {
    $('[data-toggle="popover"]').popover();

    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle=modal]').click(function () {
        $(".modal").modal();
    });
});