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
        let elem = document.createElement('textarea');
        elem.readOnly = true;
        elem.className = 'output-textarea';
        elem.innerHTML = data['output']['stdout'] + data['output']['stderr'];
        // ta.textContent = (data['output']['stdout'] + data['output']['stderr']).replace('\r\n', '<br/>');
        $('#log-info').append(elem);
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
        $('#log-info').children().remove();
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
            $(this).removeClass().addClass('btn btn-outline-primary mr-4').attr('title', 'Run')
                .find('i').first().removeClass().addClass('fas fa-play');
            running = false;
            sendWebSocketData({action: 'stop_run'})
        } else {
            /** otherwise run it */
            $(this).removeClass().addClass('btn btn-danger mr-4').attr('title', 'Stop')
                .find('i').first().removeClass().addClass('fas fa-stop');
            $('#submit-btn').attr('disabled', '');
            $('input-btn').attr('disabled', '');
            var data = {
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
    running = false;
    $('#run-btn').removeClass().addClass('btn btn-outline-primary mr-4').attr('title', 'Run')
        .find('i').first().removeClass().addClass('fas fa-play');
    $('#submit-btn').removeAttr('disabled');
    $('#input-btn').removeAttr('disabled');
}