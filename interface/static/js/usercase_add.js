$(document).ready(function () {

    var projectOptions = getOption("selectProject", 0);
    $('#btn_env_add').click(function () {
        var valHtml = "<li><select id=\"project_id\" class='project_id' name=\"project_id\"></select>\n" +
            "<select id=\"modules_id\" class='modules_id' name=\"modules_id\"></select>\n" +
            "<select id=\"env_id\" class='env_id' name=\"env_id\"></select>\n" +
            "<button type=\"button\" class=\"btn btn-danger del\" >删除</button></li>";
        $('#env_ul').append(valHtml);
        var li_num = $('#env_ul').parent().find("li").length - 1;
        $('#env_ul').children("li").eq(li_num).children(".project_id").html(projectOptions);
    })
    $('#env_ul').on("click", ".del", function (e) {
        $(this).parent("li").remove();
    });

    $('#env_ul').on("change", ".project_id", function (e) {
        var val = $(this).val();
        var modulesOptions = getOption("selectModular", val);
        $(this).siblings(".modules_id").html(modulesOptions);
    });

    $('#env_ul').on("change", ".modules_id", function (e) {
        var val = $(this).val();
        var envOptions = getOption("selectEnv", val);
        $(this).siblings(".env_id").html(envOptions);
    });


    $('#btnSubmit').click(function () {
        var csrftoken = $("meta[name=csrf-token]").attr("content");
        var fromObject = new Object();
        fromObject.case_name = $('#case_name').val();
        var case_jsonarray = new Array();
        for (var i = 0; i < $(".project_id").length; i++) {
            var json_case = {};
            json_case.project_id = $(".project_id").eq(i).val();
            json_case.modules_id = $(".modules_id").eq(i).val();
            json_case.env_id = $(".env_id").eq(i).val();
            case_jsonarray.push(json_case)
        }
        fromObject.case_jsonarray = case_jsonarray;
        // var url = window.location.protocol + "//" + window.location.host + "/case/add";
        var url = 'http://127.0.0.1:5000/aps/addjob';
        // var data = JSON.stringify(fromObject);

       var data = "{\n" +
           "\"caseList\":[1,3],\n" +
           "\"cronStr\":\"1-2 0/1 * * * * *\",\n" +
           "\"scheduling_title\":\"测试调度\"\n" +
           "}\n"

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


function getOption(path, num) {
    var optionstring;
    var result;
    var url = ""
    if (num == 0) {
        url = window.location.protocol + "//" + window.location.host + "/env/" + path;
    } else {
        url = window.location.protocol + "//" + window.location.host + "/env/" + path + "/" + num;
    }
    $.ajax({
        url: url,
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        async: false,  //这里选择异步为false，那么这个程序执行到这里的时候会暂停，等待数据加载完成后才继续执行
        success: function (data) {
            var dataObj = eval("(" + data + ")");//转换为json对象
            $.each(dataObj, function (key, value) {  //循环遍历后台传过来的json数据
                optionstring += "<option value=\"" + key + "\" >" + value + "</option>";
            });
            // $("#tra_project_name").html(); //获得要赋值的select的id，进行赋值
            result = "<option value=''>请选择</option> " + optionstring
        }
    });
    return result;
}