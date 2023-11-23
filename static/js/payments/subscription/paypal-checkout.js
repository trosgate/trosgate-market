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
// let csrftoken = getCookie('csrftoken');

paypal.Buttons({
    
    createSubscription: function(data, actions) {
        return actions.subscription.create(
            {'plan_id': paypal_subscription_plan_id}
        );
    },
    
    onApprove: function(data, actions) {
        return fetch("/payment/paypal_subscription/", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token for Django protection
            },
            body: JSON.stringify({
                paypal_order_key: data.subscriptionID,
            }),
        }).then(function(response) {
            return response.json();
        }).then(function() {
            // Handle the captured payment data here (e.g., show a success message)
            swal("Perfect!", 'Transaction Successful', "success").then((value) =>{
                window.location.href = "/payment/packages/"
            });              
        })
        .catch(function (error) {
            swal("Perfect!", 'Error occured', "error");
        });
    }
}).render('#paypal-button-container');


