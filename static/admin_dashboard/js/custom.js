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




  window.onload = function () {
    var fileUpload = document.getElementById("product_image");
    fileUpload.onchange = function () {
        if (typeof (FileReader) != "undefined") {
            var dvPreview = document.getElementById("dvPreview");
            dvPreview.innerHTML = "";
            var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.jpg|.jpeg|.gif|.png|.bmp)$/;
            for (var i = 0; i < fileUpload.files.length; i++) {
                var file = fileUpload.files[i];
                if (regex.test(file.name.toLowerCase())) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        var img = document.createElement("IMG");
                        img.height = "100";
                        img.width = "100";
                        img.classList.add("col-3");
                        img.src = e.target.result;
                        dvPreview.appendChild(img);
                    }
                    reader.readAsDataURL(file);
                } else {
                    alert(file.name + " is not a valid image file.");
                    dvPreview.innerHTML = "";
                    return false;
                }
            }
        } else {
            alert("This browser does not support HTML5 FileReader.");
        }
    }
};


function load_category() {
    var painting = document.getElementById("painting");
    var antique = document.getElementById("antique");
    var craft = document.getElementById("craft");
    var furniture = document.getElementById("furniture");
    var value = document.getElementById("product_art_type").value;

    if (value == "painting") {
        painting.style.display = "block";
        antique.style.display = "none";
        craft.style.display = "none";
        furniture.style.display = "none";
    } else if(value == "antique") {
        painting.style.display = "none";
        antique.style.display = "block";
        craft.style.display = "none";
        furniture.style.display = "noe";
    }
    else if(value == "craft") {
        painting.style.display = "none";
        antique.style.display = "none";
        craft.style.display = "block";
        furniture.style.display = "noe";
    }
    else if(value == "furniture") {
        painting.style.display = "none";
        antique.style.display = "none";
        craft.style.display = "none";
        furniture.style.display = "block";
    }
    else {
        painting.style.display = "block";
        antique.style.display = "none";
        craft.style.display = "none";
        furniture.style.display = "none";
    }
};


/* --------------Product Category Add, Update, Delete Functions-----------------*/
function showProductCategoryForm(id){
    console.log(id)
    var add_category_form = document.getElementById(id);
    console.log(add_category_form)
    add_category_form.style.display = "block";
};


function hideProductCategoryForm(id){
    var add_category_form = document.getElementById(id);
    add_category_form.style.display = "none";
};


function showUpdateForm(id){
    var category_update_form = document.getElementById(id);
    category_update_form.style.display = "block";

    var str_category = 'category_data_';
    var category = str_category.concat(id);
    var category_data_section = document.getElementById(category);
    category_data_section.style.display = "none";
};


function hideUpdateForm(id){
    var category_update_form = document.getElementById(id);
    category_update_form.style.display = "none";

    var str_category = 'category_data_';
    var category = str_category.concat(id);
    console.log(category);
    var category_data_section = document.getElementById(category);
    category_data_section.style.display = "block";
};



/* ----------------------------------------------------------------------- */
function show_order_content(id) {
    var value = document.getElementById(id).id;
    console.log(id)
    pending = document.getElementById("pendingorders");
    complete = document.getElementById("completedorders");
    cancelled = document.getElementById("cancelledorders");

    if (value == "pendingorders") {
        pending.style.display = "block";
        complete.style.display = "none";
        cancelled.style.display = "none";
    } else if(value == "completedorders") {
        pending.style.display = "none";
        complete.style.display = "block";
        cancelled.style.display = "none";
    }
    else if(value == "cancelledorders") {
        pending.style.display = "none";
        complete.style.display = "none";
        cancelled.style.display = "block";
    }
    else{
        pending.style.display = "block";
        complete.style.display = "none";
        cancelled.style.display = "none";
    }