/* When user clicks "like" icon, send a AJAX request
to update database and get back a JSON object with
an updated total like count*/
$(document).ready(function () {
    $('p.like-flag').each(function (i) {
        var id = $(this).attr('id')
        var numId = id.split('_')[1]
        if ($(this).html() === 'true') {
            $('#likeForm_' + numId).hide()
        } else {
            $('#unlikeForm_' + numId).hide()
        }
    })
    $('.like-form').on('submit', function (e) {
        e.preventDefault()
        var self = this
        var csrf = $(this).find('input[type=hidden]').val()
        var url = $(this).attr('action')
        var id = $(this).attr('id')
        var formType = id.split('_')[0]
        var numId = id.split('_')[1]
        $('#errorFor_' + numId).empty()

        $.ajax({
            type: "POST",
            url: url,
            data: {csrfmiddlewaretoken: csrf}
        })
        .done(function (data) {
            if (data.error) {
                $('#errorFor_' + numId).text(data.error)
            } else {
                if (data.success !== 1) {
                    $('#counterFor_' + numId).text(' ' + data.success + ' people liked this review')
                } else {
                    $('#counterFor_' + numId).text(' ' + data.success + ' person liked this review')
                }
                $(self).hide()
                if (formType === 'likeForm') {
                    $('#unlikeForm_' + numId).show()
                } else {
                    $('#likeForm_' + numId).show()
                }
            }
        })
        .fail(() => {
            $('#errorFor_' + numId).text("An error has occured")
        })
    })
})
