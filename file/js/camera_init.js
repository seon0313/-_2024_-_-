let id = 0;
let width = 1920;
let height = 1080;
let format = 'image/webp';
let send_per = 1.0;

let zip_per = .5;

let rotate = 0;

let count = 0;

function init(id_, width_, height_){
    id = id_;
    width = width_;
    height = height_;
    console.log(navigator.mediaDevices);
    navigator.getUserMedia = navigator.mediaDevices.getUserMedia || navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    if(navigator.getUserMedia )
    {
        navigator.mediaDevices.getUserMedia( {audio: false, video: { facingMode: "environment"} } )
            .then(function(stream) {
                cameraGet(stream);
            })
            .catch(function(e) {
                console.log("error: " + e);
            })
    }
    else {
        alert('지원 안됨');
        return;
    }
    /*
        navigator.mediaDevices.getUserMedia({video:true})
            .then(cameraGet)
            .catch(console.log("?"));*/
}

function sleep(ms) {
    const time = Date.now() + ms;
    while (Date.now() < time) {}
  }
function cameraGet(stream) {
    var cameraView = document.getElementById("cameraview");
    cameraView.srcObject = stream;
    setTimeout(() => send(), 1000);
}

function rotate_click(){
    console.log('!!U!U*@JI');
    count++;
    rotate = count*90;
    if (rotate > 280){
        rotate = 0;
        count=0;
    }
}

function send(){
    if (id!=0){
        var video = document.getElementById("cameraview");
        var canvas = document.createElement("canvas");
        canvas.width = video.videoWidth * zip_per;
        canvas.height = video.videoHeight * zip_per;

        var canvasContext = canvas.getContext("2d");
        

        canvasContext.save();
        canvasContext.translate(canvas.width/2,canvas.height/2);
        canvasContext.rotate(rotate*Math.PI/180);
        canvasContext.drawImage(video, 0-canvas.width/2, 0-canvas.height/2, canvas.width, canvas.height);
        var stream = canvas.toDataURL(format, send_per);
        canvasContext.restore();
    

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/camera/"+id);
        xhr.withCredentials = true;
        xhr.onload = function(event){
            // console.log("SEND DATA"); // raw response
        };
        xhr.onreadystatechange = function() {
            if(xhr.readyState == 4 && xhr.status == 200) {
                setTimeout(() => send(), 0);
            }
        }
        var formdata = new FormData();
        formdata.append("camera", stream);
        xhr.send(formdata);
    }
}

function change(){
    let id = document.getElementById('zip_per').value;
    let _format = document.getElementById('format').value;
    let _send = document.getElementById('send_per').value;
    zip_per = id;
    format = _format;
    send_per = _send;
    console.log(send_per);
}