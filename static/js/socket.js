((() => {
    const dynamic_inp = document.getElementById('dynamic_inp'),
        inp_res = document.getElementById('inp-results');
    if (!window.WebSocket) {
        return;
    }
    const websocket_url = `${(window.location.protocol === 'https:' ? "wss://" : "ws://") +
    window.location.host}/suggestqueries`;
    const ws = new WebSocket(websocket_url);
    dynamic_inp.oninput = function () {
        inp_res.innerHTML = "";
        make_req(this, ws);
    };
    ws.onopen = e => {
        console.log(e);
    };
    ws.onmessage = _msg_ => {
        inp_res.innerHTML = "";
        _msg = _msg_.data;
        inp_res.style.display = 'block';
        try {
            var msg = JSON.parse(_msg);
            if (msg['no-res']) {
                return;
            }
        } catch (e) {
            console.log(e);
            return;
        }

        const data = msg.data;
        console.log(`Response Cached:${msg.Cached}`);

        for (const js of data) {
            const div = document.createElement("div");
            const span = document.createElement('span');
            div.setAttribute('data-im', js.id);
            div.onclick = function () {
                Beacon.send('/collect/', {
                    type: 'movieclick',
                    data: [{
                        movie: js.movie,
                        query: window.___currentWsMsg__,
                    }],
                    ua: navigator.userAgent,
                    touch: (navigator.maxTouchPoints > 0)
                })
                window.location = `/movie/${this.getAttribute('data-im')}/watch/`;
            };
            div.style.cursor = 'pointer';
            div.style.userSelect = 'none';
            div.style.listStyle = 'none';
            div.style.width = '45%';
            div.style.fontSize = 'small';
            div.className = 'sock-res';
            div.appendChild(span);
            div.style.margin = 'auto';
            span.innerHTML = js.movie;
            inp_res.appendChild(div);
            div.style.textAlign = 'left';
            div.style.border = '2px solid #e3e3e3';
            div.style.borderRadius = '5px';
        }
    };
    window.onclick = ({
        target
    }) => {
        if (target.className !== 'input_n' && target.className !== 'sock-res' && target != inp_res) {
            inp_res.innerHTML = '';
        }
    };

    function make_req({
        value
    }, ws) {
        const str = value;
        if (!check_inp(str)) {
            return;
        };
        window.___currentWsMsg__ = str;
        ws.send(str);
    }

    function check_inp(str) {
        return str.replace(/([^\w]|_)/g, '').length !== 0;
    }
}))();