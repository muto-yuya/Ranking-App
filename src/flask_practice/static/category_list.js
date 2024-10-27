$('.show_modal').on('click', function() {
    create_game_url = $(this).closest('tr').find('.game_create_url').text()
    $('#gameCreateModal').modal('show')
});

$('#gameCreateModalClose').on('click', function() {
    $('#gameCreateModal').modal('hide')
    create_game_url = null
});

$('#gameCreateModalConfirm').on('click', function() {
    window.location.href = create_game_url;
});