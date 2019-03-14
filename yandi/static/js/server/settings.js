$(function () {
    $(".update-thread-config").click(function () {
        const poc_thread = $('[id="poc_thread"]').val();
        const discovery_thread = $('[id="discovery_thread"]').val();
        const mail_port = $('[id="mail_port"]').val();
        const subdomain_thread = $('[id="subdomain_thread"]').val();
        const port_thread = $('[id="port_thread"]').val();
        const auth_tester_thread = $('[id="auth_tester_thread"]').val();
        const discovery_time = $('[name="discovery_time_val"]').val();
        if (!poc_thread||!poc_thread || !discovery_thread || !subdomain_thread || !port_thread || !discovery_time) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "poc_thread": poc_thread,
                "mail_port": mail_port,
                "discovery_thread": discovery_thread,
                "subdomain_thread": subdomain_thread,
                "port_thread": port_thread,
                "auth_tester_thread": auth_tester_thread,
                "discovery_time": discovery_time,
                "source": "thread_settings",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Updated Successfully!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/advanced-option";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });
    $(".update-todo-config").click(function () {
        const todotext = $('[id="todotext"]').val();
        if (!todotext) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/todo', {
                "todotext": todotext,
                "source": "todo",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Updated Successfully!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/todo";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });
    $(".update-github-config").click(function () {
        const gituser = $('[id="github_user"]').val();
        const gitpassword = $('[id="github_password"]').val();
        const gitpage = $('[id="github_page"]').val();
        if (!gituser || !gitpassword) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "github_user": gituser,
                "github_password": gitpassword,
                "github_page": gitpage,
                "source": "github_settings",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Updated Successfully!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/advanced-option";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });

    $(".update-subdomain-dict-config").click(function () {
        const subdomain_dict_2 = $('[id="subdomain_dict_2"]').val();
        const subdomain_dict_3 = $('[id="subdomain_dict_3"]').val();
        if (!subdomain_dict_2 || !subdomain_dict_3) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "subdomain_dict_2": subdomain_dict_2,
                "subdomain_dict_3": subdomain_dict_3,
                "source": "subdomain_dict"
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Successfully Update!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/advanced-option";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });

    $(".update-user-passwd").click(function () {
        const username_list = $('[id="username_list"]').val();
        const password_list = $('[id="password_list"]').val();
        if (!username_list || !password_list) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "username_list": username_list,
                "password_list": password_list,
                "source": "auth"
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Successfully Update!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/advanced-option";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });
    //mail user password update
    $(".update-mail-user-passwd").click(function () {
        const mail_user_dict = $('[id="mail_user_dict"]').val();
        const mail_password_dict = $('[id="mail_password_dict"]').val();
        if (!mail_user_dict || !mail_password_dict) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "username_list": mail_user_dict,
                "password_list": mail_password_dict,
                "source": "mail-user-password"
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Successfully Update!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/advanced-option";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });
    $(".update-port-config").click(function () {
        const port_list = $('[id="port_list"]').val();
        if (!port_list) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "port_list": port_list,
                "source": "port_list"
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Updated Successfully!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/advanced-option";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });

});
