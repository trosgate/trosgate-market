//Script to add proposal quantity in session             
$(document).on('click', '#rzp-button1', function (e) {
    e.preventDefault();
    $.ajax({
        method: 'GET',
        url: '/application/razorpay/checkout/api/',
        success: function (response) {
            console.log(response)
            var options = {
                "key": "{{razorpay_public_key}}", // Enter the Key ID generated from the Dashboard
                "amount": response.amount, //"{% widthratio {{application_addon.get_total_price_after_discount_and_fee}} 1 100 %}", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": response.currency,
                "name": "{{website.site_name}}",
                "description": "Hiring of Applicants",
                "image": "{{website.site_Logo.url}}",
                "order_id": response.razorpay_order_key, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (responseOne) {
                    $.ajax({
                        type: "POST",
                        url: "/application/razorpay_webhook/",
                        data: {
                            orderid: responseOne.razorpay_order_id,
                            paymentid: responseOne.razorpay_payment_id,
                            signature: responseOne.razorpay_signature,
                            csrfmiddlewaretoken: "{{csrf_token}}",
                            action: "razorpay-application",
                            success: function (responseTwo) {
                                console.log('it went well')
                                console.log(responseTwo)
                                //swal("Perfect!", all went well, "success");
                            },
                        },
                    });
                },

                "prefill": {
                    "name": "{{request.user.get_full_name}}",
                    "email": "{{request.user.email}}",
                    "contact": "{{request.user.phone}}"
                },
                "notes": {
                    "address": "{{request.user.country}}"
                },
                "theme": {
                    "color": "#3399cc"
                }
            };
            var rzp1 = new Razorpay(options);
            rzp1.open();
        },
        error: function (xhr, errmsg, err) { }
    });
})