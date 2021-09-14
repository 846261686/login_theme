/**
 * Created by artorias on 2018/12/6.
 */
layui.use(['form'], function () {
    var form = layui.form;
});
$(document).ready(function(){
    if (window.cefQuery) {
        window.cefQuery({
            request: JSON.stringify({
                cmd: "get_auto_login_info"
            }),
            persistent: false,
            onSuccess: function (response) {
                var info = JSON.parse(response)
                var auto_login = info.autoLogin
                if(auto_login) {
                    $("#uesr_login_name").val(info.userName)
                    $("#uesr_login_password").val(info.password)
                    $("#login_submit").click()
                } 
            },
            onFailure: function (error_code, error_message) { }
        })
    }
}); 


