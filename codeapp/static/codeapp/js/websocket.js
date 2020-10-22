/*----------------
    websocket script
-----------------*/

var challenge_id;
const ws_scheme = window.location.protocol === "https:" ? "wss:" : "ws:";
const path = `${ws_scheme}//${window.location.host}/ws/codeapp/`;
var websocket;

$(document).ready(function () {
    connectWebsocket();
    $('#run').on('click', function () {
        var data = {
            action: 'run',
            code: editor.getValue(),
            lang: editor.getModel().getLanguageIdentifier()['language']
        };
        sendWebsocketData(data)
    })
});

function connectWebsocket() {
    websocket = new WebSocket(path);

    websocket.onopen = function (e) {
        console.log("new connection");
    };

    websocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('Data received', data);
        let ta = document.createElement('textarea');
        ta.readOnly = true;
        ta.className = 'output-textarea';
        ta.innerHTML = data['output']['stdout'] + data['output']['stderr'];
        // ta.textContent = (data['output']['stdout'] + data['output']['stderr']).replace('\r\n', '<br/>');
        $('#log-info').append(ta);
        $('#action_buttons').find('button').each(function () {
            $(this).removeAttr('disabled')
        })
    };

    websocket.onclose = function (e) {
        console.error('ws disconnected');
        setTimeout(function () {
            connectWebsocket();
        }, 2000)
    }
}

function sendWebsocketData(data) {
    if (websocket.readyState === WebSocket.OPEN) {
        $('#log-info').children().remove();
        disableActionButtons();
        websocket.send(JSON.stringify(data));
    } else {
        alert("Websocket is closed")
    }
}

function disableActionButtons() {
    $('#action_buttons').find('button').each(function () {
        $(this).attr('disabled', '')
    });
}