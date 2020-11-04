$(document).ready(function () {
    let lang = JSON.parse($('#doc-lang').text());
    $(".try-sample").on('click', function () {
        changeEditorLanguage(lang);
        let preview = $(this).closest('.code-sample').find('pre');
        editor.setValue(preview[0].innerText.replace(/\xa0/g, ' '));
        if (preview.attr('data-input')) {
            $('#save-run').hide();
            $("#input-modal").on('hidden.bs.modal', function (e) {
                $("#run-btn").click();
                $('#save-run').show();
                $(this).off('hidden.bs.modal');
            });
            $("#input-textarea").val(preview.attr('data-input'));
            $("#input-btn").click();
        } else {
            $("#run-btn").click();
        }
    });
    setTimeout(function () {
        $('#submit-btn').attr('disabled', '');
        resetActionButtonsState = function () {
            setTimeout(function () {
                $('#run-btn').removeClass().addClass('btn btn-outline-primary mr-4').attr('title', 'Run')
                    .find('i').first().removeClass().addClass('fas fa-play');
                $('#submit-btn').attr('disabled', '');
                running = false;
            }, 1000);
        }
    }, 500);

    function changeDocLang() {
        setTimeout(function () {
            try {
                $("#lang-picker").val(lang);
                changeEditorLanguage(lang);
            } catch (e) {
                changeDocLang();
            }
        }, 500);
    }

    changeDocLang();
});