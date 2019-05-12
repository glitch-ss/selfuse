$(document).ready(function(){
	$('#search button').click(function(){
	valstr=$('#search input').val()
	$.ajax({
		    async: false,
		    type: "POST",
		    url: '/innerexpress',
		    data: {"date": valstr},
		    dataType: "json",
		    error: function () { console('err') },
		    success: function (data) {
		        $('.name_list').html("")
				console.log(data)
				name_list = data['name_list']
				console.log(name_list)
				for (i in name_list){
					cmd = "<tr><td>"+name_list[i][0]+"</td><td>"+name_list[i][1]+"</td></tr>"
					$('.name_list').append(cmd)
				}
		    },
			complete: function () { console.log('test') },
		})
})
})