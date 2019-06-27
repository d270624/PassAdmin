//时间格式化
function CurentTime() {
    var now = new Date();
    var year = now.getFullYear();       //年
    var month = now.getMonth() + 1;     //月
    var day = now.getDate();            //日
    var hh = now.getHours();            //时
    var mm = now.getMinutes();          //分
    var ss = now.getSeconds();          //分
    var clock = year + "-";
    if (month < 10)
        clock += "0";
    clock += month + "-";
    if (day < 10)
        clock += "0";
    clock += day + "T";
    if (hh < 10)
        clock += "0";
    clock += hh + ":";
    if (mm < 10) clock += '0';
    clock += mm + ":";
    if (ss < 10) clock += '0';
    clock += ss;
    return (clock);
}

//操作栏的格式化
function actionFormatter(value, row, index) {
    var id = row.uid;
    var rows = row.hostname;
    var repUid = row.repUid;
    var auth = row.auth;
    var result = "";
    result += '<button onclick=window.open("/webssh/' + id + '") class="btn btn-danger btn-sm" style="margin-left: 0;background-color: #017162;border-color: #017162">web连接</button> ';
    result += '<button onclick=window.location.href="/xshell/' + id + '" class="btn btn-danger btn-sm" style="margin-left: 0;background-color: #017162;border-color: #017162">Xshell连接</button> ';
    result += '<button onclick=window.location.href="/xftp/' + id + '" class="btn btn-success btn-sm" style="margin-left: 0">Xftp上传</button> ';

    result += '<button onclick=document.getElementById("up_uid").value=' + id + ';document.getElementById("myModalLabel").innerText="服务器:' + rows + '"' +
        ' class="btn btn-success btn-sm" style="margin-left: 0" data-toggle="modal" data-target="#myModal">在线上传</button> ';

    result += '<button onclick=document.getElementById("uid3").value=' + id + ';document.getElementById("myModalLabel3").innerText="服务器:' + rows + '"' +
        ' class="btn btn-info btn-sm" style="margin-left: 0;" data-toggle="modal"  data-target="#myModal3">项目部署</button> ';

    result += '<button onclick=document.getElementById("uid4").value=' + id + ';document.getElementById("uid5").value="' + repUid + '";document.getElementById("myModalLabel4").innerText="服务器:' + rows + '"' +
        ' class="btn btn-primary btn-sm" style="margin-left: 0" data-toggle="modal"  data-target="#myModal4">备注</button> ';
    if (auth === 1) {
        result += '<button onclick=window.location.href="/update/' + id + '" class="btn btn-warning btn-sm" style="margin-left: 0">修改</button> ';
        result += '<button onclick=\'if (confirm("确定要删除吗？")) {window.location.href="/del/' + id + '"}\' class="btn btn-danger btn-sm" style="margin-left: 0">删除</button>';
    }
    return result;

}

function tt(url) {
    let formData = new FormData();
    let arr = url.split('|');
    if (arr.length === 1) {
        formData.append("status", arr[0]);
        formData.append("project", "None");
    } else {
        formData.append("status", arr[0]);
        formData.append("project", arr[1]);
    }
    var elements = document.querySelectorAll('.nav.nav-tabs li');
    //数组是of,对象是in
    for (let item of elements) {
        item.className = ''
    }

    let objs = event.srcElement.parentNode;
    obj = objs.parentNode.parentNode;
    if (obj.className === "") {
        obj.setAttribute("class", "active");
    } else {
        objs.setAttribute("class", "active");
    }

    $.ajax({
        type: "post",
        contentType: false,
        processData: false,
        data: formData,
        url: "/getServerList/",
        dataType: "json",
        success: function (data) {
            for (let i = 0; i < data.rows.length; i++) {
                if ($.isPlainObject(data.rows[i].group)) {
                    for (let key in data.rows[i].group) {
                        data.rows[i].group = key
                    }
                }
            }
            $('#table').bootstrapTable('load', data.rows);
        }
    });
}

