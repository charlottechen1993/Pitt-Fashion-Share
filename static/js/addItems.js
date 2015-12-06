$(document).ready(function(){

    var x1, y1, x2, y2;
    var width, height;


    // load clothing items



    $('#imgSelect').imgAreaSelect({
        handles: true, 
        onSelectEnd: function (img, selection) {
            if (!selection.width || !selection.height) {
                return;
            }

            x1 = selection.x1;
            y1 = selection.y1;
            x2 = selection.x2;
            y2 = selection.y2;
            // width = selection.width;
            // height = selection.height;
            height = $('#imgSelect').height();

            $('#x1').val(x1);
            $('#y1').val(y1);
            $('#x2').val(x2);
            $('#y2').val(y2);
            // $('#w').val(width);
            // $('#h').val(height);
        }
    });


    $('.addNewItem').click(function(){
        var clothingType = $('#clothingType').val();
        var description = $('#description').val();
        var brand = $('#brand').val();
        var price = $('#price').val();
        var imgID = $('#imgID').val();
        
        
        if (x1 === undefined || x2 === undefined || y1 === undefined || y2 === undefined) {
            alert("Please click on the image and select your clothing item.");
           // alert("x1 = " + x1 + ' and x2 = ' + x2 + ' and y1 = ' + y1 + ' and y2 = ' + y2);
            return;
        }
        
        // added this in since height and width seemed to be undefined even
        // when x1, x2, y1, y2 had values
        width = x2 - x1;
        height = y2 - y1;

        var parameters = 'clothingType=' + clothingType + "&description=" + 
                        description + "&brand=" + brand + "&price=" + price + 
                        '&x1=' + x1 + '&x2=' + x2 + '&y1=' + y1 + '&y2=' + y2 +
                        '&width=' + width + '&height=' + height + '&imgID=' + imgID;  

        $.ajax({
            'url': '/addNewItemHandler?' + parameters,
            'success': function(){
                alert(clothingType + ' was successfully added!');
                $('#brand').val("");
                $('#price').val("");
                $('#description').val("");
                $('#clothingType').val("");
                $('#x1').val(0);
                $('#y1').val(0);
                $('#x2').val(0);
                $('#y2').val(0);
            }
        });
        
        
        
    });


});