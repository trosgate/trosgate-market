function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function hiringPayPalButton() {
    paypal.Buttons({
        style: {
            layout: 'vertical',
            color: 'gold',
            shape: 'pill',
            label: 'paypal',
        },
        createOrder: function (data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: '{{application_addon.get_total_price_after_discount_and_fee}}'
                    }
                }]
            });
        },
        onApprove: function (data) {
            var url = "{% url 'applications:paypal_payment_order' %}"
            return fetch(url, {
                method: 'POST',
                headers: {
                    'content-type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    orderID: data.orderID
                })
            }).then(function () {
                location.href = "{% url 'applications:hiring_payment_success' %}"
            })
        },
    }).render('#paypal-button-container');
}
hiringPayPalButton();