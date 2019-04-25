// window.onload = () => {
//     var div2 = document.getElementById("div2");
//     var div1 = document.getElementById("div1");
//     var flag = true;
//
//     div1.addEventListener('click', () => {
//         if (flag) {
//             div2.style.position = 'absolute';
//
//             div1.className = (div1.className == "close1") ? "open1" : "close1";
//             div2.className = (div2.className == "close2") ? "open2" : "close2";
//             // document.getElementById("his").style.display="none";
//             // document.getElementById("his2").style.display="none";
//
//         } else {
//             div2.style.position = 'relative';
//
//             div1.className = (div1.className == "close1") ? "open1" : "close1";
//             div2.className = (div2.className == "close2") ? "open2" : "close2";
//             // document.getElementById("his").style.display="inline";
//             // document.getElementById("his2").style.display="inline";
//         }
//         flag = !flag
//     }, false)
// };
//
function s_click(obj) {
    var num = 0;
    for (var i = 0; i < obj.options.length; i++) {
        if (obj.options[i].selected == true) {
            num++;
        }
    }
    if (num == 1) {
        var url = obj.options[obj.selectedIndex].value;
        // window.open(url, '_self’); //这里修改打开连接方式
        window.location.href = url
    }
}