//首页table控制
function IndexTable(all) {
    $('#table').bootstrapTable({
        url: '/getServerList/',
        method: 'POST',
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
        showColumns: true, //是否显示所有的列
        toolbar: "#toolbar",
        columns: [{
            checkbox: true,
            visible: true                  //是否显示复选框
        }, {
            field: 'group',
            title: '分类',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
            width: 100,
        }, {
            field: 'project',
            title: '包含项目',
            width: 150,
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
        }, {
            field: 'hostname',
            title: '服务器名',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
            width: 150,
        }, {
            field: 'system',
            title: '系统',
            visible: false,
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
            width: 50,
        }, {
            field: 'ip',
            title: '外网IP',
            width: 100,
            switchable: true,
            sortable: true
        }, {
            field: 'intranet_ip',
            title: '内网IP',
            width: 100,
            align: 'center',
            valign: 'middle',
            switchable: true,
            sortable: true
        }, {
            field: 'user',
            title: '用户名',
            width: 80,
            align: 'center',
            valign: 'middle',
            visible: false,
            switchable: true,
            sortable: true,
        }, {
            field: 'port',
            title: '端口',
            align: 'center',
            valign: 'middle',
            visible: false,
            width: 25,
            switchable: true,
            sortable: true,
        }, {
            field: 'system_info',
            title: '系统版本',
            align: 'center',
            valign: 'middle',
            visible: false,
            width: 25,
            switchable: true,
            sortable: true,
        }, {
            field: 'cpu_count',
            title: 'cpu核心数',
            align: 'center',
            valign: 'middle',
            visible: false,
            width: 25,
            switchable: true,
            sortable: true,
        }, {
            field: 'cpu_info',
            title: 'cpu信息',
            align: 'center',
            visible: false,
            valign: 'middle',
            width: 25,
            switchable: true,
            sortable: true,
        }, {
            field: 'mem_info',
            title: '内存信息',
            align: 'center',
            visible: false,
            valign: 'middle',
            width: 25,
            switchable: true,
            sortable: true,
        }, {
            field: 'hard_info',
            title: '硬盘信息',
            visible: false,
            align: 'center',
            valign: 'middle',
            width: 25,
            switchable: true,
            sortable: true,
        },
            {
                field: 'status',
                title: '状态',
                visible: false,
                align: 'center',
                valign: 'middle',
                width: 25,
                switchable: true,
                sortable: true,
            }, {
                field: 'rep',
                title: '备注',
                align: 'center',
                valign: 'middle',
                switchable: true,
                sortable: true,
            }, {
                field: 'uid',
                title: '操作',
                width: 550,
                align: 'center',
                valign: 'middle',
                switchable: true,
                formatter: actionFormatter,
            }],
        queryParams: function (params) {
            return {
                pageSize: params.limit, //每一页的数据行数，默认是上面设置的10(pageSize)
                pageNumber: params.offset / params.limit + 1, //当前页面,默认是上面设置的1(pageNumber)
                'status': all,
            }
        },
        responseHandler: function (data) {
            let sort = data.sort;
            for (var keys in sort) {
                let group = sort[keys];
                if (group.length === 0) {
                    $("#toolbar .toolbar_ul").append('<li><a href="javascript:void(0);" onclick=\"tt(\'' + keys + '\')\">' + keys + '</a></li>');
                } else {
                    $("#toolbar .toolbar_ul").append('<li class="dropdown">' +
                        '<a class="dropdown-toggle" data-toggle="dropdown" href="javascript:void(0);">' +
                        keys + '<span class="caret"></span></a><ul class="dropdown-menu"></ul></li>');
                    let last = $('.dropdown ul:last');
                    for (let n = 0; n < group.length; n++) {
                        last.append('<li><a href="javascript:void(0);" onclick=\"tt(\'' + keys + "|" + group[n] + '\')\">' + group[n] + '</a></li>');
                    }
                }
            }
            return data.rows; //此处用于对结果进行处理，使分类变成字符串显示
        },
    });
}


