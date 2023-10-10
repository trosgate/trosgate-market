  //'use strict';

  const paystackButton = document.getElementById('paystackButton');
  
  paystackButton.addEventListener('click', function() {

    paystackButton.disabled = true;
    fetch('/contract/paystack_payment_intent/', {
      method: 'GET',
      credentials: 'same-origin',
      headers: {
          'content-type': 'application/json',
      },
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      
      const handler = PaystackPop.setup({
        key: paystack_public_key, // Replace with your Paystack key ID
        amount: data.amount,
        ref: data.reference,
        email: data.email,
        currency: data.currency,
        onClose: function(){
          paystackButton.disabled = false;
          alert('Window closed.');
        },
        callback: function(response) {
          console.log(response)
          // Handle the response after payment completion
          const formData = new FormData();
          formData.append('transaction_reference', response.trans);
          formData.append('payment_reference', response.reference);
          formData.append('status', response.status);
          formData.append('message', response.message);

          fetch('/contract/paystack_callback/', {
            method: 'POST',
            body: formData,
            credentials: 'same-origin',
            headers: {
              'X-CSRFToken': CSRF_TOKEN
            }
          })
          .then(function(response) {
            return response.json();
          })
          .then(function(data) {
            if (data.status === 'success') {
              // Handle success message or redirect to a success page
              paystackButton.disabled = false;
              swal("Perfect!", 'All looked good', "success").then((value) =>{
                window.location.href = data.transaction_url;
              });
            } else {
              // Handle payment error or redirect to an error page
              paystackButton.disabled = false;
              swal("Ooops!!", 'Payment unsuccessful', "error");
            }
          })
          .catch(function(error) {
            paystackButton.disabled = false;
            swal("Opps!", 'Payment Unsuccessful', "error");
            console.log(error);
          });
        }
      });
      handler.openIframe();
    })
    .catch(function(error) {
        paystackButton.disabled = false;
        console.log(error);
    });
  });

