$(document).ready(function () {
    function getCSRFToken() {
        return $("input[name=csrfmiddlewaretoken]").val();
    }

    $('#campaign-form').submit(function (event) {
        event.preventDefault();

        let formData = new FormData($('#campaign-form')[0]);
        formData.append('subscribers', $('select[name="subscribers"]').val().join(','));
        formData.append('template_id', $('select[name="template"]').val());

        $.ajax({
            type: 'POST',
            url: '/emails/create_campaign/',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
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
                alert('Ошибка при отправке запроса. Проверьте соединение и попробуйте снова.');
            }
        });
    });

    function updateCampaignList() {
        $.ajax({
            type: 'GET',
            url: '/emails/get_campaigns/',
            success: function (data) {
                $('#campaign-list').html(data);
            },
            error: function () {
                alert('Ошибка загрузки списка кампаний.');
            }
        });
    }
});