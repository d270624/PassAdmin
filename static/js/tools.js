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
        $('#js_timestamp_o').val(time / 1000);
    } else {
        var date = new Date($('#js_datetime_o').val());
        var time = date.getTime();
        $('#js_timestamp_o').val(time);
    }
});

$('#projectRecord').on('show.bs.modal', function () {
    $('#table').bootstrapTable({
        url: '/getProjectDeploymentRecord/',
        method: 'GET',
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        cache: false,   //是否启用 数据缓存
        sidePagination: 'client',   //谁来分页，客户端：'client'，服务端：'server'
        pageNumber: 1,   //默认显示 首页
        pageSize: 10,     //每页需要显示的数据量
        queryParamsType: 'limit',
        pagination: true,
        singleSelect: false,
        clickToSelect: true,
        sortName: "create_time",
        sortOrder: "desc",
        pageList: "[10, 25, 50, 100, All]",
        search: true,
        columns: [{
            field: 'user',
            title: '用户名',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
            width: 100,
        }, {
            field: 'servername',
            title: '服务器名',
            width: 150,
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
        }, {
            field: 'projectname',
            title: '项目名',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
            width: 150,
        }, {
            field: 'filename',
            title: '文件名',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
            width: 150,
        }, {
            field: 'datetime',
            title: '更新时间',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
            width: 150,
        }],
        responseHandler: function (data) {
            return data.rows; //此处用于对结果进行处理，使分类变成字符串显示
        },
    });
});

$('#projectRecord').on('hide.bs.modal', function () {
    location.reload();
});


