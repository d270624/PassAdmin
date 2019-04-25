$('#port_btn').click(function () {
    let ip = $('#port_ip').val();
    let port = $('#port_p').val();
    let status = $('#status');
    let data = {"type": "port", "content": {"ip": ip, "port": port}};
    status.show();
    status.text('检测中...');
    $.ajax({
        url: "/gettools/",
        type: "POST",
        data: JSON.stringify(data),
        processData: false,
        success: function (data) {
            status.text('检测结果：' + data.status)
        },
        error: function () {
            console.log('连接失败')
        }
    })
});