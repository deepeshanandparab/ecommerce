$(document).ready(function(){
    $('#previousButton').click(function(){
        var currPosition = $('#new-arrival-section ol').position().left;
        $('#new-arrival-section ol').animate({
            left: currPosition + 340
        });
    });

    $('#nextButton').click(function(){
        var currPosition = $('#new-arrival-section ol').position().left;
        $('#new-arrival-section ol').animate({
            left: currPosition - 340
        });
    });
});