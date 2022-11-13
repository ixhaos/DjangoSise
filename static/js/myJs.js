function ChangeNavigationColor(){
     var href = window.location.href;
     var page = href.split("/");
     var oAStyle = document.getElementsByClassName("navbar-nav")[0].getElementsByTagName("li");
     if(page[page.length-1]==""){
         oAStyle[0].className = "active";
     }
     else {
         var web = page[page.length - 1].split(".")[0];
         for (var i = 0; i < oAStyle.length; i++) {
             var oPage = oAStyle[i].getElementsByTagName("a")[0].href.split("/");
             var oWeb = oPage[oPage.length - 1].split(".")[0];
             if (web == oWeb) {
                 oAStyle[0].className = "";
                 oAStyle[i].className = "active";
             }
         }
     }
}