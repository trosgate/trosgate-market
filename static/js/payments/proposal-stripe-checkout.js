
/// Make csrf token availble in JS files

//let CSRF_TOKEN = '{{ csrf_token }}';

function stripePay(event) {
  event.preventDefault();

  let stripepCustomer = document.getElementById("stripepCustomer").value;
  let stripepEmail = document.getElementById("stripepEmail").value;
  let stripepCountry = document.getElementById("stripepCountry").value;

  let displayError = document.getElementById('stripecard-errors')

  if (stripepCustomer == '' || stripepEmail == '' || stripepCountry == '') {
    displayError.textContent = 'Ooops! All fields are required';
    $('#stripecard-errors').addClass('alert alert-danger');

    return false
  }
  else {
    displayError.textContent = '';
    $('#stripecard-errors').removeClass('alert alert-danger');
    

    let data = {
      'stripepCustomer': stripepCustomer, //document.querySelector('input[name=stripeCustomer]').value,
      'stripepEmail': stripepEmail,// document.querySelector('input[name=stripeEmail]').value,
      'stripepCountry': stripepCountry,//document.querySelector('input[name=stripeCountry]').value,

    }

    let stripe = Stripe('{{stripe_public_key}}');

    fetch('/transaction/stripe/checkout/api/', {
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
