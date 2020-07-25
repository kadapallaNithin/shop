//sort_links,page, order_by, order are to be set by page that includes this script
var gTable = document.getElementsByTagName('table')[0];
var headCells = gTable.tHead.rows[0].cells;
for (var i = headCells.length - 1; i >= 0; i--) {
    var anchor = document.createElement("a");
    anchor.href = "?page="+page+"&order_by="+sort_links[i]+"&order=";
    if(order_by == sort_links[i]){
        if(order == 'asc'){
            anchor.href += "desc";
        }else{
            anchor.href += "asc"
        }
    }else{
        anchor.href += "asc";
    }
    anchor.appendChild(headCells[i].firstChild);
    headCells[i].appendChild(anchor);
//    headCells[i].addEventListener("click", rowAction(i), true);
}
