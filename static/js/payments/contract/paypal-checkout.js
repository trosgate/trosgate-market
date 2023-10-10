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
        // createOrder: function(data, actions) {
        //     // Set up the transaction details
        //     const actions = actions.order.create({
        //         purchase_units: [{
        //             amount: {
        //                 value: "{{hiring_box.get_total_price_after_discount_and_fee}}"
        //             }
        //         }]
        //     });
        //     console.log('PayPal', actions.id)    
        //     console.log('PayPalD', actions.orderID) 
        return fetch("/contract/paypal/api/", {
            method: 'GET',
            credentials: 'same-origin',
            headers: {
                'content-type': 'application/json',
            },

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
        return fetch("/contract/paypal/callback/", {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken //CSRF_TOKEN
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


