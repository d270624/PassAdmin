var setting = {
    view: {
        selectedMulti: false
    },
    check: {
        enable: true
    },
    data: {
        simpleData: {
            enable: true
        }
    },
    edit: {
        enable: false
    }
};
$(document).ready(function () {
    $.ajax({
        url: "/tree/", success: function (results) {
            var parsedJson = jQuery.parseJSON(results);
            $.fn.zTree.init($("#tree"), setting, parsedJson);

            document.getElementById("key").value = ""; //清空搜索框中的内容
            //绑定事件
            key = $("#key");
            key.bind("focus", focusKey)
                .bind("blur", blurKey)
                .bind("propertychange", searchNode) //property(属性)change(改变)的时候，触发事件
                .bind("input", searchNode);
        }
    });
    $('#template').bootstrapTable({
        url: '/getTemplate/',
        method: 'get',
        sidePagination: 'client',   //谁来分页，客户端：'client'，服务端：'server'
        pageNumber: 1,   //默认显示 首页
        pageSize: 10,     //每页需要显示的数据量
        pageList: "[10, 25, 50, 100, All]", //可供选择的，每页需要显示的数据量
        sortable: false,
        columns: [{
            field: 'name',
            title: 'name',
            sortable: true,
            formatter: paramsMatter,
        }, {
            width: 105,
            field: 'content',
            title: 'operation',
            formatter: actionFormatter,
        }],
        responseHandler: function (data) {
            return data.rows;
        },
        onDblClickRow: function (row) {
            $('#cmd').val(row.content);
        }
    });
});
var setting = {
    view: {
        fontCss: setFontCss
    },
    data: {
        simpleData: {
            enable: true
        }
    }
};

//提示框
function paramsMatter(value, row, index) {
    var span = document.createElement('span');
    span.setAttribute('title', row.content);
    span.innerHTML = value;
    return span.outerHTML;
}

//操作框
function actionFormatter(value, row, index) {
    let myArray = [];
    myArray[0] = row.uid;
    myArray[1] = row.name;
    myArray[2] = row.content;
    let result = "";
    result += '<button onclick=\"modify(\'' + row.uid + '\',\'' + row.name + '\',\'' + row.content + '\')" style="color:#fff;background-color:#409eff;border-color:#409eff;border-style:solid">编辑</button>';
    result += '<button onclick="del_template(' + row.uid + ')" style="color:#fff;background-color:#c20003;border-color:#c20006;border-style:solid">删除</button>';
    return result;
}

// 编辑模板
function modify(uid, name, content) {
    $('#temp_name').val(name);
    $('#temp_text').val(content);
    $('#temp_uid').val(uid);
    $('#temp_btn').text('修改');
    $('#server').modal();
}

//删除模板
function del_template(uid) {
    if (confirm("你确定要删除吗？")) {
        $.ajax(
            {
                url: "/delTemplate/",
                data: {'uid': uid},
                type: 'post',
                dataType: 'json',
                async: true,
                success: function (data) {
                    alert(data.mes)
                    location.reload();
                },
                error: function (status, error) {
                    alert(error)
                }
            }
        )
    }
}

//添加模板，修改模板
$('#temp_btn').click(function () {
    var temp_uid = $('#temp_uid').val();
    var temp_name = $('#temp_name').val();
    var temp_text = $('#temp_text').val();
    $.ajax(
        {
            url: '/addTemplate/',
            data: {'temp_name': temp_name, 'temp_text': temp_text, 'temp_uid': temp_uid},
            type: 'post',
            dataType: 'json',
            async: 'true',
            success: function (data) {
                alert(data.mes)
                location.reload();
            },
            error: function (status, error) {
                alert(error)
            }
        })
});
//弹框实现移动效果
$('#server').draggable();
$('#myModal').draggable();


//-->
$("#run").click(function () {
        var status = $("#status");
        var table = $('#table');
        status.text("运行中...");
        table.bootstrapTable('destroy');
        var treeObj = $.fn.zTree.getZTreeObj("tree");
        nodes = treeObj.getCheckedNodes(true);
        var ids = [];
        for (var i = 0; i < nodes.length; i++) {
            if (nodes[i].id >= 0) {
                ids[ids.length] = nodes[i].id;
            }
        }
        table.bootstrapTable({
            url: '/linux/',
            method: 'POST',
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            cache: true,   //是否启用 数据缓存
            sidePagination: 'client',   //谁来分页，客户端：'client'，服务端：'server'
            pageNumber: 1,   //默认显示 首页
            pageSize: 10,     //每页需要显示的数据量
            pageList: "[10, 25, 50, 100, All]", //可供选择的，每页需要显示的数据量
            queryParamsType: 'limit',
            pagination: true,
            responseHandler: function (data) {
                return data;
            },
            queryParams: function (params) {
                return {
                    //pageSize: params.limit, //每一页的数据行数，默认是上面设置的10(pageSize)
                    //pageNumber: params.offset / params.limit + 1, //当前页面,默认是上面设置的1(pageNumber)
                    cmd: $("#cmd").val(),
                    uid: JSON.stringify(ids),
                }
            },   //查询参数,
            columns: [{
                field: 'hostname',
                title: 'hostname',
                sortable: true
            }, {
                field: 'ip',
                title: 'ip',
                sortable: true
            },
                {
                    field: 'result',
                    title: 'result',
                    sortable: true
                }],
            onLoadSuccess: function () {
                status.text("运行结束")
            }, onLoadError: function () {
                console.log("数据加载失败");
                status.text("运行结束");
            },
        });
    }
);