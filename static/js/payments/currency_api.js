$(document).on('click', '#convert-currency', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '{% url "general_settings:converter" %}',
        data: {
            currencyid: $('#id_currency option:selected').val(),
            targetamount: '{{hiring_box.get_total_price_after_discount_and_fee}}',
            csrfmiddlewaretoken: "{{csrf_token}}",
            action: 'currency'
        },
        success: function (json) {
            document.getElementById('feedback-converter').innerHTML = json.message
        },
        error: function (xhr, errmsg, err) {}
    });
    })