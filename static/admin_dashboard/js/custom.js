window.onload = $(function(){
    // this will get the full URL at the address bar
    var url = window.location.href; 

    // passes on every "a" tag 
    $("#adminDashboardList a").each(function() {
            // checks if its the same on the address bar
        if(url == this.href) {
            var current = document.getElementsByClassName("active");
            if (current.length > 0) { 
                current[0].className = current[0].className.replace(" active", "");
            }
            this.className += " active";
        }
    });
});



