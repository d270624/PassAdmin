function UrlMgmTable() {
    $('#table').bootstrapTable({
        url: '/showUrlMgm/',
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
            field: 'name',
            title: '名称',
            switchable: true,
            sortable: true,
        }, {
            field: 'url',
            title: 'url地址',
            switchable: true,
            sortable: true
        }, {
            field: 'user',
            title: '账号',
            switchable: true,
            sortable: true,
        }, {
            field: 'password',
            title: '密码',
            switchable: true,
            sortable: true,
        }, {
            field: 'uid',
            title: '操作',
            width: 120,
            align: 'center',
            valign: 'middle',
            switchable: true,
            formatter: access,
        }],
        queryParams: function (params) {
            return {
                pageSize: params.limit, //每一页的数据行数，默认是上面设置的10(pageSize)
                pageNumber: params.offset / params.limit + 1, //当前页面,默认是上面设置的1(pageNumber)
                status: 'all',
            }
        },
        responseHandler: function (data) {
            return data.rows;
        },
    });
}

function access(value, row, index) {
    var url = row.url;
    var result = "";
    result += '<button data-toggle="modal" data-target="#databaseModal" onclick=\'window.open("' + url + '")\' style="color:#fff;background-color:#409eff;border-color:#409eff;border-style:solid">访问</button> ';
    return result;
}