$(document).ready(function() {


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