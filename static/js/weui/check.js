window.onload=function(){
	
	var allInput=document.getElementsByTagName("input");
	var oName=allInput[0];
	var pwd=allInput[1];
	var confirm=allInput[2];

	
	var allP=document.getElementsByTagName("p");
	var name_msg=allP[0];
	var pwd_msg=allP[1];
	var confirm_msg=allP[2];
	var name_count=document.getElementById("count_name")
	//汉字。10-50个以内字符，使用中文
	// 中文 \u4e00-\u9fa5 unicode编码的中文字符
	//匹配所有非汉字，给用户发出警告
	var name_length=0;
	
	
	//姓名的校验工作
	oName.onfocus=function(){
		name_msg.style.display="block";
		name_msg.innerHTML='<i class="ati"></i>汉字。10-50个以内字符，使用中文';
	}
	oName.onkeyup=function(){
		name_count.style.visibility="visiable";
		name_length=getLength(this.value)
		name_count.innerHTML=name_length+"个字符";
		if(name_length==0){
			name_count.style.visibility="hidden";
		}
	}
	//鼠标离开input框操作
	oName.onblur=function(){
		//含有非法字符
		var re=/[^\w\u4e00-\u9fa5]/g;
		if(re.test(this.value)){
			name_msg.innerHTML='<i class="err"></i>含有非法字符';
		}
		//不能为空
		else if(this.value==""){
			name_msg.innerHTML='<i class="err"></i>不能为空';
		}
		
		//长度在10-50字符之内
		else if(name_length>50 || name_length<10){
			name_msg.innerHTML='<i class="err"></i>长度不符合要求';
		}
		else{
			name_msg.innerHTML='<i class="ok"></i>符合要求';
		}
		
	}
	
	function getLength(str){
		//匹配双字节的，替换为xx，就可以计算长度
		return str.replace(/[^\x00-\xff]/g,"xx").length;
	}
	//密码验证区
	pwd.onfocus=function(){
		pwd_msg.style.display="block";
		pwd_msg.innerHTML='<i class="err"></i>字母数字组合6-12位，不能单独使用字母或者数字';
	}
	pwd.onkeyup=function(){
		if(this.value.length>5){
			confirm.removeAttribute("disabled");
			confirm_msg.style.display="block";
			confirm_msg.innerHTML="再次输入密码";
		}
		else{
			confirm.setAttribute("disabled");
			confirm_msg.style.display="none";
		}
	}
	pwd.onblur=function(){
		
	}
	//确认密码验证区
	//字母数字组合6-12位
	confirm.onfocus=function(){
		
		
	}
	confirm.onkeyup=function(){
		
	}
	confirm.onblur=function(){
		
	}
	
	
	
	
	
	
	
	
	
	
	
	
}