let formData = new FormData();
formData.append('status', 'list');
let tree = $('#tree');
$.ajax({
    type: "post",
    contentType: false,
    processData: false,
    data: formData,
    url: "/showSupervisor/",
    dataType: "json",
    success: function (data) {
        tree.treeview({data: data});
        tree.treeview('selectNode', [0, {silent: true}]);
        tree.on('nodeSelected', function (event, data) {
            table_append('first', data.id)
        });
    }
});

//搜索框
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

//列表框
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

function table_append(status, data) {
    $('#table').bootstrapTable('removeAll');
    let formData = new FormData();
    formData.append('status', status);
    formData.append('id', data);
    $.ajax({
        type: "post",
        contentType: false,
        processData: false,
        data: formData,
        url: "/showSupervisor/",
        dataType: "json",
        success: function (data) {
            for (let i = 0; i < data.length; i++) {
                let dataTree = data[i];
                $('#table').bootstrapTable('append', dataTree);
            }
        }
    });
}

function operation(value, row, index) {
    var result = "";
    result += '<a style="margin-right: 10px;display: inline" href="/super?id=' + row.id + '&processname=' + row.name + '&action=restart">Restart</a>';
    result += '<a style="margin-right: 10px;display: inline" href="/super?id=' + row.id + '&processname=' + row.name + '&action=start">Start</a>';
    result += '<a style="margin-right: 10px;display: inline" href="/super?id=' + row.id + '&processname=' + row.name + '&action=stop">Stop</a>';
    result += '<a style="margin-right: 10px;display: inline" onmouseover="this.style.cursor=\'pointer\'" data-toggle="modal" data-target="#tail"  onclick=\'WebSocketLog("' + row.id + '","' + row.name + '")\'>Tail -f</a>';
    return result;
};

//日志框
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


//工具栏按钮功能
function getid() {
    let arr = $('#tree').treeview('getSelected');
    let id = arr[0].id;
    return id
}

$('#startAllProcesses').click(function () {
    window.open("/super?id=" + getid() + "&action=startAllProcesses", '_self')
});

$('#stopAllProcesses').click(function () {
    window.open("/super?id=" + getid() + "&action=stopAllProcesses", '_self')
});

$('#restartService').click(function () {
    window.open("/super?id=" + getid() + "&action=restartService", '_self')
});

$('#reloadConfig').click(function () {
    window.open("/super?id=" + getid() + "&action=reloadConfig", '_self')
});

//tail -f log关闭后事件
$('#tail').on('hide.bs.modal', function () {
    location.reload();
});
$('#confModal').on('hide.bs.modal', function () {
    location.reload();
});
//编辑confi配置显示时事件
$('#confModal').on('show.bs.modal', function () {
    $('#view').text("loading...");
    let data = new FormData();
    data.append('id', getid());
    $.ajax({
        type: "post",
        contentType: false,
        processData: false,
        data: data,
        url: "/getSuperConf/",
        dataType: "json",
        success: function (data) {
            if (data.data === "err") {
                $('#view').text("Failed to load!\r\nTips:config file path must be /etc/supervisord.conf")
            } else {
                $('#view').text(data.data)
            }
        }
    });
});

//修改配置点击事件
$('#modify').click(function () {
    let content = $('#view').val();
    let data = new FormData();
    data.append('id', getid());
    data.append('content', content);
    $('#modify').attr("disabled", "disabled");
    $.ajax({
        type: "post",
        contentType: false,
        processData: false,
        data: data,
        url: "/saveSuperConf/",
        dataType: "json",
        success: function (data) {
            $('#modify').removeAttr('disabled');
            toastr.options.positionClass = 'toast-top-center';
            if (data.data === "err") {
                toastr.error("save faild");
            } else {
                toastr.success("success");
            }
        }
    });
});

//添加进程名搜索按钮和搜索框
$('.fixed-table-toolbar').append('<input type="input" class="form-control" id="name-search" placeholder="所有字段搜索" ' +
    'value="" style="position:absolute;right:35px;top: 58px;border:1px solid #286090;">');
$('.fixed-table-toolbar').append('<button type="input" class="btn btn-primary" ' +
    'id="name-btn" style="position:absolute;right:15px;top: 58px;">搜索</button>');

//搜索事件
$('#name-btn').click(
    function search() {
        let name = $('#name-search').val();
        let data = new FormData();
        data.append('name', name);
        $.ajax({
            type: "post",
            contentType: false,
            processData: false,
            data: data,
            url: "/searchSuperConf/",
            dataType: "json",
            success: function (data) {
                if (data.length > 0) {
                    tree.treeview({data: data});
                    tree.treeview('selectNode', [0, {silent: true}]);
                    table_append('first', data[0].id);
                    tree.on('nodeSelected', function (event, data) {
                        table_append('first', data.id)
                    });
                } else {
                    tree.treeview('remove');
                    $('#table').bootstrapTable('removeAll');
                }
            }
        });
    }
);


