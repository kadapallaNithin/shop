var gTable, gOrderBy, gTBody, gRows, whole_data, sort_switch;//, gUI_showHidden;
sort_switch = document.getElementById('sort_switch');
sort_switch.innerHTML = '<span class="switch"><label><input type="checkbox" id="whole_data" onchange="update_sort_info();" /><span class="lever"></span>Sort <span id="sort_info">this page </span></label></span>';
whole_data = document.getElementById('whole_data');
update_sort_info();
function update_sort_info(){
  var sort_info = document.getElementById('sort_info');
  if(whole_data.checked){
    alert('this is under development');
    sort_info.innerHTML = 'whole data <div></div> <span class="switch"><label><input type="checkbox" id="order_by" onchange="update_order_by();" /><span class="lever"></span><span id="order_by_message">Ascending</span></label></span>';
  }else{
    sort_info.innerHTML = "this page data only";
  }
}
function update_order_by(){
  var order_by = document.getElementById('order_by');
  var order_by_message = document.getElementById('order_by_message');
  if(order_by.checked){
    order_by_message.innerHTML = "Descending";
  }else{
    order_by_message.innerHTML = "Ascending";
  }
}
document.addEventListener("DOMContentLoaded", function() {
  gTable = document.getElementsByTagName("table")[0];
  gTBody = gTable.tBodies[0];
  if (gTBody.rows.length < 2){
    sort_switch.innerHTML = "";//"Need not sort :)";
    return;
  }
  //gUI_showHidden = document.getElementById("UI_showHidden");
  var headCells = gTable.tHead.rows[0].cells,
      hiddenObjects = false;
  function rowAction(i) {
    return function(event) {
      event.preventDefault();
      if(whole_data.checked){
        var order_by_param = "asc";
        if(order_by.checked){
          order_by_param = "desc";
        }
        window.location.assign("?sort_by="+sort_links[i]+"&order_by="+order_by_param);
      }
      orderBy(i);
    }
  }
  for (var i = headCells.length - 1; i >= 0; i--) {
    var anchor = document.createElement("a");
    anchor.href = "";
    anchor.appendChild(headCells[i].firstChild);
    headCells[i].appendChild(anchor);
    headCells[i].addEventListener("click", rowAction(i), true);
  }
  // if (gUI_showHidden) {
  //   gRows = Array.from(gTBody.rows);
  //   hiddenObjects = gRows.some(row => row.className == "hidden-object");
  // }
  gTable.setAttribute("order", "");
  // if (hiddenObjects) {
  //   gUI_showHidden.style.display = "block";
  //   updateHidden();
  // }
}, "false");
function compareRows(rowA, rowB) {
  var a = rowA.cells[gOrderBy].getAttribute("sortable-data") || "";
  var b = rowB.cells[gOrderBy].getAttribute("sortable-data") || "";
  var intA = +a;
  var intB = +b;
  if (a == intA && b == intB) {
    a = intA;
    b = intB;
  } else {
    a = a.toLowerCase();
    b = b.toLowerCase();
  }
  if (a < b)
    return -1;
  if (a > b)
    return 1;
  return 0;
}
function orderBy(column) {
  if (!gRows)
    gRows = Array.from(gTBody.rows);
  var order;
  if (gOrderBy == column) {
    order = gTable.getAttribute("order") == "asc" ? "desc" : "asc";
  } else {
    order = "asc";
    gOrderBy = column;
    gTable.setAttribute("order-by", column);
    gRows.sort(compareRows);
  }
  gTable.removeChild(gTBody);
  gTable.setAttribute("order", order);
  if (order == "asc")
    for (var i = 0; i < gRows.length; i++)
      gTBody.appendChild(gRows[i]);
  else
    for (var i = gRows.length - 1; i >= 0; i--)
      gTBody.appendChild(gRows[i]);
  gTable.appendChild(gTBody);
}
// function updateHidden() {
//   gTable.className = gUI_showHidden.getElementsByTagName("input")[0].checked ?
//                      "" :
//                      "remove-hidden";
// }
// (function (){
// })();