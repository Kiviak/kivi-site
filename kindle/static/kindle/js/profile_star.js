$(document).ready(function () {
    $('.selectall').change(function (e) { 
        // e.preventDefault();
        if (this.checked) {
            // the checkbox is now checked 
            $('.item>input').prop('checked', true);
        } else {
            // the checkbox is now no longer checked
            $('.item>input').prop('checked', false);
        }
    });
    $('.delete').click(function (e) { 
        e.preventDefault();
        $('#submit').trigger('click');
    });
});