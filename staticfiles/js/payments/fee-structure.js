$('input[type=radio][name=paymentGateway]').on('change', function(e) {
    e.preventDefault();
    $.ajax({
    type: "POST",
    url: '{% url "payment:payment_option_selection" %}',
    data: {
        gatewaytype: $(this).val(),
        csrfmiddlewaretoken: "{{csrf_token}}",
        action: "post",
    },
    success: function (json) {
        console.log(json)
        document.getElementById("totalSalary").innerHTML = json.selected_total;
        document.getElementById("totalFees").innerHTML = json.processing_fee;
    },
    error: function (xhr, errmsg, err) {},
    });
    
});