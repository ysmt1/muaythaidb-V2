$(document).on('change', 'input[type="file"]', function() {
    var id = this.id
    var div = $(this).parent("div")
    var file = this.files[0]
    var filenames = this.value.split('\\')

    $("label[for='" + id + "']").html(filenames[filenames.length - 1])
    
    if ($("#" + id + ".preview").length) {
        $("#" + id + ".preview").empty()
    }

    if (validFileType(file)) {
        var elem = document.createElement('img');
        elem.src = window.URL.createObjectURL(file);
        elem.className = "img-fluid img-thumbnail"
    } else {
        var elem = document.createElement('p')
        elem.className = 'invalid-feedback d-block'
        elem.textContent = 'Choose a valid file.  The file you chose was not an image file'
    }
    $("#" + id + ".preview").append(elem)
})

var fileTypes = [
    'image/jpeg',
    'image/pjpeg',
    'image/png',
    'image/jpg',
    'image/gif'
]

function validFileType(file) {
    for (var i = 0; i < fileTypes.length; i++) {
        if (file.type === fileTypes[i]) {
            return true
        }
    }
    return false
}