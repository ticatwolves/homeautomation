var socket;
socket = io.connect('http://' + document.domain + ':' + location.port);
//var socket = io.connect('http://127.0.0.1:5000');

$("#update_ip").click(function(){
    var ip = $("#ip").val();
    console.log(ip)
    socket.emit('updateip', {'ip':ip});
    socket.on('response', function(rep){
        if(rep['status']){
            $('#update_ip').modal('toggle');
            $('#ip').val('');
            alert("IP Changed successfully");
        }
    });
});

$("#update_password").click(function(){
    console.log("some")
    var password = $("#password").val();
    console.log(password)
    socket.emit('updatepassword', {'word':password});
    socket.on('passwordresponse', function(rep){
        if(rep['status']){
            $('#update_password').modal('toggle');
            $('#password').val('');
            alert("password Changed successfully");
        }
    });
});

$("#update_name").click(function(){
    var name = $("#name").val();
    console.log(name)
    $('#username').text(name);
    socket.emit('updatename', {'uname':name});
    socket.on('nameresponse', function(rep){
        if(rep['status']){
            $('#updatename').modal('toggle');
            $('#name').val('');
            alert("name Changed successfully");
        }
    });
})
$(".switch").on("change",function(){
    var index = $(".switch").index(this);
    var typ
    if($(this).is(':checked')){
        typ = 0;
    } 
    else{typ = 1;} 
    alert(typ)
    socket.emit('updateit',{'index':index,'operation':typ});
});
$(".custom-btn").click(function(){
    var index = $(".custom-btn").index(this);
    socket.emit('deleteit',{'index':index});
    socket.on('deleted',function(){alert("Deleted")})
})