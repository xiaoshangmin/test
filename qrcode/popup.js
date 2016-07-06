$(function(){   
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	var url = encodeURI(tabs[0].url);
	var finalurl = 'https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl='+url+'&chld=L|1&choe=UTF-8';
	$("img").attr("src",finalurl);
	});
 
});
