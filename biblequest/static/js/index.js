
$(window).on('load', function () {
    $.ajax({
        method: 'get',
        dataType: 'json',
        url: '/customer',
        success: function(data){
            if(data.status) {
                userView(data.products);
            }
        }
    });

    $(".navbar-burger").click(function() {
        toggleBurger();
        resetAllForms();
    });
    $(document).on('click', '.navbar-item:not(.trigger_popup_fricc)', function() {
        toggleBurger();
        resetAllForms();
    })
    
    // $('.navbar-item:not(.trigger_popup_fricc)').click(function(){
    //     console.log('burger item clicked');
    //     toggleBurger();
    //     resetAllForms();
    // })
    
    function toggleBurger() {
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
    }

    $(".trigger_popup_fricc").click(function(){
       $('.hover_bkgr_register').show();
    });
    // $('.hover_bkgr_register').click(function(){
    //     $('.hover_bkgr_register').hide();
    // });
    // remove upper left corner x button
    // $('.popupCloseButton').click(function(){
    //     $('.hover_bkgr_register').hide();
    // });
    $('.popupCancel').click(function(){
        $('.formToReset').closest('form')[0].reset();
        resetAllForms();
        $('.hover_bkgr_register').hide();
        $('.hover_bkgr_login').hide();
        toggleBurger();
    });
    $('.popupRegister').click(function(){
        $('.hover_bkgr_register').show();
        $('.hover_bkgr_login').hide();
    });
    $('.popupLogin').click(function(){
        $('.hover_bkgr_register').hide();
        $('.hover_bkgr_login').show();
    });


    let loginValidation = $('#login').validate({
        rules: {
            lemail: {
                required: true,
                email: true
            },
            lpassword: {
                required: true,
                pattern: '(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$^+=!*()@%&]).{8,20}'
            }
        },
        messages: {
            lemail: {
                required: 'Email field is required!',
                email: 'Please enter a valid email!'
            },
            lpassword: {
                required: 'Password field is required!',
                pattern: 'Password must contain 1 uppercase, 1 lowercase, 1 number and 1 special charater!'
            }
        },
        //adding bulma error message class
        errorClass: 'help is-danger'
    });
    
    let registerValidation = $('#register').validate({
        rules: {
            rname: {
                required: true
            },
            remail: {
                required: true,
                email: true
            },
            rphone_number: {
                required: true,
                pattern: '[0-9]{3}[ -][0-9]{3}[ -][0-9]{4}'
            },
            raddress: {
                required: true
            },
            rcity: {
                required: true
            },
            rstate: {
                required: true
            },
            rzip: {
                required: true,
                pattern: '[0-9]{5}'
            },
            rpassword: {
                required: true,
                minlength: (8),
                pattern:  new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})")
            },
            rconfirm_password: {
                required: true,
                equalTo: '#registerPassword'
            },
            rpurpose: {
                required: true
            }
        },
        messages: {
            rname: {
                required: 'Name field is required!',
            },
            remail: {
                required: 'Email field is required!',
                email: 'Please enter a valid email!'
            },
            rphone_number: {
                required: 'Phone number is required!',
                pattern: 'Phone number must be in the following format XXX-XXX-XXXX'
            },
            raddress: {
                required: 'Address field is required!'
            },
            rcity: {
                required: 'City field is required!'
            },
            rstate: {
                required: 'State field is required!'
            },
            rzip: {
                required: 'Zip is required!',
                pattern: 'Zip must be in the following format XXXXX'
            },
            rpassword: {
                required: 'Password field is required!',
                minlength: 'Password must be at least 8 characters long',
                pattern: 'Password must contain 1 uppercase, 1 lowercase, 1 number and 1 special character!'
            },
            rconfirm_password: {
                required: 'Confirm Password field is required!',
                pattern: 'Passwords must match'
            },
            rpurpose: {
                required: 'Please enter an option!'
            }
        },
        //adding bulma error message class
        errorClass: 'help is-danger'
    });
    
    let addUserProduct = $('.addUserProduct').validate({
        rules: {
            acode: {
                required: true,
                rangelength: [17, 18]
            }
        },
        messages: {
            acode: {
                required: 'A code is required',
                rangelength: 'Please enter a valid code'
            }
        },
        //adding bulma error message class
        errorClass: 'help is-danger'
    })

    let resetAllForms = function () {
        registerValidation.resetForm();
        loginValidation.resetForm();
        addUserProduct.resetForm();
    }
    
    $(document).on('submit', '#register', function(e){
        console.log(this);
        e.preventDefault();
        $.ajax({
            method: 'post',
            data: $(this).serialize(),
            dataType: 'json',
            url: '/registerCustomer',
            success: (data)=>{
                console.log('success response', data);
                registerValidation.resetForm();
                $(this).closest('form')[0].reset();
                toggleBurger();
                userView();
            },
            error: (data)=>{
                console.log('error response', data);
                $('#registerEmail').after(`<p class='help is-danger product_error'>${data.responseJSON.message}</p>`);
            }
        })
    })
    
    $(document).on('submit', '#login', function(e){
        console.log(this);
        // use jquery-plugin validator
        e.preventDefault();
        $.ajax({
            method: 'post',
            data: $(this).serialize(),
            dataType: 'json',
            url: '/loginCustomer',
            success: (data)=>{
                console.log(data);
                loginValidation.resetForm();
                $(this).closest('form')[0].reset();
                toggleBurger();
                userView(data.products);
            },
            error: (data)=>{
                $('#loginEmail').after(`<p class='help is-danger product_error'>${data.responseJSON.message}</p>`);
                console.log('error response', data);
            }
        })
    })

    // add user product and display newly added product
    $(document).on('submit', '.addUserProduct', function(e){
        console.log(this);
        let tile_ancestor = $('.user_products .tile ancestor:last').length
        console.log(tile_ancestor);
        console.log('*'.repeat(90));
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: $(this).serialize(),
            success: (data)=>{
                console.log('success data: ', data);
                $(this).closest('form')[0].reset();
                let html_string = buildUserProduct(data['product']);
                let tile_ancestor_length = $('.user_products .is-ancestor:last').children().length
                if(tile_ancestor_length > 3) {
                    html_string = '<div class="tile is-ancestor">' + html_string + '</div>';
                    // $('.user_products').append('<div class="tile is-ancestor">');
                    $('.user_products').append(html_string);
                    // $('.user_products').append('</div>');
                } else {
                    $('.user_products .is-ancestor:last').append(html_string);
                }
                // $('.user_products').append(html_string);
                $('.product_error').remove();
                addUserProduct.resetForm();
            },
            error: (data)=>{
                console.log('error response: ', data);
                // add error message to form
                if($('.product_error').length < 1) {
                    $('#productCode').after(`<p class='help is-danger product_error'>${data.responseJSON.message}</p>`);
                }
            }
        });
    })

    // download user product
    $(document).on('submit', '.downloadUserProduct', function(e){
        $(this).closest('form').find(':submit').addClass('is-loading');
        let product_name = $(this).find('input[name="name"]').val();
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: $(this).serialize(),
            xhrFields: {
                responseType: 'blob'
            },
            success: (data)=>{
                console.log('success data: ', data);
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                // need to make the download field dynamic
                // need update the userView with the just added product
                a.download = `${product_name}.zip`;
                a.click();
                window.URL.revokeObjectURL(url);
                $(this).closest('form')[0].reset();
                $('.product_error').remove();
                addUserProduct.resetForm();
                $(this).closest('form').find(':submit').removeClass('is-loading');
            },
            error: (data)=>{
                console.log('error response: ', data);
                // add error message to form
                if($('.product_error').length < 1) {
                    $('#productCode').after(`<p class='help is-danger product_error'>Please enter a valid Product code</p>`);
                }
            }
        });
    })

    $(document).on('click', '.logout', function(){
        $.ajax({
            url: '/logout',
            method: 'POST',
            success: (data)=>{
                console.log(data);
                $('.logout').addClass('is-hidden');
                $('#account').addClass('is-hidden');
                $('.user_products').html('');
                // $('.navbar-start a:nth-of-type(2)').on('click');
                $('.navbar-start a:nth-of-type(2)').addClass('trigger_popup_fricc');
                $(".trigger_popup_fricc").click(function(){
                    $('.hover_bkgr_register').show();
                 });
                // $('.navbar-start a:nth-of-type(2)').html('Register/Login');
                $('.navbar-start a:nth-of-type(2)').removeAttr('href');
            },
            error:(err)=>{
                console.log(err);
            }
        })
    })

    function buildUserProduct(product) {
        let davidMMChecker = '';
        if(product.name == 'davids_mighty_men'){
            davidMMChecker = 'disabled';
        }
        return `<div class="tile is-parent is-3">
            <article class="tile is-child box tile-background-color">
                <figure class="image box is-paddingless">
                    <img src="/static/images/01_12/${product.name}.png">
                </figure>
                <form class="downloadUserProduct" action="/enterCode/${product.number}">
                <div class="field">
                    <input type="hidden" name="name" value=${product.name}>
                </div>
                <div class="control has-text-centered">
                    <button type="submit" class="button is-primary" ${davidMMChecker}>Download</button>
                </div>
                </form>
            </article>
        </div>`
    }

    function userView(products = null) {
        let html_builder = '<div class="tile is-ancestor">';
        if(products) {
            let j = 0;
            for(let i = 0; i < products.length; i++) {
                html_builder += buildUserProduct(products[i]);
                j++;
                if(j%4 == 0 && i + 1 != products.length) {
                    html_builder += '</div><div class="tile is-ancestor">';
                }
            }
            html_builder += '</div>';
        }
                                    // <p class="title">${products[i].name}</p>
                                    // <p class="subtitle">Fri 27 Nov 2016</p>
        $('.user_products').html(html_builder);
        $('.hover_bkgr_register').hide();
        $('.hover_bkgr_login').hide();
        $('#account').removeClass('is-hidden');
        $('.logout').removeClass('is-hidden');
        $('.navbar-start a:nth-of-type(2)').off('click');
        $('.navbar-start a:nth-of-type(2)').removeClass('trigger_popup_fricc');
        $('.navbar-start a:nth-of-type(2)').addClass('navbar-item');
        $('.navbar-start a:nth-of-type(2)').attr('href', '#account');
        // $('.navbar-start a:nth-of-type(2)').html('Account');
        addUserProduct.resetForm();
    }
});