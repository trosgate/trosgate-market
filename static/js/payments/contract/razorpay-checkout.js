  //'use strict';

  const razorpayButton = document.getElementById('razorpayButton');
  
  razorpayButton.addEventListener('click', function() {
    // Fetch API to create the order and get the transaction ID
    razorpayButton.disabled = true;
    fetch('/contract/razorpay_contract_intent/', {
      method: 'GET',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      // Create the Razorpay options with the received transaction ID
      const options = {
        key: razorpay_public_key, // Replace with your Razorpay key ID
        amount: data.amount,
        currency: data.currency,
        name: USER,
        description: `Purchase of service on ${SITE_NAME}`,
        image: "",
        order_id: data.razorpay_order_key, // Received from the backend
        handler: function(response) {
          razorpayButton.disabled = false;
          // Handle the response after payment completion
          const formData = new FormData();
          formData.append('orderid', response.razorpay_order_id);
          formData.append('paymentid', response.razorpay_payment_id);
          formData.append('signature', response.razorpay_signature);

          fetch('/contract/razorpay_callback/', {
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
              razorpayButton.disabled = true;
              swal("Perfect!", 'All looked good', "success").then((value) =>{
                window.location.href = data.transaction_url;
              });
            } else {
              // Handle payment error or redirect to an error page
              razorpayButton.disabled = false;
              swal("Ooops!!", 'Payment unsuccessful', "error");
            }
          })
          .catch(function(error) {
            razorpayButton.disabled = false;
            swal("Opps!", 'Payment unsuccessful', "error");
            console.log(error);
          });
        },
        prefill: {
          // Pre-fill customer details if available
          name: USER,
          email: USER_EMAIL,
          contact: USER_EMAIL,
        }
      };

      // Create the Razorpay payment form
      const rzp = new Razorpay(options);
      rzp.open();
    })
    .catch(function(error) {
        razorpayButton.disabled = false;
        console.log(error);
    });
  });

