// getting the index number of the "GPU utilization (only taken)" column
var table = document.getElementsByClassName("mdc-data-table__table")[0];

indexNumber = 0
for (var i = 0; i < table.rows[0].children.length; i ++){
    if (table.rows[0].children[i].textContent == "GPU utilization (only taken)"){
        indexNumber = i;
        break;
    }
}

for (var i = 1; i < table.rows.length; i++) {  // going through each row
    var cell = table.rows[i].cells[indexNumber];
    assignTextColor(cell, 30.0, 70.0, "green", "red");
  }

/**
 * Changes the color of the td cell's text given the threshold cutoffs
 * @param {td} cell the cell with the text whose color might be changed
 * @param {float} low anything <= this is lowColor, float between 0 and 100
 * @param {float} high anything >= this is highColor, float between 0 and 100
 * @param {string} lowColor red
 * @param {string} highColor green
 */
function assignTextColor(cell, low, high, lowColor, highColor){
    var num = parseFloat(cell.textContent) 

    if (num <= low){
        cell.style.color = lowColor;
    }
    else if (num >= high){
        cell.style.color = highColor;
    }


}
