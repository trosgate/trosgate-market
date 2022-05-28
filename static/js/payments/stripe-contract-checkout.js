
/// Make csrf token availble in JS files

//let CSRF_TOKEN = '{{ csrf_token }}';

function stripePay(event) {
  event.preventDefault();

  let stripecCustomer = document.getElementById("stripecCustomer").value;
  let stripecEmail = document.getElementById("stripecEmail").value;
  let stripecCountry = document.getElementById("stripecCountry").value;

  let displayError = document.getElementById('stripecard-errors')

  if (stripecCustomer == '' || stripecEmail == '' || stripecCountry == '') {
    displayError.textContent = 'Ooops! All fields are required';
    $('#stripecard-errors').addClass('alert alert-danger');

    return false
  }
  else {
    displayError.textContent = '';
    $('#stripecard-errors').removeClass('alert alert-danger');
    console.log('error removed')

    let data = {
      'stripeCustomer': stripecCustomer, //document.querySelector('input[name=stripeCustomer]').value,
      'stripeEmail': stripecEmail,// document.querySelector('input[name=stripeEmail]').value,
      'stripeCountry': stripecCountry,//document.querySelector('input[name=stripeCountry]').value,

    }

    let stripe = Stripe('{{stripe_public_key}}');
    //   /contract/stripe/{{contract.id}}/
    fetch('{% url "contract:stripe_contract_intent" contract.id ', {
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
