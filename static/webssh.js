function get_term_size() {
    let init_width = 9.5;
    let init_height = 17.24;
    let windows_width = $(window).width();
    let windows_height = $(window).height();
    return {
        cols: Math.floor(windows_width / init_width),
        rows: Math.floor(windows_height / init_height),
    }
}

function webssh(id) {
    let cols = get_term_size().cols;
    let rows = get_term_size().rows;
    let aCookie = document.cookie.split("; ");

    for (let i = 0; i < aCookie.length; i++) {
        let f = aCookie[i].split('=');
        if (f[0] === "user") {
            var user = f[1]
        }
    }
    let term = new Terminal(
        {
            cols: cols,
            rows: rows,
            user: user,
            useStyle: true,
            cursorBlink: true
        }
        ),
        protocol = (location.protocol === 'https:') ? 'wss://' : 'ws://',
        socketURL = protocol + location.hostname + ((8001) ? (':' + 8001) : '') +
            '/webconnect/?' + 'id=' + id + '&width=' + cols + '&height=' + rows + '&user=' + user;

    let sock = new WebSocket(socketURL);

    sock.addEventListener('open', function () {
        $('#form').addClass('hide');
        $('#django-webssh-terminal').removeClass('hide');
        term.open(document.getElementById('terminal'));
    });

    sock.addEventListener('message', function (recv) {
        let data = JSON.parse(recv.data);
        let message = data.message;
        let status = data.status;
        if (status === 0) {
            term.write(message)
        } else if (status === 1) {
            alert("连接已关闭");
            window.close()
        } else {
            window.location.reload()
        }
        // $('#django-webssh-terminal').addClass('hide');
        // $('#form').removeClass('hide');
    });
    let message = {'status': 0, 'data': null, 'cols': null, 'rows': null};
    /*
    * status 为 0 时, 将用户输入的数据通过 websocket 传递给后台, data 为传递的数据, 忽略 cols 和 rows 参数
    * status 为 1 时, resize pty ssh 终端大小, cols 为每行显示的最大字数, rows 为每列显示的最大字数, 忽略 data 参数
    * */

    term.on('data', function (data) { // term.on方法就是实时监控输入的字段，
        message['status'] = 0;
        message['data'] = data;
        let send_data = JSON.stringify(message);
        sock.send(send_data)
    });

    $(window).resize(function () {
        let cols = get_term_size().cols;
        let rows = get_term_size().rows;
        message['status'] = 1;
        message['cols'] = cols;
        message['rows'] = rows;
        let send_data = JSON.stringify(message);
        sock.send(send_data);
        term.resize(cols, rows)
    })
}