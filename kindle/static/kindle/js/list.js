
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

$(document).ready(function (e) {

    $(function(){
        var target=$('.pagination')
        var current_num=Number(target.eq(0).attr('data-current'))
        var total_num=Number(target.eq(0).attr('data-total'))
        var pagination=pagination_all_in_one()
        pagination(target,current_num,total_num)
    });

    $('.star').click(function (e) {
        var currentTarget=$(e.currentTarget)
        var img=e.target
        var parent=currentTarget.parent().parent()
        var id=parent[0].dataset['id']
        $.ajax({
            url:'/book/star/'+id,
            data:{code:img.dataset["num"]}
        }
        ).done(function( msg ) {
            if (msg['code']===0) {
                currentTarget.children('.like').css('display','none')                 
                currentTarget.children('.unlike').css('display','inline')
            }else if (msg['code']===1) {
                currentTarget.children('.like').css('display','inline')                 
                currentTarget.children('.unlike').css('display','none')
            } else {
                console.log('err')
            }
          });
        e.preventDefault();
        // e.stopPropagation();
    });

    var items=$('.item')
    var mydict=Array()
    for (let index = 0; index < items.length; index++) {
        const element = items[index];
        mydict.push(element.dataset['id'])
        
    }
    mjson=JSON.stringify(mydict)
    $.ajax({
        url:'/book/starajax/',
        method:'POST',
        data:{code:mjson,
            csrfmiddlewaretoken:getCookie('csrftoken'),}
        }
    ).done(function( msg ) {
        if (msg['code']===1) {
            var mlist=JSON.parse(msg['mlist'])
            for (let index = 0; index < mlist.length; index++) {
                const element = mlist[index];
                var item=$(items[index])
                var like=item.find('.like')
                var unlike=item.find('.unlike')
                if (element) {
                    like.css('display','inline')
                    unlike.css('display','none')
                }else{
                    unlike.css('display','inline')
                    like.css('display','none')
                }   
            }
        }else {
            console.log('rt')
        }
      });
});