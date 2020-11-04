/*----------------
    websocket script
-----------------*/

var challenge_id;
const ws_scheme = window.location.protocol === "https:" ? "wss://" : "ws://";
const path = ws_scheme + window.location.host + '/ws/codeapp/code/';
var websocket;
var running = false;

$(document).ready(function () {
    actionButtonsListener();
    connectWebSocket();
});

function connectWebSocket() {
    websocket = new WebSocket(path);

    websocket.onopen = function (e) {
        console.log("new connection");
    };

    websocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('Data received', data);
        for (var i = 0; i < 2; i++) {
            let elem = document.createElement('textarea');
            elem.readOnly = true;
            elem.className = 'output-textarea';
            if (i === 0) {
                elem.innerHTML = data['output']['stdout'] /*+ data['output']['stderr']*/;
                $('#output-info').append(elem);
            } else {
                let errors = data['output']['stderr'];
                if (errors) {
                    $('#errors-badge').text("1");
                    elem.classList.add("stderr");
                    $('#outputs a[href="#errors"]').tab('show');
                } else {
                    // errors = "No errors to show";
                    $('#outputs a[href="#output"]').tab('show');
                }
                elem.innerHTML = errors;
                $('#errors-info').append(elem);
            }
        }
        resetActionButtonsState();
    };

    websocket.onclose = function (e) {
        console.error('ws disconnected');
        resetActionButtonsState();
        setTimeout(function () {
            connectWebSocket();
        }, 2000)
    }
}

function sendWebSocketData(data) {
    if (websocket.readyState === WebSocket.OPEN) {
        $('#output-info').children().remove();
        $('#errors-info').children().remove();
        $('#errors-badge').text("");
        websocket.send(JSON.stringify(data));
    } else {
        /** on fail reset buttons state */
        resetActionButtonsState();
        alert("Websocket is closed")
    }
}

function actionButtonsListener() {
    $('#save-run').on('click', function () {
        $('#run-btn').click();
    });

    $('#run-btn').on('click', function () {
        if (running) {
            /** if running stop it */
            /*$(this).removeClass().addClass('btn btn-outline-primary mr-4').attr('title', 'Run')
                .find('i').first().removeClass().addClass('fas fa-play');
            running = false;
            sendWebSocketData({action: 'stop_run'})*/
        } else {
            /** otherwise run it */
            $(this).removeClass().addClass('btn btn-danger mr-4')
                .find('i').first().removeClass().addClass('fa fa-cog fa-spin');
            $('#submit-btn').attr('disabled', '');
            const data = {
                action: 'run',
                code: editor.getValue(),
                lang: editor.getModel().getLanguageIdentifier()['language'],
                input: $('#input-textarea').val()
            };
            running = true;
            sendWebSocketData(data)
        }
    });
    $('#submit-btn').on('click', function () {
        /** disable submit and run buttons */
    });
}

function resetActionButtonsState() {
    setTimeout(function () {
        $('#run-btn').removeClass().addClass('btn btn-outline-primary mr-4').attr('title', 'Run')
            .find('i').first().removeClass().addClass('fas fa-play');
        $('#submit-btn').removeAttr('disabled');
        running = false;
    }, 1000);
}