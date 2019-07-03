$(document).ready(function () {

    var select_index = 0;
    var index = 0;
    var projectOptions = getOption("selectProject", 0);
    var envJson = $('#envJson').val();
    var envJson = eval('(' + envJson + ')');
    var modulesOptions = getOption("selectModular", envJson.project_id);


    $("#project_id").change(function () {
        var val = $("#project_id").val();
        var modulesOptions = getOption("selectModular", val);
        $("#modules_id").find("option").remove();
        $("#modules_id").html(modulesOptions); //获得要赋值的select的id，进行赋值
    });


    $('#env_name').val(envJson.env_name);
    $('#env_desc').val(envJson.env_desc);
    $('#env_transmission').val(envJson.env_transmission);
    $('#env_agreement').val(envJson.env_agreement);
    $("#project_id").html(projectOptions);
    $("#project_id").val(envJson.project_id);
    $("#modules_id").html(modulesOptions);
    $("#modules_id").val(envJson.modules_id);
    $('#env_ip').val(envJson.env_ip);
    $('#env_port').val(envJson.env_port);
    $('#env_path').val(envJson.env_path);
    $('#env_headers').val(envJson.env_headers);
    var env_verification = envJson.env_verification;

    var objs = eval('(' + env_verification + ')');

    $('#env_verification_code').val(objs.env_verification_code);
    $('#env_agreement_relation').val(objs.env_agreement_relation);
    $('#env_verification_value').val(objs.env_verification_value);

    $('#env_id').val(envJson.env_id);
    $('#env_status').val(envJson.env_status);
    $('#env_complete').val(envJson.env_complete);


    var env_transfer_jsonarray = envJson.env_transfer_jsonarray

    env_transfer_jsonarray = eval('(' + env_transfer_jsonarray + ')');

    for (var i = 0, l = env_transfer_jsonarray.length; i < l; i++) {

        var env_transfer_json = env_transfer_jsonarray[i];

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
            "                                                        <div class=\"form-group div_var_regexp\" id=\"div_var_regexp\" >\n" +
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
        $('.addParm_ul').attr("class", addParm_ul_index);
        $("." + tar_project_name_index).html(projectOptions);
        $("." + tar_project_name_index).val(env_transfer_json.project_id);
        var modulesOptions = getOption("selectModular", env_transfer_json.project_id);
        $("." + tra_modules_name_index).html(modulesOptions);
        $("." + tra_modules_name_index).val(env_transfer_json.modules_id);
        var envOptions = getOption("selectEnv", env_transfer_json.modules_id);
        $("." + tra_env_name_index).html(envOptions);
        $("." + tra_env_name_index).val(env_transfer_json.tra_modulated_env_id);


        var variable_jsonarray = eval('(' + env_transfer_json.variable + ')');

        var var_regexp_val = "<li><div class=\"form-group\"> \n" +
            " <input id='var_regexp' name=\"var_regexp\" placeholder=\"输入正则表达式\" class='var_regexp_input'  type=\"text\" value=\"\"> \n" +
            " <input id='var_variable_name' class='var_variable_name_input' name=\"var_variable_name\" placeholder=\"请输入变量名\" type=\"text\" value=\"\"> <button type=\"button\" class=\"btn btn-danger delAdd\" >删除</button>\n" +
            "</div></li>";
        for (var j = 0; j < variable_jsonarray.length; j++) {
            var variable_json = variable_jsonarray[j];
            $('.' + div_var_regexp_index).find('ul').append(var_regexp_val);
            $('.var_regexp_input').attr("class", "var_regexp_input" + j);
            $('.var_variable_name_input').attr("class", "var_variable_name_input" + j);
            $('.' + div_var_regexp_index).find('.var_regexp_input' + j).val(variable_json.var_regexp);
            $('.' + div_var_regexp_index).find('.var_variable_name_input' + j).val(variable_json.var_name);
        }

        select_index++;

    }


    var parm_jsonarray = envJson.parm_jsonarray

    parm_jsonarray = eval('(' + parm_jsonarray + ')');

    for (var i = 0; i < parm_jsonarray.length; i++) {

        var parm_json = parm_jsonarray[i];

        var val = "<li class='env_addParm_li'><button id=\"btn_del_parm\" class=\"btn btn-outline btn-link delParm\">\n" +
            "                                                            删除参数\n" +
            "                                                        </button>" +
            "<div class=\"panel-body  body_div\">\n" +
            "                                        \n" +
            "                                            <div class=\"form-group\">\n" +
            "                                                <label>中文名称</label><input class=\"env_parameter_par_cn_name\" name=\"env_parameter_par_cn_name\" placeholder=\"输入中文名称\" required=\"\" type=\"text\" value=\"\">\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group\">\n" +
            "                                               <label>英文名称</label> <input class=\"env_parameter_par_en_name\" name=\"env_parameter_par_en_name\" placeholder=\"输入英文名称\" required=\"\" type=\"text\" value=\"\">\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group\">\n" +
            "                                              <label>参数类型</label>  <select class=\"env_parameter_par_type\" name=\"env_parameter_par_type\" class='env_parameter_select'><option value=\"0\">String</option><option value=\"1\">Number</option><option value=\"2\">Date</option></select>\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group\">\n" +
            "                                             <label>是否必填</label>   <select class=\"env_parameter_par_required\" name=\"env_parameter_par_required\" ><option value=\"0\">必填</option><option value=\"1\">非必填</option></select>\n" +
            "                                            </div>\n" +
            "                \n" +
            "                                    </div></li>";
        $('#parm_ul').append(val);

        // var body_div_index = "panel-body body_div" + index;
        var env_addParm_li = "env_addParm_li" + index;
        var body_div = "body_div" + index;
        var env_parameter_par_cn_name_input = "env_parameter_par_cn_name" + index;
        var env_parameter_par_en_name_input = "env_parameter_par_en_name" + index;
        var env_parameter_par_type_input = "env_parameter_par_type" + index;
        var env_parameter_par_required_input = "env_parameter_par_required" + index;
        $('.env_addParm_li').attr("class", env_addParm_li);
        $('.body_div').attr("class", body_div);
        $('.env_parameter_par_cn_name').attr("class", env_parameter_par_cn_name_input);
        $('.env_parameter_par_en_name').attr("class", env_parameter_par_en_name_input);
        $('.env_parameter_par_type').attr("class", env_parameter_par_type_input);
        $('.env_parameter_par_required').attr("class", env_parameter_par_required_input);
        $('.' + env_parameter_par_cn_name_input).val(parm_json.par_cn_name);
        $('.' + env_parameter_par_en_name_input).val(parm_json.par_us_name);
        $('.' + env_parameter_par_type_input).val(parm_json.par_type);
        $('.' + env_parameter_par_required_input).val(parm_json.par_required);

        if (parm_json.par_type != "2") {
            //字符串
            var string_type = "<div class=\"form-group par_range_div\">\n" +
                "    <label>参数限制范围</label>  <input class=\"env_parameter_par_range\" name=\"env_parameter_par_range\" class=\"env_parameter_par_range\" placeholder=\"输入参数限制范围\" required=\"\" type=\"text\" value=\"\">\n" +
                "</div>\n" +
                "<div class=\"form-group par_correct_value_div\">\n" +
                "    <label>案例参数值</label>    <input class=\"env_parameter_par_correct_value\" name=\"env_parameter_par_correct_value\" class=\"env_parameter_par_correct_value\" placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
                "</div>" + "<div class=\"form-group par_correct_value_div\">\n" +
                "  <label>参数变量</label>  <input id=\"env_parameter_par_variable\" name=\"env_parameter_par_variable\" class=\"env_parameter_par_variable\" placeholder=\"输入参数变量\" type=\"text\" value=\"\">\n" +
                "</div>";

            $('.' + body_div).append(string_type);
            var env_parameter_par_range_input = "env_parameter_par_range" + index;
            var env_parameter_par_correct_value_input = "env_parameter_par_correct_value" + index;
            var env_parameter_par_variable_input = "env_parameter_par_variable" + index;
            $('.env_parameter_par_range').attr("class", env_parameter_par_range_input);
            $('.env_parameter_par_correct_value').attr("class", env_parameter_par_correct_value_input);
            $('.env_parameter_par_variable').attr("class", env_parameter_par_variable_input);


            $('.' + env_parameter_par_range_input).val(parm_json.par_range);
            $('.' + env_parameter_par_correct_value_input).val(parm_json.par_correct);
            $('.' + env_parameter_par_variable_input).val(parm_json.par_variable);


        } else {
            //日期
            var date_type = "<div class=\"date_div\"><div class=\"form-group \">\n" +
                "<label>日期格式</label><input class=\"par_date_type\" class=\"par_date_type\" name=\"par_date_type\" placeholder=\"日期格式\" type=\"text\" value=\"\">\n" +
                "</div>\n" +
                "<div class=\"form-group\">\n" +
                "    <label>开始时间</label><input class=\"par_start_date\" name=\"par_start_date\" class=\"dateInput\" placeholder=\"开始时间\" type=\"text\" value=\"\">\n" +
                "</div>\n" +
                "<div class=\"form-group\">\n" +
                "  <label>结束时间</label>  <input class=\"par_end_date\" name=\"par_end_date\" class=\"dateInput\" placeholder=\"结束时间\" type=\"text\" value=\"\">\n" +
                "</div>\n" +
                "<div class=\"form-group par_correct_value_div\">\n" +
                "  <label>案例参数值</label>  <input class=\"env_parameter_par_correct_value\" name=\"env_parameter_par_correct_value\" class=\"env_parameter_par_correct_value\" placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
                "</div>" +
                "<div class=\"form-group par_correct_value_div\">\n" +
                "  <label>参数变量</label>  <input id=\"env_parameter_par_variable\" name=\"env_parameter_par_variable\" class=\"env_parameter_par_variable\" placeholder=\"输入参数变量\" type=\"text\" value=\"\">\n" +
                "</div>"
                +
                "</div>";

            $('.' + body_div).append(date_type);
            var par_date_type_input = "par_date_type" + index;
            var par_start_date_input = "par_start_date" + index;
            var par_end_date_input = "par_end_date" + index;
            var env_parameter_par_correct_value_input = "env_parameter_par_correct_value" + index;
            var env_parameter_par_variable_input = "env_parameter_par_variable" + index;
            $('.par_date_type').attr("class", par_date_type_input);
            $('.par_start_date').attr("class", par_start_date_input);
            $('.par_end_date').attr("class", par_end_date_input);
            $('.env_parameter_par_correct_value').attr("class", env_parameter_par_correct_value_input);
            $('.env_parameter_par_variable').attr("class", env_parameter_par_variable_input);


            $('.' + par_date_type_input).val(parm_json.par_date_type);
            $('.' + par_start_date_input).val(parm_json.par_start_date);
            $('.' + par_end_date_input).val(parm_json.par_end_date);
            $('.' + env_parameter_par_correct_value_input).val(parm_json.par_correct);
            $('.' + env_parameter_par_variable_input).val(parm_json.par_variable);
        }
        index++;
    }


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


    $('#transfer_ul').on("click", ".del", function (e) {
        $(this).parent().parent("li").remove();
    });

    $('#transfer_ul').on("click", ".delAdd", function (e) {
        $(this).parent().parent("li").remove();
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


    $('#transfer_ul').on("change", "#tra_modules_name", function (e) {
        var val = $(this).val();
        var select_class = $(this).attr('class');
        var num = select_class.substr(select_class.length - 1, 1)
        var tra_env_name_name = "tra_env_name" + num
        var envOptions = getOption("selectEnv", val);
        $("." + tra_env_name_name).find("option").remove();
        $("." + tra_env_name_name).html(envOptions); //获得要赋值的select的id，进行赋值
    });


    $('#transfer_ul').on("click", ".addParm", function (e) {
        var val = "<li><div class=\"form-group\"> \n" +
            " <input id='var_regexp' name=\"var_regexp\" placeholder=\"输入正则表达式\"  type=\"text\" value=\"\"> \n" +
            " <input id='var_variable_name' name=\"var_variable_name\" placeholder=\"请输入变量名\" type=\"text\" value=\"\"> <button type=\"button\" class=\"btn btn-danger delAdd\" >删除</button>\n" +
            "</div></li>";
        $(this).siblings().find('ul').addClass('addParm_ul').append(val);
    });


    //新增接口参数
    $('#btn_env_addParm').click(function () {
        var val = "<li class='env_addParm_li'><button id=\"btn_del_parm\" class=\"btn btn-outline btn-link delParm\">\n" +
            "                                                            删除参数\n" +
            "                                                        </button>" +
            "<div class=\"panel-body  body_div\">\n" +
            "                                        \n" +
            "                                            <div class=\"form-group\">\n" +
            "                                                <label>中文名称</label><input id=\"env_parameter_par_cn_name\" name=\"env_parameter_par_cn_name\" class='env_parameter_par_cn_name' placeholder=\"输入中文名称\" required=\"\" type=\"text\" value=\"\">\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group\">\n" +
            "                                               <label>英文名称</label> <input id=\"env_parameter_par_en_name\" name=\"env_parameter_par_en_name\" class='env_parameter_par_en_name' placeholder=\"输入英文名称\" required=\"\" type=\"text\" value=\"\">\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group\">\n" +
            "                                              <label>参数类型</label>  <select id=\"env_parameter_par_type\" name=\"env_parameter_par_type\" class='env_parameter_par_type'><option value=\"0\">String</option><option value=\"1\">Number</option><option value=\"2\">Date</option></select>\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group\">\n" +
            "                                             <label>是否必填</label>   <select id=\"env_parameter_par_required\" name=\"env_parameter_par_required\" class='env_parameter_par_required'><option value=\"0\">必填</option><option value=\"1\">非必填</option></select>\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group par_range_div\">\n" +
            "                                              <label >参数限制范围</label>  <input id=\"env_parameter_par_range\" name=\"env_parameter_par_range\" class='env_parameter_par_range' placeholder=\"输入参数限制范围\" required=\"\" type=\"text\" value=\"\">\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group par_correct_value_div\">\n" +
            "                                            <label >案例参数值</label>    <input id=\"env_parameter_par_correct_value\" name=\"env_parameter_par_correct_value\" class='env_parameter_par_correct_value' placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
            "                                            </div>\n" +
            "<div class=\"form-group par_correct_value_div\">\n" +
                "  <label>参数变量</label>  <input id=\"env_parameter_par_variable\" name=\"env_parameter_par_variable\" class=\"env_parameter_par_variable\" placeholder=\"输入参数变量\" type=\"text\" value=\"\">\n" +
                "</div>"+
            "                \n" +
            "                                    </div></li>";
        $('#parm_ul').append(val);

        // var body_div_index = "panel-body body_div" + index;
        var env_addParm_li = "env_addParm_li" + index;
        var env_parameter_par_cn_name_input = "env_parameter_par_cn_name" + index;
        var env_parameter_par_en_name_input = "env_parameter_par_en_name" + index;
        var env_parameter_par_type_select = "env_parameter_par_type" + index;
        var env_parameter_par_required_input = "env_parameter_par_required" + index;
        var env_parameter_par_range_input = "env_parameter_par_range" + index;
        var env_parameter_par_correct_value_input = "env_parameter_par_correct_value" + index;
        var env_parameter_par_variable_input = "env_parameter_par_variable" + index;


        $('.env_addParm_li').attr("class", env_addParm_li);
        $('.env_parameter_par_cn_name').attr("class", env_parameter_par_cn_name_input);
        $('.env_parameter_par_en_name').attr("class", env_parameter_par_en_name_input);
        $('.env_parameter_par_type').attr("class", env_parameter_par_type_select);
        $('.env_parameter_par_required').attr("class", env_parameter_par_required_input);
        $('.env_parameter_par_range').attr("class", env_parameter_par_range_input);
        $('.env_parameter_par_correct_value').attr("class", env_parameter_par_correct_value_input);
        $('.env_parameter_par_variable').attr("class", env_parameter_par_variable_input);

        index++;
    });


    $('#parm_ul').on("click", ".delParm", function (e) {
        $(this).parent("li").remove();
    });


    //参数类型选择
    $('#parm_ul').on("change", "select[name=env_parameter_par_type]", function (e) {


        var valHtml = "<div class='date_div'><div class=\"form-group \">\n" +
            "<label>日期格式</label><input id=\"par_date_type\" class='par_date_type' name=\"par_date_type\" class='dateInput par_date_type' placeholder=\"日期格式\" type=\"text\" value=\"\">\n" +
            "</div>\n" +
            "<div class=\"form-group\">\n" +
            "    <label>开始时间</label><input id=\"par_start_date\" name=\"par_start_date\" class='dateInput par_start_date'  placeholder=\"开始时间\" type=\"text\" value=\"\">\n" +
            "</div>\n" +
            "<div class=\"form-group\">\n" +
            "  <label>结束时间</label>  <input id=\"par_end_date\" name=\"par_end_date\" class='dateInput par_end_date' placeholder=\"结束时间\" type=\"text\" value=\"\">\n" +
            "</div>\n" +
            "<div class=\"form-group par_correct_value_div\">\n" +
            "  <label>案例参数值</label>  <input id=\"env_parameter_par_correct_value\" name=\"env_parameter_par_correct_value\" class=\"env_parameter_par_correct_value\" placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
            "</div>" +
            "<div class=\"form-group par_correct_value_div\">\n" +
                "  <label>参数变量</label>  <input id=\"env_parameter_par_variable\" name=\"env_parameter_par_variable\" class=\"env_parameter_par_variable\" placeholder=\"输入参数变量\" type=\"text\" value=\"\">\n" +
                "</div>"+
            "</div>";
        var val = $(this).val();
        var num = $(this).attr("class").match(/\d+/);
        if (val == '2') {
            //选择了 date
            $(this).parent().parent().find(".par_correct_value_div").remove();
            $(this).parent().parent().find(".par_range_div").remove();
            $(this).parent().parent().append(valHtml);


            var par_date_type_input = "par_date_type" + num;
            var par_start_date_input = "par_start_date" + num;
            var par_end_date_input = "par_end_date" + num;
            var env_parameter_par_correct_value_input = "env_parameter_par_correct_value" + num;
            var env_parameter_par_variable_input = "env_parameter_par_variable" + index;
            $('.par_date_type').attr("class", par_date_type_input);
            $('.par_start_date').attr("class", par_start_date_input);
            $('.par_end_date').attr("class", par_end_date_input);
            $('.env_parameter_par_correct_value').attr("class", env_parameter_par_correct_value_input);
            $('.env_parameter_par_variable').attr("class", env_parameter_par_variable_input);


        } else {
            if ($(this).parent().siblings().find('input[name=par_date_type]').length == 1) {//js判断元素是否存在
                valHtml = "<div class=\"form-group par_range_div\">\n" +
                    "  <label >参数限制范围</label><input id=\"env_parameter_par_range\" name=\"env_parameter_par_range\" class=\"env_parameter_par_range\" placeholder=\"输入参数限制范围\" required=\"\" type=\"text\" value=\"\">\n" +
                    "</div>\n" +
                    "<div class=\"form-group par_correct_value_div\">\n" +
                    "  <label >案例参数值</label>  <input id=\"env_parameter_par_correct_value\" name=\"env_parameter_par_correct_value\" class=\"env_parameter_par_correct_value\" placeholder=\"输入案例参数值\" type=\"text\" value=\"\">\n" +
                    "</div>"+"<div class=\"form-group par_correct_value_div\">\n" +
                "  <label>参数变量</label>  <input id=\"env_parameter_par_variable\" name=\"env_parameter_par_variable\" class=\"env_parameter_par_variable\" placeholder=\"输入参数变量\" type=\"text\" value=\"\">\n" +
                "</div>";
                // $(this).parent().siblings().find('input[class=dateInput]').remove();
                $(this).parent().parent().find(".date_div").remove();
                $(this).parent().parent().append(valHtml);
                var env_parameter_par_range_input = "env_parameter_par_range" + num;
                var env_parameter_par_correct_value_input = "env_parameter_par_correct_value" + num;
                var env_parameter_par_variable_input = "env_parameter_par_variable" + index;
                $('.env_parameter_par_range').attr("class", env_parameter_par_range_input);
                $('.env_parameter_par_correct_value').attr("class", env_parameter_par_correct_value_input);
                $('.env_parameter_par_variable').attr("class", env_parameter_par_variable_input);
            }
        }

    });


    $('#btnSubmit').click(function () {
        var csrftoken = $("meta[name=csrf-token]").attr("content");
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
        fromObject.env_id = $('#env_id').val();
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
                var tra_project_name_classname = $("select[id^='tra_project_name']").eq(i).attr('class')
                var var_regexp_length = $("select[class^=" + tra_project_name_classname + "]").parent().siblings().find("input[id^='var_regexp']").length
                var add_regexp_jsonarray = new Array();

                if (var_regexp_length > 0) {
                    for (var j = 0; j < var_regexp_length; j++) {
                        var json_regexp = {};
                        var var_regexp = $("select[class^=" + tra_project_name_classname + "]").parent().siblings().find("input[id^='var_regexp']").eq(j).val();
                        var var_variable_name = $("select[class^=" + tra_project_name_classname + "]").parent().siblings().find("input[id^='var_variable_name']").eq(j).val();
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
                var env_addParm_li = "env_addParm_li" + i;
                var env_parameter_par_cn_name = $("." + "env_parameter_par_cn_name" + i).val();
                var env_parameter_par_en_name = $("." + "env_parameter_par_en_name" + i).val();
                var env_parameter_par_type = $("." + "env_parameter_par_type" + i).val();
                var env_parameter_par_required = $("." + "env_parameter_par_required" + i).val();
                var env_parameter_par_range = "";
                var env_parameter_par_correct_value = "";
                var env_parameter_par_variable = "";
                var par_date_type = "";
                var par_start_date = "";
                var par_end_date = "";
                env_parameter_par_correct_value = $("." + "env_parameter_par_correct_value" + i).val();
                env_parameter_par_variable = $("." + "env_parameter_par_variable" + i).val();
                if (env_parameter_par_type != "2") {
                    env_parameter_par_range = $("." + "env_parameter_par_range" + i).val();
                } else {
                    //选择日期
                    par_date_type = $("." + "par_date_type" + i).val();
                    par_start_date = $("." + "par_start_date" + i).val();
                    par_end_date = $("." + "par_end_date" + i).val();
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

        var url = window.location.protocol + "//" + window.location.host + "/env/update";
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
                    window.location.href = window.location.protocol + "//" + window.location.host + "/env/index";
                }

            }
        });
    });


});


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