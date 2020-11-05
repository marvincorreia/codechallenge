/**
 * default scripts
 * */
let UI_THEMES = ['Red', 'Green', 'Blue', 'Purple', 'Teal'];

/** get saved theme */
let ui_theme = localStorage.getItem('theme');
if (ui_theme == null) {
    setTheme('green')
} else {
    setTheme(ui_theme)
}

function UI_themePickerListener() {
    /** Populate drop-down with themes options */
    UI_THEMES.forEach(theme => {
        var element = document.createElement('a');
        element.textContent = theme;
        element.classList.add('dropdown-item');
        if (theme.toLowerCase() === ui_theme)
            element.classList.add('active');
        element.href = "#";
        element.onclick = function () {
            setTheme(this.textContent);
            $('#ui-theme-picker').find('a').removeClass('active');
            this.classList.add('active')
        };
        $("#ui-theme-picker").append(element);
    });
}

function setTheme(theme) {
    document.getElementById('theme-style').href = themes_path + '/' + theme.toLowerCase() + '.css';
    localStorage.setItem('theme', theme.toLowerCase())
}

$(document).ready(function () {
    UI_themePickerListener();

    $('[data-toggle="popover"]').popover();

    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle=modal]').click(function () {
        $(".modal").modal();
    });

    /** active nav items */
    $("li.nav-item").on('click', function () {
        if (!$(this).hasClass('dropdown')) {
            $("li.nav-item").removeClass('active');
            $(this).addClass("active")
        }
    }).each(function () {
        var item = $(this);
        item.find('a').each(function () {
            if ($(this).attr('href') === window.location.pathname) {
                item.find('a').removeClass('active');
                item.addClass("active");
                $(this).addClass("active");
            }
        }).find('.dropdown a').each(function () {
            if (window.location.pathname.includes($(this).attr('href')))
                item.addClass("active")
        });
    });
});

