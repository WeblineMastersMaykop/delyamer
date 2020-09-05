(function($) {
    function FooterBottom() { 
        $('body').css('margin-bottom', $('.footer').outerHeight())
    }

    FooterBottom();
    window.addEventListener('resize', FooterBottom, false);  
})(jQuery);

$(document).ready(function(){
    $('.offcanvas-collapse .dropdown').on('show.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown("fast");
    });

    $('.offcanvas-collapse .dropdown').on('hide.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp("fast");
    });
});

$(document).ready(function () {
    $('.navbar .dropdown').hover(function () {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown(150);
    }, function () {
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp(150)
    });
});

$(document).ready(function(){
    $(function () {
        'use strict'
        $('[data-toggle="offcanvas"]').on('click', function () {
            $('.offcanvas-collapse').toggleClass('open');
            $('.navbar-toggler-icon').toggleClass('open');
            $('.top-bar').toggleClass('offcanvas-on');
            $('.navbar').toggleClass('offcanvas-on');
            $('body').toggleClass('offcanvas-on');
        })
    })
});

$(document).ready(function(){
    $(function () {
        'use strict'
        $('[data-toggle="offcanvas-filters"]').on('click', function () {
            $('.offcanvas-filters').toggleClass('open');
            $('.offcanvas-filters-toggler-icon').toggleClass('open');
        })
    })
});

$(document).ready(function(){
    function handleFirstTab(e) {
        if (e.keyCode === 9) {
            document.body.classList.add('user-is-tabbing');

            window.removeEventListener('keydown', handleFirstTab);
            window.addEventListener('mousedown', handleMouseDownOnce);
        }
    }

    function handleMouseDownOnce() {
        document.body.classList.remove('user-is-tabbing');

        window.removeEventListener('mousedown', handleMouseDownOnce);
        window.addEventListener('keydown', handleFirstTab);
    }

    window.addEventListener('keydown', handleFirstTab);
});

$(document).ready(function(){
    $(window).scroll(function(){
        if ($(this).scrollTop() > 750) {
            $('.scroll-to-top').fadeIn(200);
        } 
        else {
            $('.scroll-to-top').fadeOut(200);
        }
    });
    $('.scroll-to-top').click(function(){
        $('html, body').animate({scrollTop : 0},300);
        return false;
    });
});

$(document).ready(function(){
    var $grid = $('.img-grid').masonry({
        itemSelector: 'figure',
        percentPosition: true
    });
    // layout Masonry after each image loads
    $grid.imagesLoaded().progress( function() {
        $grid.masonry();
    });  
});

(function() {
    'use strict';
    window.addEventListener('load', function() {
        var forms = document.getElementsByClassName('needs-validation');
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

function numberWithCommas(number) {
    var parts = number.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    return parts.join(".");
}
$(document).ready(function() {
    $(".number").each(function() {
        var num = $(this).text();
        var commaNum = numberWithCommas(num);
        $(this).text(commaNum);
    });
});

(function($) {
    function MtchHeight() { 
        if(window.matchMedia('(min-width: 576px)').matches){
            $(function() {
                $('.mh-1').matchHeight({
                    byRow: false
                });

                $('.mh-2').matchHeight({
                    byRow: false
                });

                $('.mh-3').matchHeight({
                    byRow: false
                });
            });
        }

        else {
            $(function() {
                $('.mh-1').matchHeight({
                    byRow: false
                });

                $('.mh-2').matchHeight({
                    byRow: true
                });

                $('.mh-3').matchHeight({
                    byRow: true
                });
            });
        }
    }

    MtchHeight();
    window.addEventListener('resize', MtchHeight, false);  
})(jQuery);

jQuery(function($){
    $(".phone-input").mask("+7 (999) 999-99-99",{placeholder:"_"});
});

$(document).ready(function(){
    $(".carousel-products").owlCarousel( {
        loop: true,
        margin: 30,
        nav: true,
        dots: false,
        responsive:{
            0:{
                items:1,
                slideBy:1,
                nav:false,
                stagePadding:80
            },
            576:{
                items:2,
                slideBy:2,
                nav:false,
                stagePadding:80
            },
            768:{
                items:3,
                slideBy:3,
                nav:true,
                stagePadding:80
            },
            992:{
                items:3,
                slideBy:3,
                nav:true,
                stagePadding:80
            },
            1200:{
                items:4,
                slideBy:4,
                nav:true,
                stagePadding:60
            }

        }
    });
});

$(document).ready(function(){
    var products = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '../search-data.json'
    });

    $('.typeahead').typeahead(null, {
        name: 'search-data',
        source: products
    });
});

$(document).ready(function(){
    $('.search-input').on('focus', function() {
        $('.search-box').addClass('search-focus');
    });

    $('.search-input').on('focusout', function() {
        $('.search-box').removeClass('search-focus');
    });
});

(function($) {
    function NavbarScroll() {
        var scroll = $(window).scrollTop(),
            topbar = $('.top-bar').outerHeight();

        if(scroll > topbar){
            $('.navbar').addClass('fixed-top');
            $('.navbar').addClass('bg-white');
            $('.top-bar').css('margin-bottom', '56px');
        }

        else {
            $('.navbar').removeClass('fixed-top');
            $('.navbar').removeClass('bg-white');
            $('.top-bar').css('margin-bottom','0');
        }
    }

    NavbarScroll();
    window.addEventListener('scroll', NavbarScroll, false);  
})(jQuery);

$(document).ready(function() {
    $('.lz-menu').lazeemenu();
});


$(document).ready(function(){
    $('.photoswipe-product-photo').each(function() {
        $(this).find('a').each(function(i) {  // making true indexes for images because owl carousel cloning blocks and confuses them
            $(this).attr('data-index',i);
        });
    });
    $(".carousel-product-photo").owlCarousel( {
        loop: true,
        margin: 0,
        nav: true,
        dots: true,
        items:1,
        slideBy:1,
    })
});
(function($) {
    var $pswp = $('.pswp')[0];
    var image = [];

    $('.photoswipe-product-photo').each( function() {
        var $pic     = $(this),
            getItems = function() {
                var items = [];
                $pic.find('a').each(function() {
                    var $href   = $(this).attr('href'),
                        $size   = $(this).data('size').split('x'),
                        $width  = $size[0],
                        $height = $size[1];

                    var item = {
                        src : $href,
                        w   : $width,
                        h   : $height
                    }

                    items.push(item);
                });
                return items;
            }

        var items = getItems();

        $.each(items, function(index, value) {
            image[index]     = new Image();
            image[index].src = value['src'];
        });

        $pic.on('click', 'a', function(event) {
            event.preventDefault();

            var $index = $(this).data('index'); // we take the real index
            var options = {
                index: $index,
                bgOpacity: 1,
            }

            var lightBox = new PhotoSwipe($pswp, PhotoSwipeUI_Default, items, options);
            lightBox.init();
        });
    });
})(jQuery);

$(document).ready(function(){
    $("input[type='number']").inputSpinner();
});
