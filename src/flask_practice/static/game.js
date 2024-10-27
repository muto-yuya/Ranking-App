$('.show_modal').on('click', function() {
    item_index = $(this).index()
    $('#placecConfirmModal').modal('show')
});

$('#placecConfirmModalClose').on('click', function() {
    $('#placecConfirmModal').modal('hide')
    item_index = null
});

$('#placecConfirmModalShow').on('click', function() {
    $('#placecConfirmModal').modal('hide')

    place = $('.item_place_store').eq(item_index).text()
    $('#placecShowModal').find("#placecShowModalLabel").text(place+"位です")
    $('#placecShowModal').modal('show')

    $('.show_modal').eq(item_index).addClass("bg-secondary")
    $('.show_modal').eq(item_index).find("p.item_place").text(place+"位")

    game_item_id_to_open = $('.show_modal').eq(item_index).find("p.item_id").text()
    $.ajax("/update_is_open_ajax", {
        type: "post",
        data: {"item_id_to_open": game_item_id_to_open},
    }).done(function(received_data) {
        console.log("Ajax Success");
    }).fail(function() {
        console.log("Ajax Failed");
    });
    
    item_index = null
});

$('#placecShowModalClose').on('click', function() {
    $('#placecShowModal').modal('hide')
    place = null
    item_index = null
});

$('#gameShare').on('click', function() {
    $('#gameShareModal').modal('show')
    $('#URLtoShare').text("URL: "+location.href)
    $('#QR').children().remove()
    var qrcode = new QRCode('QR', {
        text:  location.href,
        width: 128,
        height: 128,
        correctLevel : QRCode.CorrectLevel.H
      });  
});

$('#gameShareModalClose').on('click', function() {
    $('#gameShareModal').modal('hide')
});
