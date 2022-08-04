function login() {
    url = "login"
    data = {
        "username":  window.btoa(oUser.value),
        "pwd":  window.btoa(oPswd.value),
        "oreb":oRemember.checked
    }
    var Url = HOST + url
    setCookie('usern', oUser.value, 30);
    setCookie('pswd', oPswd.value, 30);
    data = JSON.stringify(data)
    $.post(Url, data)
        .done(function (data) {
            jsondata = JSON.parse(data)
            if (jsondata.Result) {
                window.location.replace(HOST);
            }
            else{alert("username && password error!")}
        })
        .fail(function (xhr, errorText, errorType) {
            if (errorText) {
                alert("Network Error !")
            }
        });
}


window.onload = function () {
    oUser = document.getElementById('user');
    oPswd = document.getElementById('pswd');
    oRemember = document.getElementById('remember');
    //页面初始化时，如果帐号密码cookie存在则填充
    if (getCookie('usern') && getCookie('pswd')) {
        oUser.value = getCookie('usern');
        oPswd.value = getCookie('pswd');
        oRemember.checked = true;
    }
    //复选框勾选状态发生改变时，如果未勾选则清除cookie
    oRemember.onchange = function () {
        if (!this.checked) {
            delCookie('usern');
            delCookie('pswd');
        }
    };
};

//设置cookie
function setCookie(name, value, day) {
    var date = new Date();
    date.setDate(date.getDate() + day);
    document.cookie = name + '=' + window.btoa(value) + ';expires=' + date;
};

//获取cookie
function getCookie(name) {
    var reg = RegExp(name + '=([^;]+)');
    var arr = document.cookie.match(reg);
    if (arr) {
        return window.atob(arr[1]);
    } else {
        return '';
    }
};

//删除cookie
function delCookie(name) {
    setCookie(name, null, -1);
};


$(function () {
    $(".login-page").keypress(function (event) {
        if (event.which === 13) {
            $('.login').click()
        }
    })
})


function showp(e) {
    var password = document.getElementById('pswd');
    if (password.type === 'password') {
        password.setAttribute('type', 'text');
    } else {
        password.setAttribute('type', 'password');
    }
}