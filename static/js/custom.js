var message = document.getElementById("message-container");

setTimeout(function(){
   message.style.display = "none";
}, 3000);


function divPic(image) {
    document.getElementById('product_profile_img').innerHTML = "<img src= '"+image+"' class='w-100 border mt-2'>";
}