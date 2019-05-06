var lastValue = "", nodeList = [], fontCss = {},hiddenNodes=[];

function focusKey(e) {  
    if (key.hasClass("empty")) {  
        key.removeClass("empty");  
    }  
}  
function blurKey(e) {  
    if (key.get(0).value === "") {  
        key.addClass("empty");  
    }  
}  
//搜索节点  
function searchNode(e) {  
    var zTree = $.fn.zTree.getZTreeObj("tree");  
    var value = $.trim(key.get(0).value);  
    var keyType = "name";  
  
    if (key.hasClass("empty")) {  
        value = "";  
    }  
    
     //显示上次搜索后背隐藏的结点
    zTree.showNodes(hiddenNodes);
    //查找不符合条件的叶子节点
    function filterFunc(node){
        var _keywords=$("#key").val();
        if(node.isParent||node.name.indexOf(_keywords)!=-1) return false;
        return true;        
    };
    //获取不符合条件的叶子结点
    hiddenNodes=zTree.getNodesByFilter(filterFunc);
    //隐藏不符合条件的叶子结点
    zTree.hideNodes(hiddenNodes);
    
    if (lastValue === value) return;  
    lastValue = value;  
    if (value === ""){  
        updateNodes(false);  
        return;  
    }; 
    updateNodes(false);
    nodeList = zTree.getNodesByParamFuzzy(keyType, value); //调用ztree的模糊查询功能，得到符合条件的节点  
    updateNodes(true); //更新节点  
    
}  

//高亮显示被搜索到的节点  
function updateNodes(highlight) {  
    var zTree = $.fn.zTree.getZTreeObj("tree");  
    for( var i=0, l=nodeList.length; i<l; i++) {  
        nodeList[i].highlight = highlight; //高亮显示搜索到的节点(highlight是自己设置的一个属性)  
        zTree.expandNode(nodeList[i].getParentNode(), true, false, false); //将搜索到的节点的父节点展开  
        zTree.updateNode(nodeList[i]); //更新节点数据，主要用于该节点显示属性的更新  
    }  
}  

//设置颜色  
function setFontCss(treeId, treeNode) {  
    return (!!treeNode.highlight) ? {color:"#ff101b", "font-weight":"bold"} : {color:"#333", "font-weight":"normal"};
}  
