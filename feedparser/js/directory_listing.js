var EVEN_COLOR = "#fff";
var ODD_COLOR =  "#eee";

function prettyDirectoryListing() {
  if (!document.getElementsByTagName) return;
  tables = document.getElementsByTagName("table");
  for (i = 0; i < tables.length; i++) {
    table = tables[i];
    addHeaderTitles(table);
    addRowStripes(table);
  }
}

function addHeaderTitles(table) {
  ths = table.getElementsByTagName("th");
  for (i = 0; i < ths.length; i++) {
    links = ths[i].getElementsByTagName("a");
    for (j = 0; j < links.length; j++) {
      links[j].title = "Sort by " + links[j].firstChild.data.toLowerCase();
    }
  }
}

function addRowStripes(table) {
  even = false;
  trs = table.getElementsByTagName("tr");
  // 1-based because we're skipping the header row
  for (i = 1; i < trs.length; i++) {
    trs[i].onmouseover = function() { this.className = 'ruled'; return false }
    trs[i].onmouseout = function() { this.className = ''; return false }
    trs[i].style.backgroundColor = even ? EVEN_COLOR : ODD_COLOR;
    even = ! even;
  }
}

// very loosely based on http://www.alistapart.com/articles/zebratables/
// also http://www.alistapart.com/articles/tableruler/
