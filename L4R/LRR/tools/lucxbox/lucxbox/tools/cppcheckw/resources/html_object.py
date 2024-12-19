

HTML_HEAD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Cppcheck - HTML report</title>
    <link rel="stylesheet" href="style.css">
    <style>
%s
    </style>
    <script language="javascript">
      function getStyle(el,styleProp) {
        if (el.currentStyle)
          var y = el.currentStyle[styleProp];
        else if (window.getComputedStyle)
          var y = document.defaultView.getComputedStyle(el,null).getPropertyValue(styleProp);
        return y;
      }
      function setBorders() {
        var screenWidth = document.getElementById("menu").parentElement.clientWidth
        var headerHeight = document.getElementById("header").clientHeight;
        var menuWidth = document.getElementById("menu").clientWidth;
        document.getElementById("menu").style.marginTop=`${headerHeight+1}px`;
        document.getElementById("content").style.marginTop=`${headerHeight+1}px`;
        document.getElementById("content").style.marginLeft=`${Math.ceil((menuWidth/screenWidth)*100)}%%+10px`;
      }
      function toggle() {
        var el = this.expandable_content;
        var mark = this.expandable_marker;
        if (el.style.display == "block") {
          el.style.display = "none";
          mark.innerHTML = "[+]";
        } else {
          el.style.display = "block";
          mark.innerHTML = "[-]";
        }
      }
      function init_expandables() {
        var elts = document.getElementsByClassName("expandable");
        for (var i = 0; i < elts.length; i++) {
          var el = elts[i];
          var clickable = el.getElementsByTagName("span")[0];
          var marker = clickable.getElementsByClassName("marker")[0];
          var content = el.getElementsByClassName("content")[0];
          var width = clickable.clientWidth - parseInt(getStyle(content, "padding-left")) - 
          parseInt(getStyle(content, "padding-right")); 
          content.style.width = width + "px";
          clickable.expandable_content = content;
          clickable.expandable_marker = marker;
          clickable.onclick = toggle;
        }
      }
      function set_class_display(c, st) {
        var elements = document.querySelectorAll('.' + c),
            len = elements.length;
        for (i = 0; i < len; i++) {
            elements[i].style.display = st;
        }
      }
      function toggle_class_visibility(id) {
        var box = document.getElementById(id);
        set_class_display(id, box.checked ? '' : 'none');
        update_show_all();
      }
      function show_all(condition){
        var elts = document.getElementsByTagName("input");
        for (var i = 1; i < elts.length; i++) {           
          var el = elts[i];
          // el.checked ? el.checked=false : el.checked=true;
          el.checked = condition;
          toggle_class_visibility(el.id);        
        } 
      }
      function update_show_all(){
        var elts = document.getElementsByTagName("input");
        var show_all_checked = true;
        for (var i = 1; i < elts.length; i++) {  
          if (!(elts[i].checked)) {
            show_all_checked=false;
          }
        }
        var show_all_box = document.getElementById("show_all");
        show_all_box.checked = show_all_checked;
      }

    </script>
  </head>
  <body onload="init_expandables(); setBorders()">
      <div class="header" id="header">
        <h1>Cppcheck report: %s </h1>
      </div>
      <div id="main_body">
      <div class="menu" id="menu">
       <p id="filename"><a href="_index.html">Back to Summary:</a></p>
"""

HTML_HEAD_END_TEMPLATE = """
      </div>
      <div class="main" id="content">
"""

HTML_FOOTER_TEMPLATE = """
      </div>
      </div>
      <div class="footer" id="footer">
        <p>
         Cppcheck %s - a tool for static C/C++ code analysis</br>
         </br>
         Internet: <a href="http://cppcheck.net">http://cppcheck.net</a></br>
         IRC: <a href="irc://irc.freenode.net/cppcheck">irc://irc.freenode.net/cppcheck</a></br>
        <p>
      </div>
  </body>
</html>
"""

HTML_ERROR_TEMPLATE = '<span class="%s" title="%s%s">&lt;--- %s</span>\n'
