function popupImage(url){
    var img = new Image();
    var scWidth = screen.availWidth; //현재 사용중인 스크린 크기를 구함
    var scHeight = screen.availHeight;
    var left = (parseInt(scWidth)-650)/2; //팝업창 위치 조절
    var top = (parseInt(scHeight)-900)/2;
    img.src = url;
    var img_width = img.width-500; //팝업창 크기 조절
    var win_width = img.width-500;
    var height = img.height-290;
    var openImage = 
    window.open('','_blank','width='+img_width+',height='+height+',top='+top+',left='+left+',menubars=no,scrollbars=auto');
    openImage.document.write("<style>body{margin:0px;}</style><a href = # onclick = window.close() onfocus=this.blur()><img src = '"+url+"'width='"+win_width+"'></a>");
  }