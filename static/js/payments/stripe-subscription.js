// Get Stripe publishable key
fetch("/team/api/init_stripe_config/")
//fetch("{% url 'teams:create_stripe_checkout_session' %}")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  let submitBtn = document.querySelector("#submitBtn");
  if (submitBtn !== null) {
    submitBtn.addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/team/api/stripe_checkout_session/")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }
});