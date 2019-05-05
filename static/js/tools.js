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

function timestampToTime(timestamp) {
    var date = new Date(timestamp * 1000);//时间戳为10位需*1000，时间戳为13位的话不需乘1000
    var Y = date.getFullYear() + '-';
    var M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
    var D = date.getDate() + ' ';
    var h = date.getHours() + ':';
    var m = date.getMinutes() + ':';
    var s = date.getSeconds();
    return Y + M + D + h + m + s;
}

let timestamp = Math.round(new Date() / 1000);
$('#js_timestamp').val(timestamp);


$('#js_datetime_o').val(timestampToTime(timestamp));

$('#js_convert_timestamp').click(function () {
    let select = $('#js_timestamp_unit option:selected').val();
    if (select === 's') {
        let time = timestampToTime($('#js_timestamp').val());
        $('#js_datetime').val(time);
    } else {
        let time = timestampToTime($('#js_timestamp').val() / 1000);
        $('#js_datetime').val(time);
    }
});

$('#js_convert_datetime').click(function () {
    let select = $('#js_timestamp_unit_o option:selected').val();
    if (select === 's') {
        var date = new Date($('#js_datetime_o').val());
        var time = date.getTime();
        $('#js_timestamp_o').val(time);
    } else {
        var date = new Date($('#js_datetime_o').val());
        var time = date.getTime();
        $('#js_timestamp_o').val(time * 1000);
    }
});