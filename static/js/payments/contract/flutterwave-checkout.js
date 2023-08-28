
const flutterwaveButton = document.getElementById('flutterwaveButton')
flutterwaveButton.addEventListener('click', function () {
    flutterwaveButton.disabled = true;
    fetch("/transaction/flutter_payment_intent/", {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data) {
            FlutterwaveCheckout({
                public_key: flutterwave_public_key,
                tx_ref: data.tx_ref,
                amount: data.amount,
                currency: data.currency,
                payment_options: "card, banktransfer, ussd, mobilemoneyghana",
                meta: {
                    consumer_id: 23,
                    consumer_mac: "92a3-912ba-1192a",
                    },
                customer: {
                    email: data.email,
                    phone_number: data.phone,
                    name: data.customer,
                },
                customizations: {
                    title: "The Gladiators",
                    description: "Payment for an awesome service",
                    logo: "",
                },                
                callback: function (response) {
                    fetch(`/transaction/flutter_success/?tx_ref=${response.tx_ref}&transaction_id=${response.transaction_id}&status=${response.status}`,{
                        method: 'GET',
                        credentials: 'same-origin',
                        headers: {
                          'Content-Type': 'application/json',
                        }
                    })
                    .then(response => response.json())
                    .then(function(data) {
                        flutterwaveButton.disabled = false;
                        if (data.status === 'success') {
                          // Handle success message or redirect to a success page
                          swal("Perfect!", 'Payment Successful', "success").then((value) =>{
                            window.location.href = data.transaction_url;
                          });
                        } else {
                          // Handle payment error or redirect to an error page
                          swal("Ooops!!", 'Payment Unsuccessful', "error");
                        }
                    })
                },
            });
        } else {
            flutterwaveButton.disabled = false;
        }
    })
    .catch(function(error) {
        flutterwaveButton.disabled = false;
        swal("Opps!", 'Payment unsuccessful', "error");
        console.log(error);
    });
});

