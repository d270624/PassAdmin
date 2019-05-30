$('#table').bootstrapTable({
    cache: false,   //是否启用 数据缓存
    sidePagination: 'client',   //谁来分页，客户端：'client'，服务端：'server'
    pageNumber: 1,   //默认显示 首页
    pageSize: 10,     //每页需要显示的数据量
    pagination: true,
    sortName: "create_time",
    sortOrder: "desc",
    pageList: "[10, 25, 50, 100, All]",
    search: true,
    toolbar: "#toolbar",
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
    }]
});

$.ajax({
    type: "post",
    contentType: false,
    processData: false,
    url: "/showDatabase/",
    dataType: "json",
    success: function (data) {
        datas = data.rows;
        let rows = [];
        for (let i = 0; i < data.rows.length; i++) {
            let keys = data.rows[i]; //获取每一行数据
            for (let key in keys) {  //取键
                $("#toolbar .toolbar_ul").append('<li><a href="javascript:void(0);" onclick="choice(\'' + key + '\')">' + key + '</a></li>')
                for (let n = 0; n < keys[key].length; n++) {
                    if (i === 0) {
                        rows.push(keys[key][n]); //取所有键里面的值
                    }
                }
            }
        }
        $("#toolbar .toolbar_ul li:first").attr('class', 'active');
        $('#table').bootstrapTable('load', rows);
    }
});

function choice(category) {
    let rows = [];
    for (let i = 0; i < datas.length; i++) {
        let keys = datas[i];
        for (let key in keys) {
            if (key === category) {
                for (let n = 0; n < keys[key].length; n++) {
                    rows.push(keys[key][n]); //取所有键里面的值
                }
            }
        }
    }
    var elements = document.querySelectorAll('.nav.nav-tabs li');
    //数组是of,对象是in
    for (let item of elements) {
        item.className = ''
    }
    let obj = event.srcElement.parentNode;
    obj.setAttribute("class", "active");
    $('#table').bootstrapTable('load', rows);

}