//按钮隐藏显示
function radio4() {
    $('#dv1').hide();
    $('#dv2').hide();
    $('#dv3').hide();
    $('#dv4').hide();
    $('#q_btn').hide();
    $('#chengxu').show();
    $('#obj_btn').text('开始部署');
}

//按钮隐藏显示
function radio5() {
    $('#dv1').show();
    $('#dv2').show();
    $('#dv3').show();
    $('#dv4').show();
    $('#q_btn').show();
    $('#chengxu').hide();
    let time = $('#time');
    time.val(CurentTime())
    $('#obj_btn').text('添加定时任务');
}

//获取文件名
function getFileName(file) {//通过第一种方式获取文件名
    var pos = file.lastIndexOf("\\");//查找最后一个\的位置
    return file.substring(pos + 1); //截取最后一个\位置到字符长度，也就是截取文件名
}


//日志控制
function WebSocketLog(uid, obj_uid) {
    if ("WebSocket" in window) {
        // 打开一个 web socket
        // var host = window.location.host;
        var ws = new WebSocket("ws://" + location.hostname + ':' + 8001 + "/logs/");
        ws.onopen = function () {
            // Web Socket 已连接上，使用 send() 方法发送数据
            let message = {'uid': uid, 'obj_uid': obj_uid};
            let messages = JSON.stringify(message);
            ws.send(messages)
        };
        ws.onmessage = function (evt) {
            var received_msg = evt.data;
            $('#logs').append(received_msg);
            document.getElementById('logs').scrollTop = document.getElementById('logs').scrollHeight;
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

//select选择框
function s_clicks(obj) {
    let num = 0;
    for (let i = 0; i < obj.options.length; i++) {
        if (obj.options[i].selected === true) {
            num++;
        }
    }
    if (num === 1) {
        let url = obj.options[obj.selectedIndex].value;
        // window.open(url, '_self’); //这里修改打开连接方式
        let formData = new FormData();
        formData.append("status", url);
        $.ajax({
            type: "post",
            contentType: false,
            processData: false,
            data: formData,
            url: "/getServerList/",
            dataType: "json",
            success: function (data) {
                $('#table').bootstrapTable('load', data.rows);
            }
        });
    }
}

//数据库选择框
function data_clicks(obj) {
    let num = 0;
    for (let i = 0; i < obj.options.length; i++) {
        if (obj.options[i].selected === true) {
            num++;
        }
    }
    if (num === 1) {
        let url = obj.options[obj.selectedIndex].value;
        // window.open(url, '_self’); //这里修改打开连接方式
        let formData = new FormData();
        formData.append("status", url);
        $.ajax({
            type: "post",
            contentType: false,
            processData: false,
            data: formData,
            url: "/showDatabase/",
            dataType: "json",
            success: function (data) {
                $('#table').bootstrapTable('load', data.rows);
            }
        });
    }
}

//备注控制
$(function () {
    var remark = $('#remark_b');
    remark.click(function () {
        if ($('#remark_i').val() === "") {
            $('#remark_s').text("没有输入备注信息，请重新输入");
        } else {
            var uid = $('#uid4').val();
            var rep_uid = $('#uid5').val();
            var remark_i = $('#remark_i').val();
            var formData = new FormData();
            formData.append("remark_i", remark_i);
            formData.append("uid", uid);
            formData.append("rep_uid", rep_uid);
            $.ajax({
                url: "/remark/",
                type: "POST",
                data: formData,
                /**
                 *必须false才会自动加上正确的Content-Type
                 */
                contentType: false,
                /**
                 * 必须false才会避开jQuery对 formdata 的默认处理
                 * XMLHttpRequest会对 formdata 进行正确的处理
                 */
                processData: false,
                success: function (data) {
                    $('#remark_s').text(data.status);
                },
                error: function () {
                    $("#status").text("修改失败！");

                }
            });
        }
    });
});


function Upfile(id, input, status, text, pd) {
    let file_input = $("#" + input + ""); //文件输入框
    let log_out = $("#" + status + ""); //结果日志输出
    let uid = $("#" + id + ""); //服务器uid
    log_out.val("");
    if (pd === 1) {
        var progressbar = log_out; //进度条
    } else {
        var progressbar = $("#progressbar"); //进度条
    }
    if (file_input.val() === "") {
        log_out.text("未选择文件,请先选择文件");
    } else {
        log_out.text("上传中,请勿关闭或刷新界面...");
        let formData = new FormData();
        formData.append("myfile", file_input.get(0).files[0]);
        formData.append("uid", uid.val());
        $.ajax({
            url: "/ufile/",
            type: "post",
            data: formData,
            dataType: 'json',
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
                    if (pd === 0) {
                        progressbar.text('');
                        progressbar.hide();
                    }
                    log_out.text(text);
                    if (pd === 1) {
                        ProjectDep();
                    }

                }
                if (data.status === 0) {
                    if (pd === 0) {
                        progressbar.text('');
                        progressbar.hide();
                    }
                    log_out.text(text);
                }
            },
            error: function () {
                log_out.text("上传失败,请检查网络或者服务器配置");
            }
        });
    }

    function getFileName(file) {//通过第二种方式获取文件名
        var arr = file.split('\\');//通过\分隔字符串，成字符串数组
        return arr[arr.length - 1];//取最后一个，就是文件名
    }


    //进度条
    function progressHandlingFunction(e) {
        progressbar.show();
        let curr = e.loaded;
        let total = e.total;
        let process = curr / total * 100;
        if (process === 100) {
            progressbar.text('文件已上传到代理服务器,正在上传到目标服务器...');
            let fileName = getFileName(file_input.val());
            ProxyProgressLog(fileName)
        } else {
            progressbar.text('当前文件上传进度: ' + parseInt(process) + '%');
        }
    }
}

//部署执行
function ProjectDep() {
    // 如果文件上传成功，则执行部署项目的代码
    let time = $('#time');
    let obj_time = time.val();
    let pd = time.is(':visible'); //判断隐藏的定时任务是否显示
    let formData = new FormData();
    let uid = $('#uid3').val(); //服务器uid
    let obj_uid = $('#select').val();//项目uid
    let qname = $('#qname').val();
    if (pd) {
        formData.append("obj_time", obj_time);
        formData.append("time_status", "1");
    } else {
        formData.append("time_status", "0");
    }
    formData.append("uid", uid);
    formData.append("qname", qname);
    formData.append("obj_uid", obj_uid);
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
            } else if (data.result === "sradio5erver_error") {
                $("#log").text("服务器错误！");
            } else {
                $("#log").text(data.result);

                WebSocketLog(uid, obj_uid);
            }
        },
        error: function () {
            $("#log").text("上传失败,请检查网络或者服务器配置");
        }
    });
}

