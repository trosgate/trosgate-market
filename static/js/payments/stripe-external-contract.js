
/// Make csrf token availble in JS files

let CSRF_TOKEN = '{{ csrf_token }}';

function stripePay(event) {
  event.preventDefault();

  let stripeCustomer = document.getElementById("stripeCustomer").value;
  let stripeEmail = document.getElementById("stripeEmail").value;
  let stripeCountry = document.getElementById("stripeCountry").value;

  let displayError = document.getElementById('stripecard-errors')

  if (stripeCustomer == '' || stripeEmail == '' || stripeCountry == '') {
    displayError.textContent = 'Ooops! All fields are required';
    $('#stripecard-errors').addClass('alert alert-danger');

    return false
  }
  else {
    displayError.textContent = '';
    $('#stripecard-errors').removeClass('alert alert-danger');
    console.log('error removed')

    let data = {
      'stripeCustomer': stripeCustomer, //document.querySelector('input[name=stripeCustomer]').value,
      'stripeEmail': stripeEmail,// document.querySelector('input[name=stripeEmail]').value,
      'stripeCountry': stripeCountry//document.querySelector('input[name=stripeCountry]').value,
    }

    let stripe = Stripe('{{stripe_public_key}}');

    fetch('/application/stripe/checkout/api/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{csrf_token}}'
      },
      credentials: 'same-origin',
      body: JSON.stringify(data)
    })
      .then(function (response) {
        return response.json()
      })
      .then(function (session) {
        return stripe.redirectToCheckout({ sessionId: session.session.id })
      })
      .then(function (result) {
        return console.log(result.error.message)
      })
      .catch(function (error) {
        return console.log(error)
      })
  }
}
