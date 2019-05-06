let formData = new FormData();
formData.append('status', 'list')
$.ajax({
    type: "post",
    contentType: false,
    processData: false,
    data: formData,
    url: "/showSupervisor/",
    dataType: "json",
    success: function (data) {
        $('#tree').treeview({data: data});
        $('#tree').treeview('selectNode', [0, {silent: true}]);
        $('#tree').on('nodeSelected', function (event, data) {
            $('#table').bootstrapTable('destroy');
            table('first', data.id)
        });
    }
});
table('all', 'none');

function table(status, data) {
    $('#table').bootstrapTable({
        url: '/showSupervisor/',
        method: 'POST',
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        cache: false,   //是否启用 数据缓存
        sidePagination: 'client',   //谁来分页，客户端：'client'，服务端：'server'
        pageNumber: 1,   //默认显示 首页
        pageSize: 10,     //每页需要显示的数据量
        pagination: true,
        sortName: "create_time",
        sortOrder: "desc",
        pageList: "[10, 25, 50, 100, All]",
        search: false,
        toolbar: "#toolbar",
        columns: [{
            field: 'description',
            title: 'Description',
            switchable: true,
            sortable: true,
        }, {
            field: 'name',
            title: 'Name',
            switchable: true,
            sortable: true,
        }, {
            field: 'statename',
            title: 'State',
            switchable: true,
            sortable: true,
            cellStyle: function (value, row, index) {
                let css = {};
                if (row.state === 20) {
                    css = {css: {"color": "#28c210"}};
                } else if (row.state === 0) {
                    css = {css: {"color": "#ff0006"}};
                } else {
                    css = {css: {"color": "#ff0006"}};
                }
                return css
            }
        }, {
            field: 'logfile',
            title: 'logfile',
            switchable: true,
            sortable: true
        }, {
            field: 'uid',
            title: 'Action',
            width: 240,
            align: 'center',
            valign: 'middle',
            switchable: true,
            formatter: operation,
        }],
        queryParams: function (params) {
            return {
                status: status,
                id: data,
            }
        },
        responseHandler: function (data) {
            return data;
        },
    });
}


function operation(value, row, index) {
    var result = "";
    result += '<a style="margin-right: 10px;display: inline" href="/super?id=' + row.id + '&processname=' + row.name + '&action=restart">Restart</a>';
    result += '<a style="margin-right: 10px;display: inline" href="/super?id=' + row.id + '&processname=' + row.name + '&action=start">Start</a>';
    result += '<a style="margin-right: 10px;display: inline" href="/super?id=' + row.id + '&processname=' + row.name + '&action=stop">Stop</a>';
    result += '<a style="margin-right: 10px;display: inline" onmouseover="this.style.cursor=\'pointer\'" data-toggle="modal" data-target="#databaseModal"  onclick=\'WebSocketLog("' + row.id + '","' + row.name + '")\'>Tail -f</a>';
    return result;
};

function WebSocketLog(uid, name) {
    if ("WebSocket" in window) {
        // 打开一个 web socket
        // var host = window.location.host;
        var ws = new WebSocket("ws://" + location.hostname + ':' + 8001 + "/tailf/");
        ws.onopen = function () {
            // Web Socket 已连接上，使用 send() 方法发送数据
            let data = JSON.stringify({'id': uid, 'name': name});
            ws.send(data)
        };
        ws.onmessage = function (evt) {
            var received_msg = evt.data;
            $('#log').append(received_msg);
            document.getElementById('log').scrollTop = document.getElementById('log').scrollHeight;
        };
        ws.onclose = function () {
            // 关闭 websocket
            console.log("连接已关闭...");
        };
    } else {
        // 浏览器不支持 WebSocket
        alert("您的浏览器不支持 WebSocket!");
    }
}

$('#databaseModal').on('hide.bs.modal', function () {
    location.reload();
});

$('#startAllProcesses').click(function () {
    let arr = $('#tree').treeview('getSelected');
    let id = arr[0].id;
    window.open("/super?id=" + id + "&action=startAllProcesses", '_self')
});
$('#stopAllProcesses').click(function () {
    let arr = $('#tree').treeview('getSelected');
    let id = arr[0].id;
    window.open("/super?id=" + id + "&action=stopAllProcesses", '_self')
});
$('#restartService').click(function () {
    let arr = $('#tree').treeview('getSelected');
    let id = arr[0].id;
    window.open("/super?id=" + id + "&action=restartService", '_self')
});
$('#reloadConfig').click(function () {
    let arr = $('#tree').treeview('getSelected');
    let id = arr[0].id;
    window.open("/super?id=" + id + "&action=reloadConfig", '_self')
});


$(function () {
    var defaultData;
    var initSearchableTree = function () {
        return $('#tree').treeview({
            data: defaultData,
            nodeIcon: 'glyphicon glyphicon-globe',
            emptyIcon: '', //没有子节点的节点图标
            //collapsed: true,
        });
    };
    var $searchableTree = initSearchableTree();
    $('#tree').treeview('collapseAll', {
        silent: false//设置初始化节点关闭
    });
    var findSearchableNodes = function () {
        return $searchableTree.treeview('search', [$.trim($('#input-search').val()), {
            ignoreCase: false,
            exactMatch: false
        }]);
    };
    var searchableNodes = findSearchableNodes();
    $('#input-search').on('keyup', function (e) {
        var str = $('#input-search').val();
        if ($.trim(str).length > 0) {
            searchableNodes = findSearchableNodes();
        } else {
            $('#tree').treeview('collapseAll', {
                silent: false //设置初始化节点关闭
            });
        }
    });
});