//代理服务器上传进度
function ProxyProgressLog(filename) {
    if ("WebSocket" in window) {
        // 打开一个 web socket
        // var host = window.location.host;
        var ws = new WebSocket("ws://" + location.hostname + ':' + 8001 + "/proxyprogresslog/");
        ws.onopen = function () {
            // Web Socket 已连接上，使用 send() 方法发送数据
            let message = {'filename': filename};
            let messages = JSON.stringify(message);
            ws.send(messages)
        };
        ws.onmessage = function (evt) {
            var received_msg = evt.data;
            if (received_msg === 'success') {
                $('#log').val('#### 文件上传成功！开始执行项目部署脚本 ####\n\n');
            } else {
                $('#log').val('文件从到代理服务器-->>目标服务器' + received_msg);
            }
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

//文件上传
$(function () {
    $('#upbutton').click(function () {
        Upfile("up_uid", "up", "status", "上传成功！服务器中执行cd可查看已上传文件", 0);
    })
});
//下载文件
$(function () {
    var file_path = $('#file_path');
    var download = $('#download');
    download.click(function () {
        var path = file_path.val();
        var uid = $('#uid').val();
        $.ajax(
            {
                url: '/down_handler/',
                data: {'path': path, 'uid': uid},
                type: 'post',
                dataType: 'json',
                async: 'true',
                success: function (data, status, xhr) {
                    console.log('成功');
                    console.log(data);
                    console.log(status)
                },
                error: function (xhr, status, error) {
                    console.log('失败');
                    console.log(error);
                    console.log(status)
                }
            }
        )
    });
});

//部署程序
$(function () {
    let obj_btn = $('#obj_btn');
    obj_btn.click(function () {
        if (confirm("确定要部署吗？，部署前请仔细确认模板是否选择正确")) {
            Upfile("uid3", "obj_up", "log", "代码文件上传成功！正在执行部署模板...", 1);
        }
    });
});


//窗口消失后事件控制
$(function () {
    $('#myModal4').on('hide.bs.modal', function () {
        location.reload();
    });
    $('#myModal3').on('hide.bs.modal', function () {
        location.reload();
    });
    $('#pModal').on('hide.bs.modal', function () {
        location.reload();
    });
    $('#pModal').on('show.bs.modal', function () {
        toastr.options.positionClass = 'toast-top-center';
        let row = $('#table').bootstrapTable('getSelections');
        if (row.length < 1) {
            toastr.error("未选择节点，请选择节点");
        }
    })

});

//批量修改
$('#operation').change(function () {
    let res = $(this).children('option:selected').val();
    if (res === "sort") {
        $('#selects').show();
        $('#sys_select').hide();
        $('#sname').text('分组名称:');
        $('#pro_select').attr('style', 'display: none');
        $('#itext').attr('type', 'hidden');
    }
    if (res === "system") {
        $('#selects').hide();
        $('#sys_select').show();
        $('#sname').text('系统名称:');
        $('#pro_select').attr('style', 'display: none');
        $('#itext').attr('type', 'hidden');
    }
    if (res === "port") {
        $('#selects').hide();
        $('#sys_select').hide();
        $('#sname').text('新的端口:');
        $('#pro_select').attr('style', 'display: none');
        $('#itext').attr('type', 'text');
        $('#itext').attr('style', 'width:150px');

    }
    if (res === "project") {
        $('#selects').hide();
        $('#sys_select').hide();
        $('#itext').hide();
        $('#pro_select').attr('type', 'text');
        $('#pro_select').attr('style', 'width:150px');

    }
});

//批量修改保存
$('#batch_save').click(function () {
    let action = $('#operation').children('option:selected').val();
    let formData = new FormData();
    let row = $('#table').bootstrapTable('getSelections');
    if (row.length < 1) {
        toastr.error("未选择节点，请选择节点");
        return;
    }
    let arr = [];
    for (let i = 0; i < row.length; i++) {
        arr.push(row[i].uid);
    }
    formData.append("arr", arr);
    formData.append("action", action);
    if (action === 'sort') {
        let data = $('#selects').children('option:selected').val();
        formData.append("data", data);
    }
    if (action === 'system') {
        let data = $('#sys_select').children('option:selected').val();
        formData.append('data', data);
    }
    if (action === 'port') {
        let data = $('#itext').val();
        formData.append('data', data);
    }
    if (action === 'project') {
        let data = $('#pro_select').val();
        formData.append('data', data);
    }
    $.ajax({
        type: "post",
        contentType: false,
        processData: false,
        data: formData,
        url: "/batch_edit/",
        dataType: "json",
        success: function (data) {
            if (data.status === "修改失败") {
                toastr.error(data.status);
            } else {
                toastr.success(data.status);
            }
        }
    });
});