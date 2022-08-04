function add(tag, data) {
    var $td = $(tag + " tr:last").clone();
    $(tag).append($td);
    var $tr = $(tag + " tr:last")
    $tr.css({display: "block"})
    if (data.size!=0){
    $tr.find(".filen").html('<a  href="#" onclick="getfile(this)"> ' + data.file + ' </a>' +'<div style="display: contents;color: black;position: absolute;float: right;font-size: 0.8em !important;">'+data.size+'  '+data.lstime+'</div>' )
}else{$tr.find(".filen").html('<a id="dir"  href="#" onclick="getfile(this)"> ' + data.file + ' </a>'+'<div style="display: contents;color: black;position: absolute;float: right;font-size: 0.8em !important;"> '+data.lstime+'</div>' )}
}

function addd(tag, data) {
    var $td = $(tag + " li:last").clone()
    $(tag).append($td);
    var $tr = $(tag + " li:last")
    $tr.css({display: "flex"})
    $tr.html('<a  href="#" style="white-space:nowrap" onclick="getfilen(this)"> ' + data + ' </a>')
}

function del(tag) {
    $(tag + " tr:last").remove();
}

function getfilen(e) {
    fouce = $(e).text().replace(/^\s+|\s+$/g, "")
    filename = parent.split(fouce)[0] + fouce
    getfile(e, filename)
}
Url_=HOST+'uploadfiles/'
parent = ''
flag=false

function getfile(e = null, filename = null) {
    const url = "downloadfile/"
    if (e) {
        if (filename == null) {
            filename = $(e).text()
            filename = filename.replace(/^\s+|\s+$/g, "")
            if (parent) {
                Url = url + parent + '/' + filename
            } else {
                Url = url + filename
            }
        } else {
            Url = url + filename
        }
    } else {
        Url=url
    }
    get(Url)

    function get(url) {
        $.get(url)
            .done(function (data) {
                if (data) {
                    jsondata = JSON.parse(data)
                    if (jsondata.parent) {
                        parent = jsondata.parent
                        Url_=HOST+'uploadfiles/'+parent
                        while ($(".d tr").length > 1) {
                            del('.d')
                        }
                        $('.r').css({display: "none"})
                        parent.split('/').forEach(e => {
                            addd('.d', e)
                        });
                    } else {
                    }

                    if (!jsondata.Result) {
                        filedownload(url, filename)
                    } else {
                        content = jsondata.Content
                        while ($(".t tr").length > 1) {
                            del('.t')
                        }
                        $('#col').css({display: "none"})
                        content.forEach(e => {
                            add('.t', e)
                        });
                    }
                }
            })
            .fail(function (xhr, errorText) {
                if (xhr.status == '402') {
                    window.location.replace(HOST + "login");
                }
            });
    }

}


function signout(e){
    $.get(HOST + 'logout')
    .done(function (data) {
        jsondata = JSON.parse(data)
        if (jsondata.Result) {
            window.location.replace(HOST + "login")
        }
    })
    .fail(function (xhr, errorText) {
        if (xhr.status == '402') {
            window.location.replace(HOST + "login");
        }
    });
}


