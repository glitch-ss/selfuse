$(document).ready(function() {
    var post_url = "/cz"
    var post_action_url = '/action'
    $.post(post_url, {'page':'myrpa'}, function(data){
        myrpa = data['myrpa']
        update_myrpa(myrpa)})
    String.format = function() {
        if (arguments.length == 0)
            return null;
        var str = arguments[0];
        for ( var i = 1; i < arguments.length; i++) {
            var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
            str = str.replace(re, arguments[i]);
        }
        return str;
    };
    $.post(post_url, {'page':'doc'}, function(data){
        doc_list = data['doc']
        add_div = '<div id="mod_{0}" class="sub-menu" data-href="{1}" onclick="update_doc(this)">\
                <span>{2}</span>\
            </div>'
        for (i in doc_list){
            add_one = String.format(add_div, i, doc_list[i][1], doc_list[i][0])
            $('.sub-list').append(add_one)
        }
    })
    $('.self-list').click(function(){
        $(this).addClass('menu-selected')
        $(this).siblings().removeClass('menu-selected')
        $('.sub-menu').removeClass('menu-selected')
        $('.info').html('')
        var id = $(this).attr("id")
        if(id == "rpa-market"){
            $.post(post_url, {'page':'market'}, function(data){
                market_list = data['market_list']
                update_market(market_list)
            })
        }
        else if(id == "myrpa"){
            $.post(post_url, {'page':'myrpa'}, function(data){
                myrpa = data['myrpa']
                update_myrpa(myrpa)
            })
        }
        else if(id == "doc"){
            $.post(post_url, {'page':'doc'}, function(data){
                doc = data['doc']
                update_doc(doc)
            })
        }
    })
    $('#postform').on('hidden.bs.modal', function () {
        $(".name").attr("post-id", "")
        $(".name").html("")
        $(".period select").val("1")
    })
})
    function update_market(rpa_list){
        //rpa_list[   ['iso_id', 'name', 'description'],
        //            ['iso_id', 'name', 'description'],
        //            ['iso_id', 'name', 'description'],
        //        ...]
        var add_tr
        var head = '<div class="iso-name">  \
                          <span>RPA市场</span> \
                      </div>'
        var market_body = '<table class="table"> \
                        <thead> \
                          <tr> \
                            <th>镜像名</th> \
                            <th>简介</th> \
                            <th>操作</th> \
                          </tr> \
                        </thead> \
                        <tbody></tbody>'
        $('.info').append('<div class="iso-list"></div>')
        $('.info .iso-list').append(head, market_body)
        for(var i in rpa_list){
            add_tr = '<tr id="{0}"><td>{1}</td><td>{2}</td><td><a class="buy" data-toggle="modal" data-target="#postform" onclick="buy(this)">购买</a></td></tr>'
            add_tr =  String.format(add_tr, rpa_list[i][0], rpa_list[i][1], rpa_list[i][2])
            $('.info table tbody').append(add_tr)
        }
    }
    /*
    function update_doc(doc_list){
        //{
        //  '模块1': [['呵呵哒', 'http://192.168.1.4:5000/static/file/video/test.mp4'], ['鲁班大师，智商250', 'http://192.168.1.4:5000/static/file/video/test.mp4']],
        //  '模块2': [['我是警察', 'http://192.168.1.4:5000/static/file/video/test.mp4'], ['我想做个好人', 'http://192.168.1.4:5000/static/file/video/test.mp4']]
        //}
        var head = '<div class="iso-name">  \
                          <span>技术文档</span> \
                      </div>'
        var doc_body = '<table class="table"> \
                        <tbody></tbody>'
        $('.info').append('<div class="iso-list"></div>')
        $('.info .iso-list').append(head, doc_body)
        for(var i in doc_list){
            for (item in doc_list[i]){
                add_tr = '<tr><td><video src="{0}" width="320" height="240" controls="controls">\
                        Your browser does not support the video tag.\
                        </video></td></tr>'
                add_tr =  String.format(add_tr, doc_list[i][0][1], doc_list[i][0][0])
                $('.info table tbody').append(add_tr)
            }
            
        }
    }*/
    function update_doc(element){
        var link = $(element).attr('data-href')
        $(element).addClass('menu-selected')
        $(element).siblings().removeClass('menu-selected')
        $('.self-list').removeClass('menu-selected')
        $('.info').html('')
        $('.info').append('<div class="iso-list"></div>')
        add_tr = '<tr><td><video src="{0}" width="640" height="480" controls="controls">\
                Your browser does not support the video tag.\
                </video></td></tr>'
        add_tr =  String.format(add_tr, link)
        $('.info .iso-list').append(add_tr)
    }
    function update_myrpa(myrpa_list){
        //   {
        //   'iso1':{'name':'iso1', 'instance':[['0', '实例名1', '3天'], ['1', '实例名2', '已到期']]},
        //   'iso2':{'name':'iso2', 'instance':[['3', '实例名1', '5天'], ['1', '实例名2', '6天']]},
        //   ...}
        for(iso in myrpa_list){
            var head = '<div class="iso-name"> \
                          <span>{0}</span> \
                      </div>'
            head = String.format(head, myrpa_list[iso]['name'])
            var market_body = '<table id="" class="table"> \
                        <thead> \
                          <tr> \
                            <th>实例名</th>\
                            <th>剩余天数</th> \
                            <th>操作</th> \
                          </tr> \
                        </thead> \
                        <tbody></tbody>'
            main = '<div id="iso_{0}" class="iso-list"></div>'
            main = String.format(main, iso)
            $('.info').append(main)
            sel = '.info #iso_{0}'
            sel = String.format(sel, iso)
            $(sel).append(head, market_body)
            sel = sel + ' table tbody'
            for (i in myrpa_list[iso]['instance']){
                add_tr = '<tr id="instance_{0}"><td><a href="{3}">{1}</a></td><td>{2}</td><td><a class="extend" data-toggle="modal" data-target="#postform" onclick="extend(this)">续费</a>/<a class="delete" onclick="delete_instance(this)">释放</a></td></tr>'
                add_tr =  String.format(add_tr, myrpa_list[iso]['instance'][i][0],myrpa_list[iso]['instance'][i][1], myrpa_list[iso]['instance'][i][2], myrpa_list[iso]['instance'][i][3])
                $(sel).append(add_tr)
            }
            
        }
    }
    function delete_instance(element){
        if (confirm("确定释放?")){
            instance_id = $(element).parent().parent().attr('id')
            $.post(post_url, {'action':'delete', 'class':'instance', 'id':instance_id}, function(data){
                myrpa = data['myrpa']
                update_myrpa(myrpa)
            })
        }
        
    }
    function buy(element){
        iso_id = $(element).parent().parent().attr('id')
        iso_name = $(element).parent().parent().children().first().text()
        $("#myModalLabel").text("镜像购买申请")
        add_name = '<span>镜像名称:</span><span>{0}</span>'
        add_name = String.format(add_name, iso_name)
        $(".name").append(add_name)
        $(".name").attr("post-id", iso_id)
    }
    function extend(element){
        iso_id = $(element).parent().parent().attr('id')
        iso_name = $(element).parent().parent().children().first().text()
        $("#myModalLabel").text("镜像延期申请")
        add_name = '<span>镜像名称:</span><span>{0}</span>'
        add_name = String.format(add_name, iso_name)
        $(".name").append(add_name)
        $(".name").attr("post-id", iso_id)
    }
    function postaction(){
        var iso_id = $(".name").attr("post-id")
        var period = $(".period select").val()
        self.post(action_url, {"id":iso_id, "period":period}, function(){
            alert("提交成功")
        })
    }
    
    