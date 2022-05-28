$(document).on('click', '#flutterwave-payment', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '{% url "applications:flutterwave_payment_order" %}',
        data: {
            amount: "{{application_addon.get_total_price_after_discount_and_fee}}",
            name: "{{request.user.get_full_name}}",
            email: "{{request.user.email}}",
            consumerid: "{{request.user.id}}",
            csrfmiddlewaretoken: "{{csrf_token}}",
            action: 'flutterwave'
        },
        success: function (json) {
            console.log(json)
            if (json)
                window.location.href = json;
        },
        error: function (xhr, errmsg, err) { }
    });
})