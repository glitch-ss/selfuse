$(document).ready(function(){
	$('#search button').click(function(){
	valstr=$('#search input').val()
	$.ajax({
		    async: false,
		    type: "POST",
		    url: '/mk',
		    data: {"url": valstr},
		    dataType: "json",
		    error: function () { console.log('err') },
		    success: function (data) {
		        $('.inspect_list').html("")
				console.log(data)
				inspect_list = data['inspect_list']
				console.log(inspect_list[0])
				for (i in inspect_list){
					alert(inspect_list[i])
					cmd = "<tr id='" + i +"'><td>"+i+"</td><td>"+inspect_list[i]+"</td><td><button class='delete'>delete</button></td></tr>"
					console.log(cmd)
					$('.inspect_list').append(cmd)
				}
		    },
			complete: function () { },
		})
	})
	$('.delete').click(function(){
		tr=$(this).parent().parent()
		id = $(tr).attr('id')
		$.ajax({
		    async: false,
		    type: "POST",
		    url: '/stop',
		    data: {"key": id},
		    dataType: "json",
		    error: function () { console.log('err') },
		    success: function(){
				console.log($(tr))
				$(tr).remove()
			},
			complete: function () { },
		})
	})
})