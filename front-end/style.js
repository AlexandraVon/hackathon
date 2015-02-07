var home = "http://160.39.234.210:5000";
var bgcount = 1;
$( document ).ready(function() {
    bgcount = 1;
});

function login(){
	var URL = home+"/login";
	// var data = '{"login" : "true"}';
		$.ajax({
			type: 'GET',
			url: URL,
			dataType:"json",
			contentType: "application/json; charset=utf-8",
			success: function(data, textStats, XMLHttpRequest){
				console.log(data);
				var user = data.user;
				var exist = user.exist;
				var user_id = user.user_id;
				var user_name = user.user_name;
				var headline = user.headline;
				var email = user.email;
				var linkedin_add = user.linkedin_add;
				var company = user.company;
				var photo_url = user.photo_url;
				if (exist){
					var friend = data.friend;
					var friend_id = friend.content.friend_id;
					var friend_photo = friend.content.friend_photo;
					var template_id = user.template_id;

				}else{
					$.mobile.changePage('#non_existed_user');
					$("#welcom_head").append("<h2>"+user_name+"'s Card</h2>");
					$("#non_existed_user").append("<img class=\"cardbg\" id=\"cardimg\" src=\"img/temp"+bgcount+".jpg\">");
					$("#non_existed_user").append("<a href=\"#choose\" data-role=\"button\" data-icon=\"search\" data-icon=\"check\" onclick=\"choosecard("+bgcount+","+user_name+","+headline+","+photo_url+")\"></a>")
				}
			}
		});
}

$(document).on("pageinit","#welcom_head",function(){
  $("#cardimg").on("swipe",function(){
  	if(bgcount==6){bgcount=1;}else{bgcount+=1;}
    $("cardimg").attr("src","img/bg"+bgcount+".jpg");
  });                       
});

function choosecard(bgcount,name,headline,photo_url){
	if(bgcount!=3 && bgcount!=5){
		$("#choose").append("<div class=\"words"+bgcount+"\"><h3 class=\"name"+bgcount+"\">"+name+"</h3><p class=\"headline"+bgcount+"\">"+headline+"</p></div><img src=\""+photo_url+"\" class=\"card\">");
	}else{
		$("#choose").append("<img src=\""+photo_url+"\" class=\"photo"+bgcount+"\"><div class=\"words"+bgcount+"\"><h3 class=\"name"+bgcount+"\">"+name+"</h3><p class=\"headline"+bgcount+"\">"+headline+"</p></div><img src=\""+photo_url+"\" class=\"card\">");
	}
}

