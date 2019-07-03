###interface-master轻量级便捷接口自动化平台###
目前还有很多缺憾，请各位大神多提提意见，进一步修改。
包含五个功能 项目管理，模块管理，接口管理，用例执行，定时任务
#####其核心设计目标#####
自动生成接口测试用例,解决接口测试人员花费太多的时间去编写,接口参数是否必填,参数数据类型限制,参数数据类型自身的数据范围值限制等用例

#####开发环境#####
环境：python3.6   
后端框架：
WEB框架：python-flask
登录鉴权：Flask-JWT
数据库：Flask-SQLAchemy
定时调度：Flask-APScheduler
Execl操作：openpyxl
虚拟数据 ：Faker
邮件：Flask-Mail


#####运行项目#####
后端运行：
进入interface-master目录 执行  flask initdb  创建表格

执行  flask forge  生成默认的项目和模块数据，管理员账号密码   admin/admin

执行  flask run 运行项目


配置邮箱：


前端运行：
安装 Node.js环境 
进入interface目录 
执行 npm install 加载资源
执行 npm run dev 运行项目
如npm加载太慢请使用cnpm


#####使用流程介绍#####
*  登录   账号密码  admin/admin




新增项目和新增模块就不用多说了，主要说下新增接口
######接口测试配置######
<font color='#777'>
*案例：
 > url:  http://127.0.0.1:7777/jia
 > herder : content-Type :application/json;charset=UTF-8
 > 协议: POST
 > 参数: {"a":"11","a1":"10"}
 > 响应信息：
 > {'msg': '请求成功 ', 'msg_code': 1000, 'a_list': '3333'}
 > msg_code:1000 请求成功的code
 > 限制条件：
 >  > 1. a，a1必填 
 >  > 2. a ,a1  int类型可输入范围 1-100
 >  以下开始配置：
 > 1.Body 输入整个请求参数结构，需要测试的参数值设置变量${变量名称} 
</font>
 >  > 
<font color='#777'>
 > 2. 点击新增参数，填写相对应的内容
</font>
 >  > 
<font color='#777'>
 > 3. 如一个广告接口，01 表示投放某个版面位置， 02表示投放某个版面位置
 >  > 这时候的测试案例参数值就有两个 01和02
 >  > 案例参类型 选择- 列表 
 >  > 案例参数值 ['01','02']
</font>
 >  > 
<font color='#777'>
 > 案例2 ：接口B需要登录后的token才能请求
 >  > 1. 新增一个登录接口
 >  > 2.新增接口B时点击新增调用接口按钮
 >  > 选择需要调用接口的项目名称，模块名称，接口名称
</font>
 >  > 
<font color='#777'>
 >  > 获取登录成功后的token
 >  > 如：登录接口请求成功返回信息如下
 >  > {"resultCode":"0000000000","resultMsg":"正常","resultData":{"token":"fsfsdfj22320023"}
 >  > 返回路径填写：resultData.token
 >  > 
 >  > 我们只需在需要用到token的地方填写${token}就可以了


> 如Get请求 Body填写方式

</font>

* 结果校验
如返回信息 {'msg': '请求成功 ', 'msg_code': 1000}
如  msg_code = 1000 表示该接口请求通过
校验路径只需如下填写

如返回信息 
{'msg': '请求成功 ', 'msgList': [{"a":10,"b":11},{"a":"11","b":12}]}
msgList 第一个 a =10表示正确
校验路径只需如下填写


##### CASE新增与执行 #####

> 查看case执行日志



* 新增调度


> 查看调度日志










