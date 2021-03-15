// 1.模块化，可灵活定制
// 2.支持ajax和local两种模式
// 3.不依赖jquery
// 4.支持多种事件的响应

function pagination_all_in_one() {

    function html_builder(container, page_size = 3, has_arrow_menu = true, has_go_menu = true,
        auto_hide_arrow = true, class_pre = 'pagination', use_default_css = true) {
        var config = {
            arrow_previou: {
                'element': '<a></a>',
                'class': '-arrow-previou',
                'text': '<',
                'css': {
                    'min-width': '30px',
                    'border': '1px solid #aaa',
                    'border-radius': '3px',
                    'padding': '5px 7px 5px 7px',
                    'margin-right': '5px',
                    'background': '#fff',
                    'font-size': '14px',
                    'color': '#333',
                    'text-decoration': 'none',
                    'text-align': 'center'
                }
            },
            arrow_next: {
                'element': '<a></a>',
                'class': '-arrow-next',
                'text': '>',
                'css': {
                    'min-width': '30px',
                    'border': '1px solid #aaa',
                    'border-radius': '3px',
                    'padding': '5px 7px 5px 7px',
                    'margin-left': '5px',
                    'background': '#fff',
                    'font-size': '14px',
                    'color': '#333',
                    'text-decoration': 'none',
                    'text-align': 'center'
                }
            },
            first_page: {
                'element': '<a></a>',
                'class': '-first-page',
                'text': 'first',
                'css': {
                    'min-width': '30px',
                    'border': '1px solid #aaa',
                    'border-radius': '3px',
                    'padding': '5px 7px 5px 7px',
                    'margin': '1px',
                    'background': '#fff',
                    'font-size': '14px',
                    'color': '#333',
                    'text-decoration': 'none',
                    'text-align': 'center'
                }
            },
            last_page: {
                'element': '<a></a>',
                'class': '-last-page',
                'text': 'last',
                'css': {
                    'min-width': '30px',
                    'border': '1px solid #aaa',
                    'border-radius': '3px',
                    'padding': '5px 7px 5px 7px',
                    'margin': '1px',
                    'background': '#fff',
                    'font-size': '14px',
                    'color': '#333',
                    'text-decoration': 'none',
                    'text-align': 'center'
                }
            },
            first_ellipsis: {
                'element': '<a></a>',
                'class': '-first-ellipsis',
                'text': '...',
                'css': {
                    'min-width': '30px',
                    'padding': '5px 7px 5px 7px',
                    'margin': '1px',
                    'background': '#fff',
                    'font-size': '14px',
                    'color': '#333',
                    'text-decoration': 'none',
                    'text-align': 'center'
                }
            },
            last_ellipsis: {
                'element': '<a></a>',
                'class': '-last-ellipsis',
                'text': '...',
                'css': {
                    'min-width': '30px',
                    'padding': '5px 7px 5px 7px',
                    'margin': '1px',
                    'background': '#fff',
                    'font-size': '14px',
                    'color': '#333',
                    'text-decoration': 'none',
                    'text-align': 'center'
                }
            },
            common_page: {
                'element': '<a></a>',
                'class': '-common-page',
                'text': '+',
                'css': {
                    'min-width': '30px',
                    'border': '1px solid #aaa',
                    'border-radius': '3px',
                    'padding': '5px 7px 5px 7px',
                    'margin': '1px',
                    'background': '#fff',
                    'font-size': '14px',
                    'color': '#333',
                    'text-decoration': 'none',
                    'text-align': 'center'
                }
            },
            go_input: {
                'element': '<input type="text" minlength="1" placeholder="">',
                'class': '-go-input',
                'css': {
                    'width': '40px',
                    'border': '1px solid #aaa',
                    'border-radius': '3px',
                    'padding': '5px 7px 5px 7px',
                    'margin-left': '20px',
                    'background': '#fff',
                    'font-size': '14px',
                    'color': '#333',
                    'text-align': 'center'
                },
            },
            go_button: {
                'element': '<input type="button" value="Go" >',
                'class': '-go-button',
                'css': {
                    'width': '40px',
                    'border': '1px solid #aaa',
                    'border-radius': '3px',
                    'padding': '5px 7px 5px 7px',
                    'margin-left': '5px',
                    'background': '#fff',
                    'font-size': '14px',
                    'font-style': 'italic',
                    'color': '#333',
                    'text-align': 'center'
                },
            },
            container: {
                css: {
                    'clear': 'both',
                    'padding': '10px'
                }
            }
        }

        has_arrow_menu ? $(config.arrow_previou.element).attr({
            class: class_pre + config.arrow_previou.class
        }).html(config.arrow_previou.text).appendTo(container) : undefined

        $(config.first_page.element).attr({
            class: class_pre + config.first_page.class
        }).html(config.first_page.text).appendTo(container)

        $(config.first_ellipsis.element).attr({
            class: class_pre + config.first_ellipsis.class
        }).html(config.first_ellipsis.text).appendTo(container)

        for (var index = 0; index < 2 * page_size + 1; index++) {
            $(config.common_page.element).attr({
                class: class_pre + config.common_page.class + ' ' + class_pre + config.common_page.class + '-' + index
            }).html(config.common_page.text).appendTo(container)
        }

        $(config.last_ellipsis.element).attr({
            class: class_pre + config.last_ellipsis.class
        }).html(config.last_ellipsis.text).appendTo(container)

        $(config.last_page.element).attr({
            class: class_pre + config.last_page.class
        }).html(config.last_page.text).appendTo(container)

        has_arrow_menu ? $(config.arrow_next.element).attr({
            class: class_pre + config.arrow_next.class
        }).html(config.arrow_next.text).appendTo(container) : undefined

        has_go_menu ? $(config.go_input.element).attr({
            class: class_pre + config.go_input.class
        }).appendTo(container) : undefined

        has_go_menu ? $(config.go_button.element).attr({
            class: class_pre + config.go_button.class
        }).appendTo(container) : undefined

        var pagination_block = {
            get_arrow_pre: function () {
                return has_arrow_menu ? container.find('.' + class_pre + config.arrow_previou.class) : undefined
            },
            get_arrow_next: function () {
                return has_arrow_menu ? container.find('.' + class_pre + config.arrow_next.class) : undefined
            },
            get_first_page: function () {
                return container.find('.' + class_pre + config.first_page.class)
            },
            get_last_page: function () {
                return container.find('.' + class_pre + config.last_page.class)
            },
            get_first_ellipsis: function () {
                return container.find('.' + class_pre + config.first_ellipsis.class)
            },
            get_last_ellipsis: function () {
                return container.find('.' + class_pre + config.last_ellipsis.class)
            },
            get_common_page_all: function () {
                return container.find('.' + class_pre + config.common_page.class)
            },
            get_common_page: function (index) {
                return container.find('.' + class_pre + config.common_page.class + '-' + index)
            },
            get_go_input: function () {
                return has_go_menu ? container.find('.' + class_pre + config.go_input.class) : undefined
            },
            get_go_button: function () {
                return has_go_menu ? container.find('.' + class_pre + config.go_button.class) : undefined
            },
        }
        if (use_default_css) {
            if (has_arrow_menu) {
                pagination_block.get_arrow_pre().css(config.arrow_previou.css)
                pagination_block.get_arrow_next().css(config.arrow_next.css)
            }
            if (has_go_menu) {
                pagination_block.get_go_input().css(config.go_input.css)
                pagination_block.get_go_button().css(config.go_button.css)
            }
            pagination_block.get_first_page().css(config.first_page.css)
            pagination_block.get_last_page().css(config.last_page.css)
            pagination_block.get_first_ellipsis().css(config.first_ellipsis.css)
            pagination_block.get_last_ellipsis().css(config.last_ellipsis.css)
            pagination_block.get_common_page_all().css(config.common_page.css)
            container.css(config.container.css)
        }

        return pagination_block
    }

    function pagination(container, current_num, total_num, page_size = 3, has_arrow_menu = true, has_go_menu = true,
        auto_hide_arrow = true, class_pre = 'pagination', use_default_css = true, keyword = 'page') {

        var block = html_builder(container, page_size, has_arrow_menu, has_go_menu, auto_hide_arrow, class_pre, use_default_css)


        function newurl(key, val, url) {
            var re = RegExp('[\?&]?' + key + '=[^&]+')
            var marr = re.exec(url)[0].split('=')
            marr[1] = '' + val
            return (url.replace(re, marr.join('=')))
        }

        var url = String(document.location.href)

        if (has_arrow_menu) {
            if (auto_hide_arrow) {
                var arrow_pre = block.get_arrow_pre()
                var arrow_next = block.get_arrow_next()
                current_num == 1 ? arrow_pre.hide() : arrow_pre.show()
                current_num == total_num ? arrow_next.hide() : arrow_next.show()
                arrow_pre.attr('href', newurl(keyword, current_num - 1, url))
                arrow_next.attr('href', newurl(keyword, current_num + 1, url))
            }
        }

        if (has_go_menu) {
            block.get_go_button().click(function () {
                var input_text = $(this).parent().find('input[type="text"]')
                var num = input_text.val()
                try {
                    num = Number(num)
                } catch (error) {

                }
                if (num >= 1 && num <= total_num) {
                    location = newurl(keyword, Math.floor(num), url)
                } else {
                    input_text.val('')
                }
            })
            block.get_go_input().keydown(function (event) {
                if (event.keyCode == 13) {
                    var input_text = $(this)
                    var num = input_text.val()
                    try {
                        num = Number(num)
                    } catch (error) {

                    }
                    if (num >= 1 && num <= total_num) {
                        location = newurl(keyword, Math.floor(num), url)
                    } else {
                        input_text.val('')
                    }
                }
            })
        }

        current_num - page_size > 2 ? block.get_first_ellipsis().show() : block.get_first_ellipsis().hide()
        current_num + page_size < total_num - 1 ? block.get_last_ellipsis().show() : block.get_last_ellipsis().hide()

        var first_page = block.get_first_page()
        var last_page = block.get_last_page()
        current_num - page_size > 1 ? first_page.show() : first_page.hide()
        current_num + page_size < total_num ? last_page.show() : last_page.hide()
        first_page.html(1).attr('href', newurl(keyword, 1, url))
        last_page.html(total_num).attr('href', newurl(keyword, total_num, url))

        block.get_common_page_all().hide()
        var left = Math.min(page_size, current_num - 1)
        for (var i = 0; i < left; i++) {
            block.get_common_page(page_size - 1 - i).html(current_num - 1 - i).show().attr('href', newurl(keyword, current_num - 1 - i, url))
        }
        var right = Math.min(page_size, total_num - current_num)
        for (var i = 0; i < right; i++) {
            block.get_common_page(page_size + 1 + i).html(current_num + 1 + i).show().attr('href', newurl(keyword, current_num + 1 + i, url))
        }
        if (use_default_css) {
            block.get_common_page(page_size).html(current_num).show().attr('href', url).css({
                'background': 'gray',
                'color': '#fff'
            })
        } else {
            block.get_common_page(page_size).html(current_num).show().attr('href', url)
        }

    }

    return pagination
}
