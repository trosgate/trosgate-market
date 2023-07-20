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
let csrftoken = getCookie('csrftoken');

const paypalButton = document.getElementById('paypal-button-container');

paypal.Buttons({
    createOrder(){
        // This function will be called when the button is clicked
        // Call your Django view to create a new PayPal order
        // return fetch("{% url 'transactions:paypal_payment_order' %}", {
        return fetch("/transaction/paypal/api/", {
            method: 'POST',
            headers: {
                'content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                amount: "{{hiring_box.get_total_price_after_discount_and_fee}}",
                currency: '{{base_currency}}',
                description: 'Purchase of proposal',
            }),
        }).then(function(response) {
            return response.json();
        }).then(function(order_id) {
            return order_id.paypal_order_key;
        })
        .catch(function (error) {
            swal("Perfect!", 'Error occured', "error");
        });
    },
    onApprove: function(data, actions) {
        // This function will be called when the payment is approved
        // Call your Django view to capture the payment
        // return fetch("{% url 'transactions:paypal_callback' %}", {
        return fetch("/transaction/paypal/callback/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                paypal_order_key: data.orderID,
            }),
        }).then(function(response) {
            return response.json();
        }).then(function() {
            // Handle the captured payment data here (e.g., show a success message)
            swal("Perfect!", 'All looked good', "success").then((value) =>{
                window.location.href = "/transaction/proposals/"
            });              
        })
        .catch(function (error) {
            swal("Perfect!", 'Error occured', "error");
        });
    }
}).render('#paypal-button-container');