$(document).ready(function() {
     var $ = jQuery,
        $list = $('#thelist'),
        $btn = $('.upfile'),
        state = 'pending',
        uploader;
        var task_id = WebUploader.Base.guid();        //产生task_id
        var uploader = WebUploader.create({           //创建上传控件
            swf: "{{static_url('webuploader/Uploader.swf')}}", //swf位置，这个可能与flash有关
            server: Url_,                             //接收每一个分片的服务器地址
            pick: '#picker',                          //填上传按钮的id选择器值
            auto: false,                               //选择文件后，是否自动上传
            chunked: true,                            //是否分片
            chunkSize: 20 * 1024 * 1024,              //每个分片的大小，这里为20M
            chunkRetry: 3,                            //某分片若上传失败，重试次数
            threads: 10,                               //线程数量，考虑到服务器，这里就选了1
            duplicate: true,                          //分片是否自动去重
            // accept: {
            // title: 'Images',
            // extensions: 'gif,jpg,jpeg,bmp,png,txt',
            // mimeTypes: 'image/*'
            // },
            formData: {                               //每次上传分片，一起携带的数据
                task_id: task_id,
            },
        });

        uploader.on( 'fileQueued', function( file ) {
        if (parent){
            $('.filename').text(file.name)
        }
        $btn.click()
    });

        uploader.on('startUpload', function() {       //开始上传时，调用该方法
            $('.progress-bar').css('width', '0%');
            $('.progress-bar').text('0%');
        });

        uploader.on('uploadProgress', function(file, percentage) { //一个分片上传成功后，调用该方法
            $('.progress-bar').css('width', percentage * 100 - 1 + '%');
            $('.progress-bar').text(Math.floor(percentage * 100 - 1) + '%');
        });

        uploader.on('uploadSuccess', function(file) { //整个文件的所有分片都上传成功，调用该方法
            var data = {'task_id': task_id, 'filename': file.source['name'] ,'parent':parent};
            msg=''
            $.post(HOST+'upload_success', data).done(function (data) {
            jdata = JSON.parse(data)
            if (jdata.result) {
                msg=jdata.message
                $('.progress-bar').css('width', '100%');
                $('.progress-bar').text(msg);
            }})
    .fail(function (xhr, errorText) {
        msg='上传失败'});          //ajax携带data向该url发请求
        $('.progress-bar').css('width', '100%');
            $('.progress-bar').text(msg);
        });

        uploader.on('uploadError', function(file) {   //上传过程中发生异常，调用该方法
            $('.progress-bar').css('width', '100%');
            $('.progress-bar').text('上传失败');
        });

        uploader.on('uploadComplete', function(file) {//上传结束，无论文件最终是否上传成功，该方法都会被调用
            $.post(HOST+'upload_success')
            $('.progress-bar').removeClass('active progress-bar-striped');
        });

        $btn.on( 'click', function() {
            if(!parent){window.alert('该目录下不允许操作') }
            else if (parent  && $('.filename').text()){
                uploader.upload();
            }else{window.alert('没有选择文件')}
            });
    });

// function upfile(){
//                 if(!parent){window.alert('该目录下不允许操作') }
//             else if (parent  && $('.filename').text()){
//                 uploader.upload();
//             }else{window.alert('没有选择文件')}
// }


$(function () {
    var file = "";
    var fileName = "";
    var fileExt = "";
    $(".fileupload").change(function () {
        //获取文件的value值
        file = $(".fileupload").val()
        fileName = file.split("\\").pop();
        if (fileName) {
            $(".textN").css({display: "inline"})
        } else {
            $(".textN").css({display: "none"})
        }
    })
});

