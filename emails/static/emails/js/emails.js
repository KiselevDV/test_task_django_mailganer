$(document).ready(function () {
    $('#campaign-form').submit(function (event) {
        event.preventDefault();
        let formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: '/create_campaign/',
            data: formData,
            success: function (response) {
                if (response.success) {
                    $('#campaignModal').modal('hide');
                    updateCampaignList();
                    alert('Рассылка успешно создана!');
                } else {
                    alert('Ошибка: ' + response.error);
                }
            },
            error: function () {
                alert('Ошибка при отправке запроса.');
            }
        });
    });

    function updateCampaignList() {
        $.ajax({
            url: '/get_campaigns/',
            type: 'GET',
            success: function (data) {
                $('#campaign-list').html(data);
            },
            error: function () {
                alert('Ошибка при обновлении списка рассылок.');
            }
        });
    }

    $('#campaignModal').on('hidden.bs.modal', function () {
        $('#campaign-form')[0].reset();
    });
});