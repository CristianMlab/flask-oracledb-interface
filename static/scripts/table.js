function isNumber(value) 
{
   return !Number.isNaN(Number(value));
}

function compare(x, y){
    var numberCompare = isNumber(x) && isNumber(y);
    if(x=="None")x="zzzzzzz";
    if(y=="None")y="zzzzzzz";
    if(numberCompare){
      return Number(x) > Number(y);
    } else {
      return x > y;
    }
}

function revcompare(x, y){
  var numberCompare = isNumber(x) && isNumber(y);
  if(x=="None")x="0";
  if(y=="None")y="0";
  if(numberCompare){
    return Number(x) < Number(y);
  } else {
    return x < y;
  }
}

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("table");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (compare(x.innerHTML, y.innerHTML)) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (revcompare(x.innerHTML, y.innerHTML)) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

function edit(){
  var x = document.getElementsByClassName("tableInput");
  var y = document.getElementsByClassName("tableElement");
  var b = document.getElementById("submit-edit");
  var input = "";
  var element = "";
  console.log(x[0].style.display);
  if(x[0].style.display == "none" || x[0].style.display == ""){
    input = "block";
    element = "none";
  } else {
    input = "none";
    element = "block";
  }
  b.style.display = input;
  for(var i = 0; i < x.length; i++){
    x[i].style.display = input;
  }
  for(var i = 0; i < y.length; i++){
    y[i].style.display = element;
  }
}