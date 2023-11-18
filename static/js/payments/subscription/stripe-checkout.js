//'use strict';
const stripe = Stripe(STRIPE_PUBLIC_KEY);
const cardbtn = document.getElementById('stripeButton');
const elements = stripe.elements();
const style = {
  base: {
    color: "#000",
    lineHeight: '2.4',
    fontSize: '16px'
  }
};

const cardElement = elements.create("card", { style: style });
cardElement.mount("#card-element");

let form = document.getElementById('stripe-form');
cardbtn.disabled = true;
cardElement.on('change', function(event) {
  cardbtn.disabled = true;
  let displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
    $('#card-errors').addClass('alert alert-danger');
  } else {
    cardbtn.disabled = false;
    displayError.textContent = '';
    $('#card-errors').removeClass('alert alert-danger');
  }
});

form.addEventListener('submit', function(event) {
  event.preventDefault();
  cardbtn.disabled = true;
  stripe.createToken(cardElement).then(function(result) {
    if (result.error) {
      // Handle card tokenization error
      console.log(result.error.message);
      cardbtn.disabled = false;
    } else {
      let formData = new FormData();
      formData.append('card_token', result.token.id);
      fetch('/team/stripe_payment_intent/', {
        method: 'POST',
        body: formData, 
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': CSRF_TOKEN
        }
      }).then(function(response) {
        return response.json();
      }).then(function(data) {
        if (data.client_secret) {
          // Handle the card action (3D Secure) and confirm the payment
          stripe.handleCardPayment(data.client_secret).then(function(result) {
            if (result.error) {
              // Handle payment authentication error
              console.log(result.error.message);
              cardbtn.disabled = false;
            } else {
              if (result.paymentIntent.status === 'succeeded') {
                // Payment successful, submit the form data to your backend
                console.log('stripe_order_key ::', result.paymentIntent.id)
                let formData = new FormData();
                formData.append('stripe_order_key', result.paymentIntent.id);
                fetch('/application/stripe_payment_order/', {
                  method: 'POST',
                  body: formData,
                  credentials: 'same-origin',
                  headers: {
                    'X-CSRFToken': CSRF_TOKEN
                  }
                }).then(function(response) {
                  return response.json();
                }).then(function(data) {
                  if (data.status === "success") {
                    
                    form.reset();
                    swal("Perfect!", 'All looked good', "success").then((value) =>{
                      window.location.href = data.transaction_url;
                    });
                  } else if (data.status === "failed") {
                    // Handle payment error
                    swal("Perfect!", 'Payment unsuccessful', "error");
                  }
                  cardbtn.disabled = false;
                }).catch(function (error) {
                  cardbtn.disabled = false;
                  return console.log(error);
                });
              } else {
                // Payment failed or canceled
                swal("Perfect!", 'Payment unsuccessful', "error");
                cardbtn.disabled = false;
              }
            }
          });
        } else {
          // Error handling if client_secret is not available
          console.log("Client secret is missing.");
          cardbtn.disabled = false;
        }
      }).catch(function (error) {
        cardbtn.disabled = false;
        return console.log(error);
      });
    }
  });
});
