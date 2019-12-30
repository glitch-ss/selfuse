$(document).ready(function(){
	$('#get_key_list').click(function(){
		
	})
	$('.band').change(function(){
		if ($(this).val()=='nordstrom'){
			$('.color').removeClass('hidden')
		}else{
			$('.color').addClass('hidden')
		}
	})
	$('#submit').click(function(){
		$('.error-message').html("")
		band = $('.band').val()
		item_id = $('.item_id').val()
		color = $('.color').val()
		if(item_id==""){
			$('.error-message').append('<span>Item-ID is None!!!!</span>')
			return false;
		}
		if(band==""){
			$('.error-message').append('<span>band is None!!!!</span>')
			return false;
		}
		$.ajax({
		    async: false,
		    type: "POST",
		    url: '/sephora',
		    data: {"band": band, 'item_id': item_id, 'color': color},
		    dataType: "json",
		    error: function (e) { console.log(e) },
		    success: function (data) {
				if('error_message' in data){
					$('.error-message').append('<span>'+data['error_message']+'</span>')
					return false;
				}
		        $('.'+band+'0 tbody').html("")
				$('.'+band+'1 tbody').html("")
				band_list = data[band + '_list']
				console.log(band_list)
				for (l in band_list){
					bands = '.'+band+l+' tbody'
					for (i in band_list[l]){
						cmd = "<tr><td id=" + band_list[l][i][0] + ">" + band_list[l][i][0] + "</td><td href="+band_list[l][i][2]+ ">" + band_list[l][i][1]+"</td><td class='status'><span>" + 
						band_list[l][i][3]+"</span><button class='del btn btn-dark btn-sm' style='display:none'>delete</button></td></tr>"
						$(bands).append(cmd)
						if (band_list[l][i][3]=='BUY'){
							$('.'+bands+' tr:last').css("background-color", "#7ec699")
						}
					}
				}
		    },
			complete: function () { console.log('test1') },
		})
	})
	$('.del').click(function(){
		var tr = $(this).parent().parent()
		var item_id = $(tr).attr('id')
		$.ajax({
		    async: false,
		    type: "POST",
		    url: '/sephora',
		    data: {"action":'del', 'item_id': item_id},
		    dataType: "json",
		    error: function (e) { console.log(e) },
		    success: function (data) {
				if('error_message' in data){
					$('.error-message').append('<span>'+data['error_message']+'</span>')
					return false;
				}
		        $(tr).remove()
		    },
			complete: function () { console.log('test1') },
		})
	})
	upload = function(files){
		formData = new FormData()
		formData.append('files',$('#file')[0].files[0])
		$.ajax({
		    type: "POST",
		    url: "/upload",
		    data: formData,
		    cache: false,
		    processData: false, 
		    contentType: false,
		    success: function(data){
		    	if('error_message' in data){
					$('.error-message').append('<span>'+data['error_message']+'</span>')
					return false;
				}
				for (band in ['sephora', 'nordstrom']){
			        $('.'+band+'0 tbody').html("")
					$('.'+band+'1 tbody').html("")
					band_list = data[band + '_list']
					console.log(band_list)
					for (l in band_list){
						bands = '.'+band+l+' tbody'
						for (i in band_list[l]){
							cmd = "<tr><td id=" + band_list[l][i][0] + ">" + band_list[l][i][0] + "</td><td href="+band_list[l][i][2]+ ">" + band_list[l][i][1]+"</td><td class='status'><span>" + 
							band_list[l][i][3]+"</span><button class='del btn btn-dark btn-sm' style='display:none'>delete</button></td></tr>"
							$(bands).append(cmd)
							if (band_list[l][i][3]=='BUY'){
								$('.'+bands+' tr:last').css("background-color", "#7ec699")
							}
						}
					}
				}
		    }
		  })
	};
})