(function($) {
    $.fn.filesUpload = function(opts) {
        var defaults = {
            url: '',
            multiple: true,
            accept: '',
            waiiflie:'',
            fileTypes: '',
            buttonText: '选择文件',
            irmeprocess: '<li id="${fileID}file"><div class="progress"><div class="progressbar"></div></div><span class="filename">${fileName}</span><span class="progressnum">0/${fileSize}</span><a class="uploadbtn">上传</a><a class="delfilebtn">删除</a></li>',
            filehtml: '<span class="selfbutton"><span class="selftext"></span><input type="file" id="FileUploadSelf" class="selfinput" /></span>',
            onUploadStart: function() {},
            onUploadSuccess: function() {},
            onUploadComplete: function() {},
            onUploadError: function() {},
            onInit: function() {},
        }
        var option = $.extend(defaults, opts);
        var _self = this
        var obj = {
            init: function() {
                _self.append(option.filehtml)
                _self.find(".selftext").text(option.buttonText)
                this.fileInput = _self.find(".selfinput")[0]
                if(option.accept && option.accept != '') {
                    _self.find(".selfinput").attr("accept", option.accept)
                }
                if(option.multiple) {
                    _self.find(".selfinput").attr("multiple", "multiple")
                }
                this.onChange()
            },
            onChange: function() {
                var that = this
                this.fileInput.addEventListener("change", function(e) {
                    var files = e.target.files || e.dataTransfer.files;
                    var filterfile = that.filter(files)
                    option.fileChangeEnd(filterfile);
                    if(option.autoUpload){
                        option.waiiflie=filterfile
                        that.uploadBtn()
                    }else{
                        that.upload(filterfile)
                    }
                }, false);
            },
            uploadBtn:function(){
                var that = this
                if(!$(option.autoUpload) || $(option.autoUpload).length==0){
                    console.log("找不到"+option.autoUpload)
                    return false;
                }
                $("body").on("click",option.autoUpload,function(){
                    that.upload(option.waiiflie)
                })
            },
            upload: function(files) {
                var html = '',
                    that = this,
                    timing=new Date().getTime()
                _self.append(html)
                var data
                for(var j = 0; j < files.length; j++) {
                    var formData = new FormData();
                    formData.append("file", files[j]); //加入文件对象
                    data = formData;
                    that.send(timing,j,data)
                }
            },
            send:function(timing,index,file){
                var xhr = new XMLHttpRequest();
                if(xhr.upload) {
                    xhr.upload.addEventListener("progress", function(e) {
                        var percent = (e.loaded / e.total*100).toFixed(2);
                        $('.fileprocessbox[name='+(timing+''+index)+']').find(".fileprocess div").width(percent+"%")
                        var size=(parseFloat($('.fileprocessbox[name='+(timing+''+index)+']').find(".size").text())*percent/100).toFixed(2)
                        var texts=$('.fileprocessbox[name='+(timing+''+index)+']').find(".size").text()
                        var unit=texts.replace(/\d+(\.\d+)/g,'')
                        $('.fileprocessbox[name='+(timing+''+index)+']').find(".currentsize").text(size+unit)
                    }, false);
                    xhr.onreadystatechange = function(e) {
                        if(xhr.readyState == 4) {
                            if(xhr.status == 200) {
                                option.onUploadSuccess(xhr, xhr.responseText);
                                option.onUploadComplete();
                            } else {
                                option.onUploadError(xhr, xhr.responseText);
                            }
                            var FileUploadSelf = document.getElementById('FileUploadSelf');
                            FileUploadSelf.value = ''
                        }
                        option.waiiflie=''
                    };
                    option.onUploadStart();
                    xhr.open("POST", Url_, true);
                    xhr.send(file);
                }
            },
            getSize: function(size) {
                var s
                if(size < 1024) {
                    s = size + "B"
                } else {
                    s = size / 1024 >= 1024 ? (size / 1048576).toFixed(2) + 'M' : (size / 1024).toFixed(2) + "KB"
                }
                return s
            },
            filter: function(files) {
                var fileType = option.fileTypes ? option.fileTypes.split(",") : '',
                    result = []
                if(fileType) {
                    for(var i = 0; i < files.length; i++) {
                        var fileExtension=files[i].name.substring(files[i].name.lastIndexOf('.') + 1);
                        if(fileType.indexOf(fileExtension) > -1) {
//                      if(fileType.indexOf(files[i].type.split("/")[1]) > -1) {
                            result.push(files[i])
                        } else {
                            result = []
                            alert("上传类型不对！")
                            break;
                            return false;
                        }
                    }
                } else {
                    result = files
                }
                return result
            }
        }
        obj.init()
    }
})(jQuery)

// function filedownload(Url, filename) {
//     var xhr = new XMLHttpRequest();
//     xhr.open('POST', Url, true);
//     xhr.responseType = "blob";
//     xhr.setRequestHeader("user",window.atob(getCookie('usern')));
//     xhr.onload = function () {
//         if (this.status === 200) {
//             var blob = this.response;
//             var reader = new FileReader();
//             reader.readAsDataURL(blob);
//             reader.onload = function (e) {
//                 var a = document.createElement('a');
//                 a.download = filename;
//                 a.href = e.target.result;
//                 $("body").append(a);
//                 a.click();
//                 $(a).remove();
//             }
//         }
//     };
//     xhr.send()
// }

