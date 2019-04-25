function dataBaseTable() {
    $('#table').bootstrapTable({
        url: '/showDatabase/',
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
        search: true,

        columns: [{
            field: 'dataGroup',
            title: '数据库类型',
            switchable: true,
            sortable: true,
        }, {
            field: 'name',
            title: '名称',
            switchable: true,
            sortable: true,
        }, {
            field: 'ip',
            title: 'IP地址',
            switchable: true,
            sortable: true
        }, {
            field: 'user',
            title: '用户名',
            switchable: true,
            sortable: true,
        }, {
            field: 'password',
            title: '密码',
            switchable: true,
            sortable: true,
        }, {
            field: 'port',
            title: '端口',
            switchable: true,
            sortable: true,
        }, {
            field: 'edition',
            title: '版本',
            switchable: true,
            sortable: true,
        }, {
            field: 'remark',
            title: '备注',
            switchable: true,
            sortable: true,
        }, {
            field: 'uid',
            title: '操作',
            width: 120,
            align: 'center',
            valign: 'middle',
            switchable: true,
            formatter: operation,
        }],
        queryParams: function (params) {
            return {
                pageSize: params.limit, //每一页的数据行数，默认是上面设置的10(pageSize)
                pageNumber: params.offset / params.limit + 1, //当前页面,默认是上面设置的1(pageNumber)
                status: 'all',
            }
        },
        responseHandler: function (data) {
            $(".fixed-table-toolbar").append("<select class=\"select-control\" id=\"select_id\" onchange=\"data_clicks(this)\" style=\"width: 115px; margin-top:10px\">\n" +
                "</select>");
            var select = $("#select_id");
            select.append("<option value='all'>显示所有</option>");
            for (var i = 0; i < data.sort.length; i++) {
                var group = data.sort[i];
                select.append("<option value='" + group + "'>" + group + "</option>");
            }
            return data.rows;
        },
    });
}

function operation(value, row, index) {
    var uid = row.uid;
    var result = "";
    result += '<button data-toggle="modal" data-target="#databaseModal" onclick="upclick(' + uid + ')" style="color:#fff;background-color:#409eff;border-color:#409eff;border-style:solid">修改</button> ';
    result += '<button onclick=\'if (confirm("确定要删除吗？")) {window.location.href="/delDatabase/' + uid + '"}\' style="color:#fff;background-color:#c20003;border-color:#c20006;border-style:solid">删除</button>';
    return result;
}

function upclick(uid) {
    let formData = new FormData();
    formData.append("uid", uid);
    $.ajax({
        type: "post",
        contentType: false,
        processData: false,
        data: formData,
        url: "/updateDatabase/",
        dataType: "json",
        success: function (data) {
            $("#id_dataGroup").find("option:contains('" + data.dataGroup + "')").attr("selected", true);
            $('#id_name').val(data.name);
            $('#id_ip').val(data.ip);
            $('#id_user').val(data.user);
            $('#id_password').val(data.password);
            $('#id_port').val(data.port);
            $('#id_edition').val(data.edition);
            $('#id_remark').val(data.remark);
            $('#id_btn').text('修改');
            $('#id_uid').val(data.uid);
            $('#id_form').attr('action', '/updateDatabase/');
        }
    });
}