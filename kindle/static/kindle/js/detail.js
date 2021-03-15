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

$(document).ready(function () {
    $('#download').click(function (e) {
        // e.preventDefault();
        var a = $('#down-link')
        a[0].click()
    });
    $('.star').click(function (e) {
        var currentTarget = $(e.currentTarget)
        var img = e.target
        // var parent=currentTarget.parent().parent()
        var id = currentTarget[0].dataset['id']
        $.ajax({
            url: '/book/star/' + id,
            data: {
                code: img.dataset["num"]
            }
        }).done(function (msg) {
            if (msg['code'] === 0) {
                currentTarget.children('.like').css('display', 'none')
                currentTarget.children('.unlike').css('display', 'inline')
            } else if (msg['code'] === 1) {
                currentTarget.children('.like').css('display', 'inline')
                currentTarget.children('.unlike').css('display', 'none')
            } else {
                console.log('err')
            }
        });
        e.preventDefault();
        // e.stopPropagation();
    });

    var link = $('.star')
    var mjson = JSON.stringify([link[0].dataset['id']])
    $.ajax({
        url: '/book/starajax/',
        method: 'POST',
        data: {
            code: mjson,
            csrfmiddlewaretoken: getCookie('csrftoken'),
        }
    }).done(function (msg) {
        if (msg['code'] === 1) {
            var mlist = JSON.parse(msg['mlist'])
            for (let index = 0; index < mlist.length; index++) {
                const element = mlist[index];
                var like = link.find('.like')
                var unlike = link.find('.unlike')
                if (element) {
                    like.css('display', 'inline')
                    unlike.css('display', 'none')
                } else {
                    unlike.css('display', 'inline')
                    like.css('display', 'none')
                }
            }
        } else {
            console.log('rt')
        }
    });
    $('.review-reply').click(function (e) {
        e.preventDefault();
        $('#hidden-code').attr('value', this.dataset.num);
        var mstyle = {
            'display': 'block'
        }
        $('.hidden-form').css(mstyle)
    });
    $('#shutdown').click(function (e) { 
        e.preventDefault();
        $('.hidden-form').css({'display': 'none'});
        $('#text2').val('');
    });

});