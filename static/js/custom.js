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
    result += '<button onclick=window.open("/webssh/' + id + '") style="color:#fff;background-color:#28c210;border-color:#28c210;border-style:solid">web连接</button> ';
    result += '<button onclick=window.location.href="/xshell/' + id + '" style="color:#fff;background-color:#2caef5;border-color:#2caef5;border-style:solid">Xshell连接</button> ';
    result += '<button onclick=window.location.href="/xftp/' + id + '" style="color:#fff;background-color:#1a4c67;border-color:#1a4c67;border-style:solid">Xftp上传</button> ';

    result += '<button onclick=document.getElementById("uid2").value=' + id + ';document.getElementById("myModalLabel").innerText="服务器:' + rows + '"' +
        ' style="color:#fff;background-color:#1278e2;border-color:#1278e2;border-style:solid" data-toggle="modal" data-target="#myModal">在线上传</button> ';

    result += '<button onclick=document.getElementById("uid3").value=' + id + ';document.getElementById("myModalLabel3").innerText="服务器:' + rows + '"' +
        ' style="color:#fff;background-color:#672ade;border-color:#672ade;border-style:solid" data-toggle="modal"  data-target="#myModal3">项目部署</button> ';

    result += '<button onclick=document.getElementById("uid4").value=' + id + ';document.getElementById("uid5").value="' + repUid + '";document.getElementById("myModalLabel4").innerText="服务器:' + rows + '"' +
        ' style="color:#fff;background-color:#8a6d3b;border-color:#8a6d3b;border-style:solid" data-toggle="modal"  data-target="#myModal4">备注</button> ';
    if (auth === 1) {
        result += '<button onclick=window.location.href="/update/' + id + '" style="color:#fff;background-color:#409eff;border-color:#409eff;border-style:solid">修改</button> ';
        result += '<button onclick=\'if (confirm("确定要删除吗？")) {window.location.href="/del/' + id + '"}\' style="color:#fff;background-color:#c20003;border-color:#c20006;border-style:solid">删除</button>';
    }
    return result;

}

function tt(url) {
    let formData = new FormData();
    formData.append("status", url);

    var elements = document.querySelectorAll('.nav.nav-tabs li');
    //数组是of,对象是in
    for (let item of elements) {
        item.className = ''
    }

    let obj = event.srcElement.parentNode;
    obj.setAttribute("class", "active");
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
        singleSelect: true,
        clickToSelect: true,
        sortName: "create_time",
        sortOrder: "desc",
        pageList: "[10, 25, 50, 100, All]",
        search: true,
        showColumns: true, //是否显示所有的列
        toolbar: "#toolbar",
        columns: [{
            field: 'user_group',
            title: '分类',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
            width: 100,
        }, {
            field: 'hostname',
            title: '服务器名',
            switchable: true,
            sortable: true,
            align: 'center',
            valign: 'middle',
            width: 250,
        }, {
            field: 'system',
            title: '系统',
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
            switchable: true,
            sortable: true,
        }, {
            field: 'port',
            title: '端口',
            align: 'center',
            valign: 'middle',
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
            for (var i = 0; i < data.sort.length; i++) {
                var group = data.sort[i];
                $("#toolbar ul").append('<li><a href="javascript:void(0);" onclick=\"tt(\'' + group + '\')\">' + group + '</a></li>');
            }
            return data.rows;
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
    $('#obj_btn').text('开始部署');
}

//按钮隐藏显示
function radio5() {
    $('#dv1').show();
    $('#dv2').show();
    $('#dv3').show();
    $('#dv4').show();
    $('#q_btn').show();
    time.val(CurentTime())
    $('#obj_btn').text('添加定时任务');
}

//获取文件名
function getFileName(file) {//通过第一种方式获取文件名
    var pos = file.lastIndexOf("\\");//查找最后一个\的位置
    return file.substring(pos + 1); //截取最后一个\位置到字符长度，也就是截取文件名
}

//当前主机识别
function host() {
    var host = window.location.host;
    return host.replace(/8000/, "8001")
}

//日志控制
function WebSocketLog(uid, obj_uid) {
    if ("WebSocket" in window) {
        // 打开一个 web socket
        // var host = window.location.host;
        var ws = new WebSocket("ws://" + location.hostname + ':' + 8003 + "/logs/");
        ws.onopen = function () {

            // Web Socket 已连接上，使用 send() 方法发送数据
            ws.send(uid + '|' + obj_uid)
        };
        ws.onmessage = function (evt) {
            var received_msg = evt.data;
            $('#log').append(received_msg);
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
//文件上传
$(function () {
    var ufile = $('#upbutton');
    ufile.click(function () {
        if ($("#up").val() === "") {
            $("#status").text("未选择文件,请先选择文件");
        } else {
            $("#status").text("上传中,请勿关闭或刷新界面...");
            var formData = new FormData();
            formData.append("myfile", document.getElementById("up").files[0]);
            $.ajax({
                url: "http://" + host() + "/Upload/",
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
                        var uid = $('#uid2').val();
                        var formData2 = new FormData();
                        var uploadfile = $("#up").val();
                        formData2.append("uid", uid);
                        formData2.append("path", getFileName(uploadfile));
                        $.ajax({
                            url: "/ufile/",
                            type: "post",
                            contentType: false,
                            processData: false,
                            dataType: 'json',
                            data: formData2,
                            success: function (data) {
                                if (data.status === "true") {
                                    $("#status").text("上传成功！服务器中执行cd可查看已上传文件");
                                    $("#progressbar").text('');
                                    $("#progressbar").hide();
                                } else {
                                    $("#status").text("上传失败！");
                                    $("#progressbar").text('');
                                    $("#progressbar").hide();
                                }
                            },
                            error: function () {
                                $("#status").text("上传失败！");

                            }
                        });
                    }
                    if (data.status === 0) {
                        $("#status").text("未选择文件,请先选择文件");
                        $("#progressbar").text('');
                        $("#progressbar").hide();
                    }
                },
                error: function () {
                    $("#status").text("上传失败！");

                }
            });

            function progressHandlingFunction(e) {
                var curr = e.loaded;
                var total = e.total;
                process = curr / total * 100;
                $("#progressbar").show();
                if (process === 100) {
                    $("#progressbar").text('文件已上传到代理服务器,正在上传到目标服务器...');
                } else {
                    $("#progressbar").text('当前文件上传进度: ' + parseInt(process) + '%');
                }
            }


        }
    });
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
//部署执行
$(function () {
    var time = $('#time');
    var obj_btn = $('#obj_btn');
    obj_btn.click(function () {
        if (confirm("确定要部署吗？，部署前请仔细确认模板是否选择正确"))
            if ($("#obj_up").val() === "") {
                $('#log').text("未选择文件,请先选择文件");
            } else {
                $('#log').text("文件上传中...");
                var uid = $('#uid3').val(); //服务器uid
                var obj_uid = $('#select').val();//项目uid
                var qname = $('#qname').val();
                var formData = new FormData();
                var uploadfile = $("#obj_up").val();
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
                    url: "http://" + host() + "/Upload/",
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
        } else {
            $("#log").text('当前文件上传进度: ' + parseInt(process) + '%');
        }
    }
});
//窗口消失后事件控制
$(function () {
    $('#myModal4').on('hide.bs.modal', function () {
        location.reload();
    });
    $('#myModal3').on('hide.bs.modal', function () {
        location.reload();
    })

});