function filedownload(Url, filename) {
        const url = HOST+Url
        if (!url || !/http?/.test(url)) return;
        download({
          url,
          chunkSize: 1024 * 1024 * 20,
          poolLimit: 10,
        }).then((buffers) => {
          saveAs({ buffers, name: filename, mime: "application/zip" });
        });
      }



window.onload = function () {
    getfile()
}



// function selectfile(){
//     // $("#FileUploadSelf").click()
//     // $("#picker").click()
//     if(parent){
//     $("#picker").click()
//     }else{
//         window.alert(1111111111111111)
//     }
// }


$(".fileupload").filesUpload({
    url: Url_,//上传地址
    multiple: true,  //是否多文件上传
    accept: '', //input accept属性
    fileTypes: '',//文件格式
    buttonText: '',  //按钮文字
    autoUpload: '',
    fileChangeEnd: function (file) {
    },
    onUploadStart: function () {
    },
    onUploadSuccess: function (res, data) {
        var jsondata = JSON.parse(data);
        if (jsondata.result && jsondata.message=='succeeful') {
            UploadResult = true
            add('.t', jsondata.data)
            loadingRemove()
        }
        else if (jsondata.result){window.alert(jsondata.message)}else{window.alert('文件上传失败')}
        UploadResult = true;
        loadingRemove();
    },
    onUploadComplete: function () {
        loadingRemove()
    },
    onUploadError: function (res, xhr) {//请求错误
        loadingRemove()
        if (res.status == '402') {
            window.location.replace(HOST + "login");
        }
        window.alert('文件上传失败')
    }
})



function timestampToTime(timestamp) {
      var date = new Date(timestamp);
      var Y = date.getFullYear() + "-";
      var M =
        (date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1) + "-";
      var D = date.getDate() < 10 ? "0" + date.getDate() : date.getDate() + " ";
      var text = " ";
      var hh =
        date.getHours() < 10 ? "0" + date.getHours() : date.getHours() + ":";
      var mm =
        date.getMinutes() < 10
          ? "0" + date.getMinutes()
          : date.getMinutes() + ":";
      var ss =
        date.getSeconds() < 10 ? "0" + date.getDate() : date.getSeconds();
      return Y + M + D + text + hh + mm + ss;
    }

function loadingShow(title, discription) {
    $('body').loading({
        loadingWidth: 240,
        title: title,
        name: 'uploadf',
        discription: discription,
        direction: 'column',
        type: 'origin',
        originBg: '#71EA71',
        originDivWidth: 40,
        originDivHeight: 40,
        originWidth: 6,
        originHeight: 6,
        smallLoading: false,
        loadingMaskBg: 'rgba(0,9,168,0.2)'
    });
}


function loadingRemove() {
    setTimeout(function () {
        removeLoading('uploadf');
    }, 200);
}

function createdir() {
        if($('.dir').css('display')=='none'){$('.dir').css({'display':'block'})}
}

$('#diri').on('blur',function(){
    $('.dir').css('display','none')
    data={'dir':$('#diri').val()}
    $.post(HOST + 'createdir/'+parent,JSON.stringify(data))
        .done(function (data) {
            jsondata = JSON.parse(data)
            if (jsondata.result && jsondata.message=='succeeful') {
                add('.t',jsondata.data)
            }  else if(jsondata.result){window.alert(jsondata.message)} else {window.alert('文件夹创建失败')}
        })
        .fail(function (xhr, errorText) {
            if (xhr.status == '402') {
                window.location.replace(HOST + "login");
    }
 });
})

function getCookie(name){
    var reg = RegExp(name+'=([^;]+)');
    var arr = document.cookie.match(reg);
    if(arr){
        return arr[1];
    }else{
        return '';
    }
};


function concatenate(arrays) {
  if (!arrays.length) return null;
  let totalLength = arrays.reduce((acc, value) => acc + value.length, 0);
  let result = new Uint8Array(totalLength);
  let length = 0;
  for (let array of arrays) {
    result.set(array, length);
    length += array.length;
  }
  return result;
}

