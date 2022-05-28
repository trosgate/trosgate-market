$(function () {


    /* ============================================================
         TESTIMONIALS SLIDER
    =============================================================== */
    $('.testimonials-slider').owlCarousel({
        items: 1,
        loop: true,
        margin: 30,
        autoplay: true,
        smartSpeed: 1000,
    });


    /* ============================================================
         MODAL VIDEO
    =============================================================== */
    new ModalVideo('.video-btn');


    /* ============================================================
         NAVBAR SHOW & HIDE ON SCROLL
    =============================================================== */
    var currentScrollTop = 0,
        c = 0;
    $(window).on('scroll load', function () {
         var a = $(window).scrollTop(), b = $('.header').height();
        currentScrollTop = a;
        if (c < currentScrollTop && a > b + b + 100) {
            $('.header').addClass("scrollUp");
            $('.navbar .dropdown-menu').removeClass('show');
            $('.navbar .dropdown-toggle').attr('aria-expanded', 'false');
        } else if (c > currentScrollTop && !(a <= b)) {
            $('.header').removeClass("scrollUp");
        }
        c = currentScrollTop;

        if ( $(window).scrollTop() > 50 ) {
            $('.header.header-animated').addClass('active');
        } else {
            $('.header.header-animated').removeClass('active');
        }
    });


    /* ============================================================
         DISABLE DEMO LINKS
    =============================================================== */
    $('[href="#"]').on('click', function (e) {
        e.preventDefault();
    });


    /* ============================================================
         SCROLL TOP BUTTON
    =============================================================== */
    $('#scrollTop').on('click', function () {
        $('html, body').animate({ scrollTop: 0}, 1000);
    });

    $(window).on('scroll', function () {
        if ($(window).scrollTop() >= 2000) {
            $('#scrollTop').addClass('active');
        } else {
            $('#scrollTop').removeClass('active');
        }
    });



});
