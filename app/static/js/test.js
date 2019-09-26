$(document).ready(function(){
	$('#search_button').click(function(){
	valstr=$('#search input').val()
	$.ajax({
		    async: false,
		    type: "POST",
		    url: '/innerexpress',
		    data: {"date": valstr},
		    dataType: "json",
		    error: function () { console.log('err') },
		    success: function (data) {
		        $('.name_list').html("")
				console.log(data)
				name_list = data['name_list']
				price = data['price']
				console.log(name_list)
				price_cmd = 'price for the day is: '+ price
				$('#price').text(price_cmd)
				for (i in name_list){
					cmd = "<tr><td>"+name_list[i][0]+"</td><td>"+name_list[i][1]+"</td></tr>"
					$('.name_list').append(cmd)
				}
		    },
			complete: function () { console.log('test') },
		})
	})
	$('#download').click(function(){
		valstr=$('#search input').val()
		file_name = valstr + ".xlsx"
		$.ajax({
		    async: false,
		    type: "POST",
		    url: '/innerexpress',
		    data: {"date": valstr},
		    dataType: "json",
		    error: function () { console.log('err') },
		    success: function (data) {
				console.log(data)
				name_list = data['name_list']
		    },
			complete: function () { funDownload(name_list, fine_name); },
		})
	})
	var funDownload = function (content, filename) {
	    var eleLink = document.createElement('a');
	    eleLink.download = filename;
	    eleLink.style.display = 'none';
	    // 字符内容转变成blob地址
	    var sheet = list2sheet(content);
    	var blob = sheet2blob(sheet);
	    eleLink.href = URL.createObjectURL(blob);
	    // 触发点击
	    document.body.appendChild(eleLink);
	    eleLink.click();
	    // 然后移除
	    document.body.removeChild(eleLink);
	};
	function list2sheet(list) {
	    var sheet = {}; // 将要生成的sheet
	    list.forEach(function(row, i) {
	        if(i == 0) sheet['!ref'] = 'A1:'+String.fromCharCode(65+row.length-1)+(list.length-1);
	        row.forEach(function(col, j) {
	            sheet[String.fromCharCode(65+j)+(i+1)] = {v: col};
	        });
	    });
	    return sheet;
	}
	function sheet2blob(sheet, sheetName) {
	    sheetName = sheetName || 'sheet1';
	    var workbook = {
	        SheetNames: [sheetName],
	        Sheets: {}
	    };
	    workbook.Sheets[sheetName] = sheet;
	    // 生成excel的配置项
	    var wopts = {
	        bookType: 'xlsx', // 要生成的文件类型
	        bookSST: false, // 是否生成Shared String Table，官方解释是，如果开启生成速度会下降，但在低版本IOS设备上有更好的兼容性
	        type: 'binary'
	    };
	    var wbout = XLSX.write(workbook, wopts);
	    var blob = new Blob([s2ab(wbout)], {type:"application/octet-stream"});
	    // 字符串转ArrayBuffer
	    function s2ab(s) {
	        var buf = new ArrayBuffer(s.length);
	        var view = new Uint8Array(buf);
	        for (var i=0; i!=s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
	        return buf;
	    }
	    return blob;
	}
})