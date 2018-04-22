var socket;
socket = io.connect('http://' + document.domain + ':' + location.port);
//var socket = io.connect('http://127.0.0.1:5000');

$("#add_device").click(function(){
    var device_name = $("#device_name").val();
    var device_pin = $("#device_pin").val();
    socket.emit('addit', {'name':device_name,'pin':device_pin});
    socket.on('response', function(rep){
        if(rep['status']){
            $('#addDevice').modal('toggle');
            $('#device_name').val('');
            $('#device_pin').val('');
            alert("Device added successfully");
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
    socket.on('deleted',function(){alert("Deleted");
    $(".custom-btn").eq(index).remove();
    //$(".custom-btn").index(this).remove();
})
})
