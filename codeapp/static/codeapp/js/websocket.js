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
        let elem = document.createElement('textarea');
        elem.readOnly = true;
        elem.className = 'output-textarea';
        elem.innerHTML = data['output']['stdout'] + data['output']['stderr'];
        // ta.textContent = (data['output']['stdout'] + data['output']['stderr']).replace('\r\n', '<br/>');
        $('#log-info').append(elem);
        changeActionButtonsState('enable')
    };

    websocket.onclose = function (e) {
        console.error('ws disconnected');
        changeActionButtonsState('enable');
        setTimeout(function () {
            connectWebsocket();
        }, 2000)
    }
}

function sendWebsocketData(data) {
    if (websocket.readyState === WebSocket.OPEN) {
        $('#log-info').children().remove();
        changeActionButtonsState('disable');
        websocket.send(JSON.stringify(data));
    } else {
        alert("Websocket is closed")
    }
}

function changeActionButtonsState(state) {
    if (state === 'enable') {
        $('#action_buttons').find('button').each(function () {
            $(this).removeAttr('disabled')
        });
    } else if (state === 'disable') {
        $('#action_buttons').find('button').each(function () {
            $(this).attr('disabled', '')
        });
    }
}