//
// function getTree() {
//     var tree = [
//         {
//             text: "1",
//             {#icon: "glyphicon glyphicon-stop",#}
//             id: 1,
//         },
//         {
//             text: "2",
//         },
//         {
//             text: "3"
//         },
//         {
//             text: "4"
//         }
//     ];
//     return tree;
// }

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
    }
});

// $('#tree').treeview({data: getTree()});
// $('#tree').on('nodeSelected', function (event, data) {
//     console.log(event);
//     console.log(data)
// });

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
        sortable: true
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
            // pageSize: params.limit, //每一页的数据行数，默认是上面设置的10(pageSize)
            // pageNumber: params.offset / params.limit + 1, //当前页面,默认是上面设置的1(pageNumber)
            status: 'all',
        }
    },
    responseHandler: function (data) {
        // $(".fixed-table-toolbar").append("<select class=\"select-control\" id=\"select_id\" onchange=\"data_clicks(this)\" style=\"width: 115px; margin-top:10px\">\n" +
        //     "</select>");
        // var select = $("#select_id");
        // select.append("<option value='all'>显示所有</option>");
        // for (var i = 0; i < data.sort.length; i++) {
        //     var group = data.sort[i];
        //     select.append("<option value='" + group + "'>" + group + "</option>");
        // }
        return data.rows;
    },
})

function operation(value, row, index) {
    console.log(value);
    console.log(row);
    var result = "";
    result += '<a style="margin-right: 10px;display: inline" href="/super?processname=' + row.name + '&action=restart">Restart</a>';
    result += '<a style="margin-right: 10px;display: inline" href="/super?processname=' + row.name + '&action=Start">Start</a>';
    result += '<a style="margin-right: 10px;display: inline" href="/super?processname=' + row.name + '&action=Stop">Stop</a>';
    result += '<a style="margin-right: 10px;display: inline" href="/super?processname=' + row.name + '&action=logtail">Tail -f</a>';
    return result;
};