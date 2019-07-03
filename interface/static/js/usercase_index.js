$(document).ready(function () {

     $('#start').click(function () {
        var csrftoken = $("meta[name=csrf-token]").attr("content");
        var fromObject = new Object();
        fromObject.case_name = $('#case_name').val();
        fromObject.case_id = $('#caseid').val();
        var case_jsonarray = new Array();
        for (var i = 0; i < $(".project_id").length; i++) {
            var json_case = {};
            json_case.project_id = $(".project_id").eq(i).val();
            json_case.modules_id = $(".modules_id").eq(i).val();
            json_case.env_id = $(".env_id").eq(i).val();
            case_jsonarray.push(json_case)
        }
        fromObject.case_jsonarray = case_jsonarray;
        var url = window.location.protocol + "//" + window.location.host + "/case/start";
        var data = JSON.stringify(fromObject);
        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: data,
            contentType: 'application/json; charset=utf-8',
            headers: {"X-CSRFToken": csrftoken},
            success: function (data) {
                if (data.ok) {
                    window.location.href = window.location.protocol + "//" + window.location.host + "/case/index";
                }

            }
        });


    });


})