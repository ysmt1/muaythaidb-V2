$(document).ready(function () {
    $("#addGym").on('submit', function (e) {
        e.preventDefault()
        var self = this
        var csrf = $(this).find('input[type=hidden]').val()
        var gym_name = $('input[name="gym_name"]').val()
        var gym_location = $('input[name="gym_location"]').val()
        var gym_website = $('input[name="gym_website"]').val()

        $.ajax({
            type: "POST",
            url: "add_gym/",
            data: { 
                csrfmiddlewaretoken: csrf,
                "gym_name": gym_name,
                "gym_location": gym_location,
                "gym_website": gym_website
            }
        })
        .done(function (data) {
                if (data.error) {
                    $("#add-gym-msg").text(data.error)
                } else {
                    $("#add-gym-msg").text(data.success)
                }
            })
        .fail(() => {
            $("#add-gym-msg").text("An error has occured")
        })
    })
})
