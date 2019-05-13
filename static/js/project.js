function projectTable(category) {
    let formData = new FormData();
    formData.append("category", category);

    $('#table').bootstrapTable({
        url: '/project/',
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
        toolbar: '#toolbar',
        search: true,

        columns: [{
            field: 'name',
            title: '项目名称',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
        }, {
            field: 'host_name',
            title: '服务器名称',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
        }, {
            field: 'ip',
            title: 'IP地址',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
        }, {
            field: 'template_name',
            title: '模板名称',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
        }, {
            field: 'uid',
            title: '操作',
            width: 100,
            align: 'center',
            valign: 'middle',
            switchable: true,
            formatter: project,
        }],
        queryParams: function (params) {
            return {
                category: category,
                pageSize: params.limit, //每一页的数据行数，默认是上面设置的10(pageSize)
                pageNumber: params.offset / params.limit + 1, //当前页面,默认是上面设置的1(pageNumber)
            }
        },
        responseHandler: function (data) {
            return data.rows;
        },
    });
}

function project(value, row, index) {
    uid = row.uid;
    var host_id = row.host;
    var template_id = row.template;
    var name = row.name;
    var result = "";
    // result += '<button data-toggle="modal" data-target="#myModal3" onclick="upclick(' + uid + ')" style="color:#fff;background-color:#409eff;border-color:#409eff;border-style:solid">项目部署</button> ';

    result += '<button onclick=document.getElementById("host_id").value=' + host_id + ';document.getElementById("temp_id").value=' + template_id + ';document.getElementById("pro_title").innerText="项目名称:' + name + '"' +
        ' style="color:#fff;background-color:#672ade;border-color:#672ade;border-style:solid" data-toggle="modal"  data-target="#pro">部署项目</button> ';
    // result += '<button onclick=\'if (confirm("确定要删除吗？")) {window.location.href="/project_del/' + uid + '"}\' style="color:#fff;background-color:#c20003;border-color:#c20006;border-style:solid">删除</button>';
    return result;
}

//部署执行
$(function () {
    let time = $('#time');
    let pro_btn = $('#pro_btn');
    pro_btn.click(function () {
        if (confirm("确定要部署吗？，部署前请仔细确认模板是否选择正确"))
            if ($("#obj_up").val() === "") {
                $('#log').text("未选择文件,请先选择文件");
            } else {
                $('#log').text("文件上传中...");
                let uid = $('#host_id').val(); //服务器uid
                let obj_uid = $('#temp_id').val(); //模板uid
                let qname = $('#qname').val();
                let formData = new FormData();
                let uploadfile = $("#obj_up").val();
                formData.append("path", getFileName(uploadfile));
                formData.append("myfile", document.getElementById("obj_up").files[0]);
                formData.append("uid", uid);
                formData.append("qname", qname);
                var pd = time.is(':visible');
                if (pd) {
                    var obj_time = time.val();
                    formData.append("obj_time", obj_time);
                    formData.append("time_status", "1");
                } else {
                    formData.append("time_status", "0");
                }
                formData.append("obj_uid", obj_uid);
                $.ajax({
                    url: "/ufile/",
                    type: "POST",
                    dataType: 'json',
                    data: formData,
                    contentType: false,
                    processData: false,
                    xhr: function () { //获取ajaxSettings中的xhr对象，为它的upload属性绑定progress事件的处理函数
                        myXhr = $.ajaxSettings.xhr();
                        if (myXhr.upload) { //检查upload属性是否存在
                            //绑定progress事件的回调函数
                            myXhr.upload.addEventListener('progress', progressHandlingFunction, false);
                        }
                        return myXhr; //xhr对象返回给jQuery使用
                    },
                    success: function (data) {
                        if (data.status === 1) {
                            formData.delete("myfile");
                            $.ajax({
                                url: "/obj_hander/",
                                type: "POST",
                                dataType: 'json',
                                data: formData,
                                contentType: false,
                                processData: false,
                                success: function (data) {
                                    if (data.result === "time_error") {
                                        $("#log").text("时间不能为空，请检测设置！");
                                    } else if (data.result === "que_true") {
                                        $("#log").text("已添加计划任务！");
                                    } else if (data.result === "file_true") {
                                        $("#log").text("文件上传成功！");
                                    } else if (data.result === "file_false") {
                                        $("#log").text("文件上传失败！");
                                    } else if (data.result === "server_error") {
                                        $("#log").text("服务器错误！");
                                    } else {
                                        $("#log").text(data.result);
                                        WebSocketLog(uid, obj_uid);
                                    }
                                },
                                error: function () {
                                    $("#status").text("未知错误！");
                                }
                            });
                        } else {
                            $("#log").text("未选择文件,请先选择文件");
                        }
                    },
                    error: function () {
                        $("#status").text("未知错误！");

                    }
                });
            }
    });

    function progressHandlingFunction(e) {
        var curr = e.loaded;
        var total = e.total;
        process = curr / total * 100;
        if (process === 100) {
            $("#log").text('文件已上传到代理服务器,正在上传到目标服务器...');
            // WebSocketPublic()
        } else {
            $("#log").text('当前文件上传进度: ' + parseInt(process) + '%');
        }
    }
});

//日志控制
function WebSocketPublic() {
    if ("WebSocket" in window) {
        // 打开一个 web socket
        var host = window.location.host;
        var ws = new WebSocket("ws://" + host + "/public/");
        ws.onopen = function () {
            // Web Socket 已连接上，使用 send() 方法发送数据
            ws.send('1111')
        };
        ws.onmessage = function (evt) {
            var received_msg = evt.data;
            $('#log').append(received_msg);
        };
        ws.onclose = function () {
            // 关闭 websocket
            $('#log').append("连接已关闭...");
        };
    } else {
        // 浏览器不支持 WebSocket
        alert("您的浏览器不支持 WebSocket!");
    }
}


function choice(category) {
    var elements = document.querySelectorAll('.nav.nav-tabs li');
    //数组是of,对象是in
    for (let item of elements) {
        item.className = ''
    }
    let obj = event.srcElement.parentNode;
    obj.setAttribute("class", "active");
     $('#table').bootstrapTable('destroy');
    projectTable(category)
}
