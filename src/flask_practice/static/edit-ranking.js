$('.item_image_url').change(function(){
    var item_image_url = $(this).closest('tr').find('.item_image_url').val();
    $(this).closest('tr').find('.item_image').attr('src', item_image_url)
});


$('.rowdel').click(function() {
        let row = $(this).closest("tr").remove();
    $(row).remove();
});

$(function(){
    $('input').keypress(function(e){
        if(e.which == 13) {
            return false;
        }
    });
});