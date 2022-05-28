
// STRIPE DEPOSIT
let CSRF_TOKEN = '{{ csrf_token }}';
function stripePay(event) {
    event.preventDefault();

    let stripeAmount = $('[name="stripeAmount"]').val();
    let stripeNarration = $('[name="stripeNarration"]').val();

    let displayError = document.getElementById('stripe-error-message')
    let displaySuccess = document.getElementById('stripe-success-message')

    if (stripeAmount == '' || stripeNarration == '') {
        displayError.textContent = 'Ooops! All fields are required';
        $('#stripe-error-message').addClass('alert alert-danger');

        return false;
    }
    else {
        displayError.textContent = '';
        $('#stripe-error-message').removeClass('alert alert-danger');

        let data = {
            'stripeAmount': stripeAmount,
            'stripeNarration': stripeNarration,
        }

        let stripe = Stripe('{{stripe_public_key}}');

        fetch('/client/stripe-deposit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'csrfmiddlewaretoken': '{{csrf_token}}',
                // 'X-CSRFToken': '{{csrf_token}}'
            },
            credentials: 'same-origin',
            body: JSON.stringify(data)
        })
            .then(function (response) {
                displaySuccess.textContent = 'Hold on, you are almost there .....';
                $('#stripe-success-message').addClass('alert alert-success');
                return console.log(response)
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
