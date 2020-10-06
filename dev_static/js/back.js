$(document).ready(function() {
    function numberWithSpaces(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    }

    $('.search-input').on('keypress', function(e){
        console.log(e.which);
        if(e.which === 13) {
            $(this).parents('.search-box').submit();
        }
    });

    $('#add-order').click(function() {
        $(this).prop('disabled', true);

        order_form = $('#order-form');
        delivery = $('input[name="delivery"]');
        pay_type = $('input[name="pay-type"]').val('online');

        order_form.append(delivery);
        order_form.append(pay_type);
        order_form.submit();
    });

    $('#add-order-credit').click(function() {
        $(this).prop('disabled', true);

        order_form = $('#order-form');
        delivery = $('input[name="delivery"]');
        pay_type = $('input[name="pay-type"]').val('credit');

        order_form.append(delivery);
        order_form.append(pay_type);
        order_form.submit();
    });

    $('input[name="delivery"]').change(function() {
        form = $(this).parents('form');

        $('#id_postcode').clone().addClass('d-none').appendTo(form);
        $('#id_country').clone().addClass('d-none').appendTo(form);
        $('#id_region').clone().addClass('d-none').appendTo(form);
        $('#id_city').clone().addClass('d-none').appendTo(form);
        $('#id_address').clone().addClass('d-none').appendTo(form);
        $('#id_phone').clone().addClass('d-none').appendTo(form);
        $('#id_full_name').clone().addClass('d-none').appendTo(form);
        $('#id_email').clone().addClass('d-none').appendTo(form);

        form.submit();
    });

    $('#MessageToManagerModal button[type="submit"]').on('click', function(e) {
        e.preventDefault();
        submit_button = $(this);

        var form = submit_button[0].form;

        if(form.checkValidity() === false) {
            form.classList.add('was-validated');
        } else {
            submit_button.prop("disabled", true);

            data = {
                'csrfmiddlewaretoken': form.elements['csrfmiddlewaretoken'].value,
                name: form.elements['name'].value,
                email_or_phone: form.elements['email_or_phone'].value,
                text: form.elements['text'].value,
            }

            $.ajax({
                type: 'POST',
                url: $('#MessageToManagerModal form').attr('action'),
                data: data,
                success: function(data) {
                    if (data.status) {
                        $('#MessageToManagerModal .form-success').removeClass('d-none');
                        $('#MessageToManagerModal .form-success').addClass('d-flex');
                    } else {
                        $('#MessageToManagerModal .alert-dismissible').removeClass('d-none');
                    }
                }
            });
        }

    });

    $('#OneClickOrderModal button[type="submit"]').click(function(e) {
        e.preventDefault();
        submit_button = $(this);

        var form = submit_button[0].form;

        if(form.checkValidity() === false) {
            form.classList.add('was-validated');
        } else {
            submit_button.prop("disabled", true);

            data = {
                'csrfmiddlewaretoken': form.elements['csrfmiddlewaretoken'].value,
                full_name: form.elements['full_name'].value,
                phone: form.elements['phone'].value,
                product: $('#ChangeOffer input[name="product"]').val(),
                color: $('#ChangeOffer input[name="color"]:checked').val(),
                size: $('#ChangeOffer input[name="size"]:checked').val(),
                cup: $('#ChangeOffer input[name="cup"]:checked').val(),
            }

            $.ajax({
                type: 'POST',
                url: form.action,
                data: data,
                success: function(data) {
                    if (data.success) {
                        $('#one-click-add-message').removeClass('d-none');
                        $('#one-click-add-message').addClass('d-flex');
                    } else {
                        $('#one-click-add-error').removeClass('d-none');
                    }
                }
            });
        }
    });

    $('.add-favorite').click(function(e) {
        button = $(this);
        e.preventDefault();
        offer = button.data('offer-id');

        data = {
            offer: offer,
        }

        $.ajax({
            type: "GET",
            url: '/catalogue/add-favorite/',
            data: data,
            success: function(data) {
                button.addClass('d-none');
                button.removeClass('d-inline-block');
                favorite_len = $('#favorite-len').text();
                $('#favorite-len').html(parseInt(favorite_len) + 1);
            }
        });
    });

    $('.remove-favorite').click(function(e) {
        e.preventDefault();
        favorite = $(this).data('favorite-id');

        data = {
            favorite: favorite,
        }

        $.ajax({
            type: "GET",
            url: '/catalogue/remove-favorite/',
            data: data,
            success: function(data) {
                $('.cart-item-' + favorite).addClass('d-none');
                favorite_len = $('#favorite-len').text();
                $('#favorite-len').html(parseInt(favorite_len) - 1);
            }
        });
    });

    function change_quantity() {
        $(this).parents('form').submit();
    }

    $('.product-item-number input').on('blur', change_quantity);
    $('.product-item-number .input-group-append').on('click', change_quantity);
    $('.product-item-number .input-group-prepend').on('click', change_quantity);

    $('#ChangeOffer').on('change', 'input[type="radio"]', function() {
        data = {
            product: $('#ChangeOffer input[name="product"]').val(),
            color: $('#ChangeOffer input[name="color"]:checked').val(),
            size: $('#ChangeOffer input[name="size"]:checked').val(),
            cup: $('#ChangeOffer input[name="cup"]:checked').val(),
            btn_type: $(this).attr('name')
        }

        $.ajax({
            type: 'GET',
            url: '/catalogue/change-offer/',
            data: data,
            success: function(data) {
                switch(data.btn_type) {
                    case 'color':
                        sizes = $('#product-size-select');
                        sizes.empty();
                        for(i=0; i<data.sizes.length; i++) {
                            checked = parseInt(data.sizes[i][2]);
                            sizes.append(`
                            <label class="btn ${ checked ? 'active' : '' }">
                                <input type="radio" name="size" value="${data.sizes[i][0]}" autocomplete="off" ${ checked ? 'checked' : '' }>
                                ${data.sizes[i][1]}
                            </label>
                            `);
                        }

                        cups = $('#product-cup-select');
                        cups.empty();
                        for(i=0; i<data.cups.length; i++) {
                            checked = parseInt(data.cups[i][2]);
                            cups.append(`
                            <label class="btn ${ checked ? 'active' : '' }">
                                <input type="radio" name="cup" value="${data.cups[i][0]}" autocomplete="off" ${ checked ? 'checked' : '' }>
                                ${data.cups[i][1]}
                            </label>
                            `);
                        }
                        break;
                    case 'size':
                        // colors = $('#product-color-select');
                        // colors.empty();
                        // for(i=0; i<data.colors.length; i++) {
                        //     checked = parseInt(data.colors[i][2]);
                        //     colors.append(`
                        //     <label class="btn ${ checked ? 'active' : '' }" style="background-color: ${ data.colors[i][1] };">
                        //         <input type="radio" name="color" value="${data.colors[i][0]}" autocomplete="off" ${ checked ? 'checked' : '' }>
                        //     </label>
                        //     `);
                        // }

                        cups = $('#product-cup-select');
                        cups.empty();
                        for(i=0; i<data.cups.length; i++) {
                            checked = parseInt(data.cups[i][2]);
                            cups.append(`
                            <label class="btn ${ checked ? 'active' : '' }">
                                <input type="radio" name="cup" value="${data.cups[i][0]}" autocomplete="off" ${ checked ? 'checked' : '' }>
                                ${data.cups[i][1]}
                            </label>
                            `);
                        }
                        break;
                    case 'cup':
                        // colors = $('#product-color-select');
                        // colors.empty();
                        // for(i=0; i<data.colors.length; i++) {
                        //     checked = parseInt(data.colors[i][2]);
                        //     colors.append(`
                        //     <label class="btn ${ checked ? 'active' : '' }" style="background-color: ${ data.colors[i][1] };">
                        //         <input type="radio" name="color" value="${data.colors[i][0]}" autocomplete="off" ${ checked ? 'checked' : '' }>
                        //     </label>
                        //     `);
                        // }

                        // sizes = $('#product-size-select');
                        // sizes.empty();
                        // for(i=0; i<data.sizes.length; i++) {
                        //     checked = parseInt(data.sizes[i][2]);
                        //     sizes.append(`
                        //     <label class="btn ${ checked ? 'active' : '' }">
                        //         <input type="radio" name="size" value="${data.sizes[i][0]}" autocomplete="off" ${ checked ? 'checked' : '' }>
                        //         ${data.sizes[i][1]}
                        //     </label>
                        //     `);
                        // }
                        break;
                }

                if (data.offer_price == data.product_price) {
                    $('#offer-price').html(`
                        <span class="number h3 font-weight-normal mr-1e">${numberWithSpaces(data.offer_price)}</span><span class="smaller">₽</span>
                    `);
                } else {
                    $('#offer-price').html(`
                        <div>
                            <div class="d-inline-block mr-2 text-muted"><del><span class="number mr-1">${numberWithSpaces(data.product_price)}</span><span class="small">₽</span></del></div>
                            <div class="d-inline-block text-danger"><span class="number h3 font-weight-normal mr-1">${numberWithSpaces(data.offer_price)}</span><span class="smaller">₽</span></div>
                        </div>
                    `);
                }

                $('#offer-stock').html(data.offer_stock);

                console.log(data.promo_text);
                if (data.promo_text) {
                    $('#promo-text').parent().addClass('d-block');
                    $('#promo-text').parent().removeClass('d-none');
                    $('#promo-text').html(data.promo_text);
                } else {
                    $('#promo-text').parent().addClass('d-none');
                    $('#promo-text').parent().removeClass('d-block');
                }

                if (data.offer_stock) {
                    $('#product-buttons').addClass('d-md-flex');
                    $('#product-buttons').removeClass('d-none');
                    if (data.in_cart) {
                        $('#add-to-cart').addClass('d-none');
                        $('#in-cart').removeClass('d-none');
                    } else {
                        $('#add-to-cart').removeClass('d-none');
                        $('#in-cart').addClass('d-none');
                    }
                } else {
                    $('#product-buttons').addClass('d-none');
                    $('#product-buttons').removeClass('d-md-flex');
                }

                image_id = $('#image-' + data.image_id).data('image_id');

                var owl = $('.owl-carousel');
                owl.trigger('to.owl.carousel', [image_id, 1]);
            }
        });
    });

    $('#big_filters input').on('click', function(e) {
        $('.filter-apply').removeClass('d-block');
        $('.filter-apply').addClass('d-none');
        $(this).parents('.filter-box').children('.filter-apply').removeClass('d-none');
    });

    $('#small_filters input').on('click', function(e) {
        $('.filter-apply').removeClass('d-block');
        $('.filter-apply').addClass('d-none');
        $(this).parents('.filter-box').children('.filter-apply').removeClass('d-none');
    });

    $('#AccountDeleteModal .btn[type="submit"]').on('click', function(e) {
        submit_button = $(this);
        e.preventDefault();
        $('#delete-errors').empty();

        var form = submit_button[0].form;

        if(form.checkValidity() === false) {
            form.classList.add('was-validated');
        } else {
            submit_button.prop("disabled", true);

            csrf_token = form.elements['csrfmiddlewaretoken'].value;
            username = form.elements['username'].value;
            password = form.elements['password'].value;

            data = {
                'csrfmiddlewaretoken': csrf_token,
                username: username,
                password: password,
            }
    
            $.ajax({
                type: 'POST',
                url: form.action,
                data: data,
                success: function(data) {
                    if (data.success) {
                        window.location.replace('/users/delete-user/');
                    } else {
                        submit_button.prop("disabled", false);
                        for(i=0; i<data.errors.length; i++){
                            $('#delete-errors').append(`
                                <div class="alert alert-secondary alert-dismissible small fade show mb-4" role="alert">
                                    ${data.errors[i]}
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                            `);
                        }
                    }
                }
            });
        }
    });


    $('#SignIn-pane .btn[type="submit"]').on('click', function(e) {
        submit_button = $(this);
        e.preventDefault();
        $('#login-errors').empty();

        var form = submit_button[0].form;

        if(form.checkValidity() === false) {
            form.classList.add('was-validated');
        } else {
            submit_button.prop("disabled", true);

            csrf_token = form.elements['csrfmiddlewaretoken'].value;
            username = form.elements['username'].value;
            password = form.elements['password'].value;
            remember_me = form.elements['remember_me'].value;

            data = {
                'csrfmiddlewaretoken': csrf_token,
                username: username,
                password: password,
                remember_me: remember_me
            }
    
            $.ajax({
                type: 'POST',
                url: form.action,
                data: data,
                success: function(data) {
                    if (data.success) {
                        window.location.replace('/users/profile/');
                    } else {
                        submit_button.prop("disabled", false);
                        for(i=0; i<data.errors.length; i++){
                            $('#login-errors').append(`
                                <div class="alert alert-secondary alert-dismissible small fade show mb-4" role="alert">
                                    ${data.errors[i]}
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                            `);
                        }
                    }
                }
            });
        }
    });


    $('#SignUp-pane .btn[type="submit"]').on('click', function(e) {
        submit_button = $(this);
        e.preventDefault();
        $('#register-errors').empty();

        var form = submit_button[0].form;

        if(form.checkValidity() === false) {
            form.classList.add('was-validated');
        } else {
            submit_button.prop("disabled", true);

            csrf_token = form.elements['csrfmiddlewaretoken'].value;
            username = form.elements['username'].value;
            password1 = form.elements['password1'].value;
            password2 = form.elements['password2'].value;

            data = {
                'csrfmiddlewaretoken': csrf_token,
                username: username,
                password1: password1,
                password2: password2
            }
    
            $.ajax({
                type: 'POST',
                url: form.action,
                data: data,
                success: function(data) {
                    submit_button.prop("disabled", false);
                    if (data.success) {
                        if (data.success_message) {
                            $('#register-errors').append(`
                                <div class="alert alert-secondary alert-dismissible small fade show mb-4" role="alert">
                                    ${data.success_message}
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                            `);
                        }
                    } else {
                        errors = jQuery.parseJSON(data.errors);
                        for (item in errors){
                            for(i=0; i<errors[item].length; i++){
                                $('#register-errors').append(`
                                    <div class="alert alert-secondary alert-dismissible small fade show mb-4" role="alert">
                                        ${errors[item][i]['message']}
                                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                `);
                            }
                        }
                        if (data.email_error) {
                            $('#register-errors').append(`
                                <div class="alert alert-secondary alert-dismissible small fade show mb-4" role="alert">
                                    ${data.email_error}
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                            `);
                        }
                    }
                }
            });
        }
    });
});