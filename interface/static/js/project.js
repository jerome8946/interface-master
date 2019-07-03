

$(document).ready(function () {
    $('#btn').click(function () {
        var fromObject = new Object();
        fromObject.project_name = $('#project_name').val();
        fromObject.status = $('#status').val();
        fromObject.page = '1';
        var data = JSON.stringify(fromObject);
        $.ajax({
            url: "index",
            type: 'GET',
            dataType: 'json',
            data: data,
            success: function (data) {
               alert(data)
            }
        });
    });
})
