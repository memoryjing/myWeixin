window.onload=function(){
	
	var allInput=document.getElementsByTagName("input");
	var oName=allInput[0];
	var teleNumber=allInput[1];
	var goodsName=allInput[2];
	var count=allInput[3];
	var allP=document.getElementsByTagName("p");
	var name_msg=allP[0];
	var count=document.getElementById("count")
	//汉字。10-50个以内字符，使用中文
	// 中文 \u4e00-\u9fa5 unicode编码的中文字符
	var re=/[^\u4e00-\u9fa5]/g;//匹配所有非汉字，给用户发出警告
	var name_length=0;
	
	
	//姓名
	oName.onfocus=function(){
		name_msg.style.display="block";
		name_msg.innerHTML='<i class="ati"></li>汉字。10-50个以内字符，使用中文';
	}
	oName.onkeyup=function(){
		count.style.visibility="visible";
		name_length=getLength(this.value)
		count.innerHTML=name_length+"个字符";
	}
	oName.onblur=function(){
		
	}
	
	
	
	
	
	
	
	function getLength(str){
		//匹配双字节的，替换为xx，就可以计算长度
		return str.replace(/[^\x00-\xff]/g,"xx").length;
	}
}