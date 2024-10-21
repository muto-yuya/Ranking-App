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
    $('.show_modal').eq(item_index).find("p.item_place").text("順位 "+place+"位")

    item_id_to_open = $('.show_modal').eq(item_index).find("p.item_id").text()
    $.ajax("/update_is_open_ajax", {
        type: "post",
        data: {"item_id_to_open": item_id_to_open},
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