function getContentLength(url) {
  return new Promise((resolve, reject) => {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.setRequestHeader("user",window.atob(getCookie('usern')));
    xhr.send();
    xhr.onload = function () {
      resolve(
        // xhr.getResponseHeader("Accept-Ranges") === "bytes" &&
        xhr.getResponseHeader("ContentLength")
      );
    };
    xhr.onerror = reject;
  });
}

function progress_bar(flag,percentage){
    if (!flag){
        $('.progress-bar').removeClass('active progress-bar-striped');
        $('.progress-bar').css('width', '0%');
        $('.progress-bar').text('0%');
    }else{
    $('.progress-bar').css('width', percentage * 100  + '%');
    $('.progress-bar').text(Math.floor(percentage * 100 ) + '%');
    if(percentage===1){$('.progress-bar').text('下载完成');}
}}

function getBinaryContent(url, start, end,chunkSize, i) {
  return new Promise((resolve, reject) => {
    try {
      let xhr = new XMLHttpRequest();
      xhr.open("POST", url, true);
      xhr.setRequestHeader("user",window.atob(getCookie('usern')));
      xhr.setRequestHeader("range", `bytes=${start}-${end}`); // 请求头上设置范围请求信息
      xhr.setRequestHeader("start", `${start}`);
      xhr.setRequestHeader("chunkSize", `${chunkSize}`);
      xhr.responseType = "arraybuffer"; // 设置返回的类型为arraybuffer
      xhr.onload = function () {
        resolve({
          index: i, // 文件块的索引
          buffer: xhr.response, // 范围请求对应的数据
        });
      };
      xhr.send();
    } catch (err) {
      reject(new Error(err));
    }
  });
}

function saveAs({ name, buffers, mime = "application/octet-stream" }) {
  const blob = new Blob([buffers], { type: mime });
  const blobUrl = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.download = name || Math.random();
  a.href = blobUrl;
  a.click();
  URL.revokeObjectURL(blob);
  progress_bar(0,0);
}

async function asyncPool(poolLimit, array, iteratorFn) {
  const ret = []; // 存储所有的异步任务
  const executing = []; // 存储正在执行的异步任务
  for (const item of array) {
    // 调用iteratorFn函数创建异步任务
    const p = Promise.resolve().then(() => iteratorFn(item, array));
    ret.push(p); // 保存新的异步任务

    // 当poolLimit值小于或等于总任务个数时，进行并发控制
    if (poolLimit <= array.length) {
      // 当任务完成后，从正在执行的任务数组中移除已完成的任务
      const e = p.then(() => executing.splice(executing.indexOf(e), 1));
      executing.push(e); // 保存正在执行的异步任务
      if (executing.length >= poolLimit) {
        await Promise.race(executing); // 等待较快的任务执行完成
      }
    }
  }
  return Promise.all(ret);
}

async function download({ url, chunkSize, poolLimit = 1 }) {
  const contentLength = await getContentLength(url);
  const chunks =
    typeof chunkSize === "number" ? Math.ceil(contentLength / chunkSize) : 1;
    progress_bar(0,0)
  const results = await asyncPool(
    poolLimit,
    [...new Array(chunks).keys()],
    (i) => {
      let start = i * chunkSize;
      let end = i + 1 == chunks ? contentLength - 1 : (i + 1) * chunkSize - 1;
      progress_bar(1,(i+1)/chunks)
      return getBinaryContent(url, start, end, chunkSize,i);
    }
  );
//   console.log(1111111111111,results)
//   if (window.DOMParser)
// { // Firefox, Chrome, Opera, etc.
//     parser=new DOMParser();
//     xmlDoc=parser.parseFromString(xml,"text/xml");
// }
// else // Internet Explorer
// {
//     xmlDoc=new ActiveXObject("Microsoft.XMLDOM");
//     xmlDoc.async=false;
//     xmlDoc.loadXML(xml); 
// } 

  r=results.map((item)=> console.log(item))
  const sortedBuffers = results
    .map((item) => new Uint8Array(item.buffer));
  return concatenate(sortedBuffers);
}