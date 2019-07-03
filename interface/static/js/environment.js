$(document).ready(function () {
    //获取项目下拉列表
    var projectOptions = getOption("selectProject", 0);
    var select_index = 0;
    var index = 0;

    $("#project_id").html(projectOptions);

    $("#project_id").change(function () {
        var val = $("#project_id").val();
        var modulesOptions = getOption("selectModular", val);
        $("#modules_id").find("option").remove();
        $("#modules_id").html(modulesOptions); //获得要赋值的select的id，进行赋值
    });

    $('#transfer_ul').on("click", ".del", function (e) {
        $(this).parent().parent("li").remove();
    });

    $('#transfer_ul').on("click", ".delAdd", function (e) {
        $(this).parent().parent("li").remove();
    });

    $('#parm_ul').on("click", ".delParm", function (e) {
        $(this).parent("li").remove();
    });

    $('#transfer_ul').on("click", ".addParm", function (e) {
        var val = "<li><div class=\"form-group\"> \n" +
            " <input id='var_regexp' name=\"var_regexp\" placeholder=\"输入正则表达式\"  type=\"text\" value=\"\"> \n" +
            " <input id='var_variable_name' name=\"var_variable_name\" placeholder=\"请输入变量名\" type=\"text\" value=\"\"> <button type=\"button\" class=\"btn btn-danger delAdd\" >删除</button>\n" +
            "</div></li>";
        $(this).siblings().find('ul').addClass('addParm_ul').append(val);
    });

    //参数类型选择
    $('#parm_ul').on("change", ".env_parameter_select", function (e) {
        var valHtml = "<div class='date_div'><div class=\"form-group \">\n" +
            "<label>日期格式</label><input id=\"par_date_type\" class='par_date_type' name=\"par_date_type\" class='dateInput' placeholder=\"日期格式\" type=\"text\" value=\"\">\n" +
            "</div>\n" +
            "<div class=\"form-group\">\n" +
            "    <label>开始时间</label><input id=\"par_start_date\" name=\"par_start_date\" class='dateInput'  placeholder=\"开始时间\" type=\"text\" value=\"\">\n" +
            "</div>\n" +
            "<div class=\"form-group\">\n" +
            "  <label>结束时间</label>  <input id=\"par_end_date\" name=\"par_end_date\" class='dateInput' placeholder=\"结束时间\" type=\"text\" value=\"\">\n" +
            "</div>\n" +
            "<div class=\"form-group par_correct_value_div\">\n" +
            "  <label>案例参数值</label>  <input id=\"env_parameter_par_correct_value\" name=\"env_parameter_par_correct_value\" class=\"env_parameter_par_correct_value\" placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
            "</div>"
            +
            "<div class=\"form-group par_correct_value_div\">\n" +
            "  <label>参数变量</label>  <input id=\"env_parameter_par_variable\" name=\"env_parameter_par_par_variable\" class=\"env_parameter_par_par_variable\" placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
            "</div>"
            + "</div>";
        var val = $(this).val();
        if (val == '2') {
            //选择了 date
            $(this).parent().parent().find(".par_correct_value_div").remove();
            $(this).parent().parent().find(".par_range_div").remove();
            $(this).parent().parent().append(valHtml);
        } else {
            // console.log($(this).parent().siblings().find('input[class=par_date_type]').length)
            // console.log($(this).parent().parent().siblings().find('input[class=par_date_type]').length)

            if ($(this).parent().siblings().find('input[class=par_date_type]').length == 1) {//js判断元素是否存在
                valHtml = "<div class=\"form-group par_range_div\">\n" +
                    "  <label >参数限制范围</label><input id=\"env_parameter_par_range\" name=\"env_parameter_par_range\" class=\"env_parameter_par_range\" placeholder=\"输入参数限制范围\" required=\"\" type=\"text\" value=\"\">\n" +
                    "</div>\n" +
                    "<div class=\"form-group par_correct_value_div\">\n" +
                    "  <label >案例参数值</label>  <input id=\"env_parameter_par_correct_value\" name=\"env_parameter_par_correct_value\" class=\"env_parameter_par_correct_value\" placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
                    "</div>" + "<div class=\"form-group par_correct_value_div\">\n" +
                    "  <label>参数变量</label>  <input id=\"env_parameter_par_variable\" name=\"env_parameter_par_par_variable\" class=\"env_parameter_par_par_variable\" placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
                    "</div>";
                // $(this).parent().siblings().find('input[class=dateInput]').remove();
                $(this).parent().parent().find(".date_div").remove();
                $(this).parent().parent().append(valHtml);
            }
        }

    });

    //项目下拉框选择
    $('#transfer_ul').on("change", "#tra_project_name", function (e) {
        var val = $(this).val();
        var select_class = $(this).attr('class');
        var num = select_class.substr(select_class.length - 1, 1);
        var tra_modules_name = "tra_modules_name" + num;
        var modulesOptions = getOption("selectModular", val);
        $("." + tra_modules_name).find("option").remove();
        $("." + tra_modules_name).html(modulesOptions); //获得要赋值的select的id，进行赋值
    });

    //新增接口参数
    $('#btn_env_addParm').click(function () {
        var val = "<li class='env_addParm_li'><button id=\"btn_del_parm\" class=\"btn btn-outline btn-link delParm\">\n" +
            "                                                            删除参数\n" +
            "                                                        </button>" +
            "<div class=\"panel-body  body_div\">\n" +
            "                                        \n" +
            "                                            <div class=\"form-group\">\n" +
            "                                                <label>中文名称</label><input id=\"env_parameter_par_cn_name\" name=\"env_parameter_par_cn_name\" placeholder=\"输入中文名称\" required=\"\" type=\"text\" value=\"\">\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group\">\n" +
            "                                               <label>英文名称</label> <input id=\"env_parameter_par_en_name\" name=\"env_parameter_par_en_name\" placeholder=\"输入英文名称\" required=\"\" type=\"text\" value=\"\">\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group\">\n" +
            "                                              <label>参数类型</label>  <select id=\"env_parameter_par_type\" name=\"env_parameter_par_type\" class='env_parameter_select'><option value=\"0\">String</option><option value=\"1\">Number</option><option value=\"2\">Date</option></select>\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group\">\n" +
            "                                             <label>是否必填</label>   <select id=\"env_parameter_par_required\" name=\"env_parameter_par_required\" ><option value=\"0\">必填</option><option value=\"1\">非必填</option></select>\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group par_range_div\">\n" +
            "                                              <label >参数限制范围</label>  <input id=\"env_parameter_par_range\" name=\"env_parameter_par_range\" class='env_parameter_par_range' placeholder=\"输入参数限制范围\" required=\"\" type=\"text\" value=\"\">\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group par_correct_value_div\">\n" +
            "                                            <label >案例参数值</label>    <input id=\"env_parameter_par_correct_value\" name=\"env_parameter_par_correct_value\" class='env_parameter_par_correct_value' placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
            "                                            </div>\n" +
             "<div class=\"form-group par_correct_value_div\">\n" +
            "  <label>参数变量</label>  <input id=\"env_parameter_par_variable\" name=\"env_parameter_par_par_variable\" class=\"env_parameter_par_par_variable\" placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
            "</div>"
            +
            "                \n" +
            "                                    </div></li>";
        $('#parm_ul').append(val);

        // var body_div_index = "panel-body body_div" + index;
        var env_addParm_li = "env_addParm_li" + index;
        $('.env_addParm_li').attr("class", env_addParm_li);
        index++;
    });

    $('#transfer_ul').on("change", "#tra_modules_name", function (e) {
        var val = $(this).val();
        var select_class = $(this).attr('class');
        var num = select_class.substr(select_class.length - 1, 1)
        var tra_env_name_name = "tra_env_name" + num
        var envOptions = getOption("selectEnv", val);
        $("." + tra_env_name_name).find("option").remove();
        $("." + tra_env_name_name).html(envOptions); //获得要赋值的select的id，进行赋值
    });

    $('#btn_env_transfer').click(function () {
        var val = "<li>\n" +
            "                                            <div class=\"form-group\" id=\"env_verification\">\n" +
            "                                                <label>项目</label>\n" +
            "                                                <select id=\"tra_project_name\"\n" +
            "                                                        name=\"tra_project_name\" class='tra_project_name' required=\"\">\n" +
            "                                                    <option value=\"0\">请选择</option>\n" +
            "                                                </select>\n" +
            "                                                <label>模块</label>\n" +
            "                                                <select id=\"tra_modules_name\"\n" +
            "                                                        name=\"tra_modules_name\" class='tra_modules_name' required=\"\">\n" +
            "                                                    <option value=\"0\">请选择</option>\n" +
            "                                                </select>\n" +
            "                                                <label>接口</label>\n" +
            "                                                <select id=\"tra_env_name\"\n" +
            "                                                        name=\"tra_env_name\"\n" +
            "                                                      class='tra_env_name'  required=\"\">\n" +
            "                                                    <option value=\"0\">请选择</option>\n" +
            "                                                </select>\n" +
            "                                                <button type=\"button\" class=\"btn btn-danger del\" >删除</button>\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group\">\n" +
            "                                                <div class=\"panel panel-green\">\n" +
            "                                                    <div class=\"panel-heading\">获取参数区块</div>\n" +
            "                                                    <div class=\"panel-body\">\n" +
            "                                                        <button id=\"btn_add_regexp\" class=\"btn btn-outline btn-link addParm\">\n" +
            "                                                            新增获取参数变量\n" +
            "                                                        </button>\n" +
            "                                                        <div class=\"form-group\" id=\"div_var_regexp\" class='div_var_regexp'>\n" +
            "                                                            <div class=\"form-group\">\n" +
            "                                                                <ul class='addParm_ul'></ul>\n" +
            "                                                            </div>\n" +
            "                                                        </div>\n" +
            "                                                    </div>\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                        </li>";
        $('#transfer_ul').append(val)

        var tar_project_name_index = "tra_project_name" + select_index
        var tra_modules_name_index = "tra_modules_name" + select_index
        var tra_env_name_index = "tra_env_name" + select_index
        var div_var_regexp_index = "div_var_regexp" + select_index
        var addParm_ul_index = "addParm_ul" + select_index
        $('.tra_project_name').attr("class", tar_project_name_index);
        $('.tra_modules_name').attr("class", tra_modules_name_index);
        $('.tra_env_name').attr("class", tra_env_name_index);
        $('.div_var_regexp').attr("class", div_var_regexp_index);
        // $('.addParm').attr("class", addParm_index);
        $('.addParm_ul').attr("class", addParm_ul_index);
        $("." + tar_project_name_index).html(projectOptions); //获得要赋值的select的id，进行赋值
        select_index++;
    });


    $('#btnSubmit').click(function () {

        // var csrftoken = $("meta[name=csrf-token]").attr("content");
        var fromObject = new Object();
        fromObject.env_name = $('#env_name').val();
        fromObject.env_desc = $('#env_desc').val();
        fromObject.env_transmission = $('#env_transmission').val();
        fromObject.env_agreement = $('#env_agreement').val();
        fromObject.env_path = $('#env_path').val();
        fromObject.env_headers = $('#env_headers').val();

        var env_verification_code = $('#env_verification_code').val();
        var env_agreement_relation = $('#env_agreement_relation').val();
        var env_verification_value = $('#env_verification_value').val();
        var env_verification = {};
        env_verification.env_verification_code = env_verification_code;
        env_verification.env_agreement_relation = env_agreement_relation;
        env_verification.env_verification_value = env_verification_value;
        fromObject.env_verification = env_verification;
        fromObject.project_id = $('#project_id').val();
        fromObject.modules_id = $('#modules_id').val();
        fromObject.env_status = $('#env_status').val();
        fromObject.env_complete = $('#env_complete').val();
        fromObject.env_ip = $('#env_ip').val();
        fromObject.env_port = $('#env_port').val();
        //判断有没有调用的接口
        var env_transfer_jsonarray = new Array();
        if ($("select[id^='tra_project_name']").length > 0) {

            // env_transfer_jsonarray = eval('(' + env_transfer_jsonarray + ')');
            for (var i = 0; i < $("select[id^='tra_project_name']").length; i++) {
                var jsonstr = {};
                //项目
                var tra_project_name = $("select[id^='tra_project_name']").eq(i).val()
                //模块
                var tra_modules_name = $("select[id^='tra_modules_name']").eq(i).val()
                //接口
                var tra_env_name = $("select[id^='tra_env_name']").eq(i).val()
                jsonstr.tra_project_name = tra_project_name;
                jsonstr.tra_modules_name = tra_modules_name;
                jsonstr.tra_env_name = tra_env_name;

                //获取参数变量
                var tra_project_name_classname = $("select[id^='tra_project_name']").eq(i).attr('class');
                var var_regexp_length = $("select[class^=" + tra_project_name_classname + "]").parent().siblings().find("input[id^='var_regexp']").length
                var add_regexp_jsonarray = new Array();

                if (var_regexp_length > 0) {
                    console.log('var_regexp_length : ' + var_regexp_length);
                    for (var j = 0; j < var_regexp_length; j++) {
                        var json_regexp = {};
                        var var_regexp = $("select[class^=" + tra_project_name_classname + "]").parent().siblings().find("input[id^='var_regexp']").eq(j).val();
                        var var_variable_name = $("select[class^=" + tra_project_name_classname + "]").parent().siblings().find("input[id^='var_variable_name']").eq(j).val();
                        console.log('var_regexp : ' + var_regexp)
                        json_regexp.var_regexp = var_regexp;
                        json_regexp.var_variable_name = var_variable_name;
                        add_regexp_jsonarray.push(json_regexp);
                    }
                }
                jsonstr.variables = add_regexp_jsonarray;
                env_transfer_jsonarray.push(jsonstr);
            }
        }
        fromObject.env_transfer_jsonarray = env_transfer_jsonarray;


        var parm_jsonarray = new Array();
        //接口参数模块
        if ($("button[id^='btn_del_parm']").length > 0) {
            for (var i = 0; i < $("button[id^='btn_del_parm']").length; i++) {
                var json_parm = {};
                var env_parameter_par_cn_name = $("li[class^='env_addParm_li']").eq(i).find("input[id^='env_parameter_par_cn_name']").val();
                var env_parameter_par_en_name = $("li[class^='env_addParm_li']").eq(i).find("input[id^='env_parameter_par_en_name']").val();
                var env_parameter_par_type = $("li[class^='env_addParm_li']").eq(i).find("select[id^='env_parameter_par_type']").val();
                var env_parameter_par_required = $("li[class^='env_addParm_li']").eq(i).find("select[id^='env_parameter_par_required']").val();
                var env_parameter_par_range = "";
                var env_parameter_par_correct_value = "";
                var env_parameter_par_variable = "";
                var par_date_type = "";
                var par_start_date = "";
                var par_end_date = "";
                env_parameter_par_correct_value = $("li[class^='env_addParm_li']").eq(i).find("input[id^='env_parameter_par_correct_value']").val();
                env_parameter_par_variable = $("li[class^='env_addParm_li']").eq(i).find("input[id^='env_parameter_par_variable']").val();
                if (env_parameter_par_type != "2") {
                    env_parameter_par_range = $("li[class^='env_addParm_li']").eq(i).find("input[id^='env_parameter_par_range']").val();
                } else {
                    //选择日期
                    par_date_type = $("li[class^='env_addParm_li']").eq(i).find("input[id^='par_date_type']").val();
                    par_start_date = $("li[class^='env_addParm_li']").eq(i).find("input[id^='par_start_date']").val();
                    par_end_date = $("li[class^='env_addParm_li']").eq(i).find("input[id^='par_end_date']").val();
                }
                json_parm.par_cn_name = env_parameter_par_cn_name;
                json_parm.par_us_name = env_parameter_par_en_name;
                json_parm.par_type = env_parameter_par_type;
                json_parm.par_required = env_parameter_par_required;
                json_parm.par_range = env_parameter_par_range;
                json_parm.par_correct = env_parameter_par_correct_value;
                json_parm.par_variable = env_parameter_par_variable;
                json_parm.par_date_type = par_date_type;
                json_parm.par_start_date = par_start_date;
                json_parm.par_end_date = par_end_date;
                parm_jsonarray.push(json_parm)
            }

        }
        fromObject.parm_jsonarray = parm_jsonarray;


        var data = JSON.stringify(fromObject);
        $.ajax({
            url: "add",
            type: 'POST',
            dataType: 'json',
            data: data,
            contentType: 'application/json; charset=utf-8',
            headers: {"X-CSRFToken": csrftoken},
            success: function (data) {
                if (data.ok) {
                    window.location.href = window.location.protocol + "//" + window.location.host + "/env/index";
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
        url = path;
    } else {
        url = path + "/" + num;
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


