

$(document).ready(function(){
    $('.adore').click(function(){
   
        var photo_id = $(this).attr('data-id');
              alert(photo_id);
        $.ajax({
            url: '/addLike?photo_id=' + photo_id,
            type: 'GET',
            success: function(data){
                
            }
        });
    });

});


function printJSON(json){
    alert(JSON.stringify(json, null, 2));
    console.log(JSON.stringify(json, null, 2));
}
