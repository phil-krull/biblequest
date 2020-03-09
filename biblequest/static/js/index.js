$(window).on('load', function () {
    console.log(sessionStorage.getItem('access_token'));
    userView();
    // $.ajax({
    //     method: 'get',
    //     dataType: 'json',
    //     url: '/customer',
    //     success: function(data){
    //         console.log(data);
    //         if(data.status) {
    //             userView(data.products);
    //         }
    //     }
    // });

    // $('.profile').click(function(){
    //     $('.hover_bkgr_profile').show();
    // })


    let loginValidation = $('#login').validate({
        rules: {
            lemail: {
                required: true,
                email: true
            },
            lpassword: {
                required: true
            }
        },
        messages: {
            lemail: {
                required: 'Email field is required!',
                email: 'Please enter a valid email!'
            },
            lpassword: {
                required: 'Password field is required!'
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
                minlength: (8)
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
                minlength: 'Password must be at least 8 characters long'
            },
            rconfirm_password: {
                required: 'Confirm Password field is required!',
                equalTo: 'Passwords must match'
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

    let updateUserPassword = $('#profile').validate({
        rules: {
            new_password :{
                required: true,
                minlength: (8)
            },
            new_confirm_password: {
                required: true,
                equalTo: '#new_password'
            },
            old_password: {
                required: true
            }
        },
        messages: {
            new_password: {
                required: 'Please enter a password',
                minlength: 'Password must be at least 8 characters long',
            },
            new_confirm_password: {
                required: 'Please enter a password',
                equalTo: 'Passwords must match'
            }
        }
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
                $(this).closest('form')[0].reset();
                userView();
                resetAllForms();
            },
            error: (data)=>{
                registerValidation.showErrors({
                    'remail': 'Email already in use'
                })
            }
        })
    })
    
    $(document).on('submit', '#login', function(e){
        let email = $('#loginEmail').val();
        let password = $('#loginPassword').val();
        let test = JSON.stringify({
            "email": `${email}`,
            "password": `${password}`
        });
        // use jquery-plugin validator
        e.preventDefault();
        $.ajax({
            url: '/auth',
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            data: test,
            success: (data)=>{
                console.log(data);
                sessionStorage.setItem("access_token", data.access_token);
                $(this).closest('form')[0].reset();
                userView(data.products);
                resetAllForms();
            },
            error: (data)=>{
                loginValidation.showErrors({
                    'lpassword': 'Invalid email/password combination'
                });
            }
        })
    })

    // add user product and display newly added product
    $(document).on('submit', '.addUserProduct', function(e){
        let tile_ancestor = $('.user_products .tile ancestor:last').length;
        let token = sessionStorage.getItem('access_token');
        if(token) {
            e.preventDefault();
            $.ajax({
                url: $(this).attr('action'),
                method: 'POST',
                data: $(this).serialize(),
                headers: {
                    'Authorization': `JWT ${token}`
                },
                success: (data)=>{
                    $(this).closest('form')[0].reset();
                    let html_string = buildUserProduct(data['product']);
                    let tile_ancestor_length = $('.user_products .is-ancestor:last').children().length
                    if(tile_ancestor_length > 3) {
                        html_string = '<div class="tile is-ancestor">' + html_string + '</div>';
                        $('.user_products').append(html_string);
                    } else {
                        $('.user_products .is-ancestor:last').append(html_string);
                    }
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
        }
    })

    // download user product
    $(document).on('submit', '.downloadUserProduct', function(e){
        let token = sessionStorage.getItem('access_token');
        if(token) {
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
                headers: {
                    'Authorization': `JWT ${token}`
                },
                success: (data)=>{
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
                    // add error message to form
                    if($('.product_error').length < 1) {
                        $('#productCode').after(`<p class='help is-danger product_error'>Please enter a valid Product code</p>`);
                    }
                }
            });
        }
    })

    $(document).on('click', '.logout', function(){
        // let access_token = sessionStorage.getItem("access_token");
        // $.ajax({
        //     url: '/logout',
        //     method: 'POST',
        //     headers: {
        //         'Authorization': `JWT ${access_token}`
        //     },
        //     success: (data)=>{
        //         console.log(data);
        //         $('.logout').addClass('is-hidden');
        //         $('#account').addClass('is-hidden');
        //         $('#user-form').removeClass('is-hidden');
        //         $('.user_products').html('');
        //     },
        //     error:(err)=>{
        //         console.log(err);
        //     }
        // })
        sessionStorage.removeItem('access_token');
        $('.logout').addClass('is-hidden');
        // $('#account').addClass('is-hidden');
        $('#user-form').removeClass('is-hidden');
        $('.user_products').html('');
    })

    // update user password
    $(document).on('submit', '#profile', function(){
        let token = sessionStorage.getItem('access_token');
        if(token) {
            $.ajax({
                url: `/editCustomer/${need_password_here}`,
                method: 'PUT',
                headers: {
                    'Authorization': `JWT ${token}`
                },
                success: (data)=>{
                    
                },
                error: (err)=>{
                    
                }
            })
        }
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

    function buildUserView(products) {
        let html_builder = '<div class="tile is-ancestor">';
        let j = 0;
        for(let i = 0; i < products.length; i++) {
            html_builder += buildUserProduct(products[i]);
            j++;
            if(j%4 == 0 && i + 1 != products.length) {
                html_builder += '</div><div class="tile is-ancestor">';
            }
        }
        html_builder += '</div>';
        $('.user_products').html(html_builder);
        $('#user-form').addClass('is-hidden');
        // $('#account').removeClass('is-hidden');
        // $('.profile').removeClass('is-hidden');
        $('.logout').removeClass('is-hidden');
        // addUserProduct.resetForm();
    }

    function userView() {
        let token = sessionStorage.getItem('access_token');
        accountView();
        if(token) {
            $.ajax({
                method: 'get',
                dataType: 'json',
                url: '/customer_page',
                headers: {
                    'Authorization': `JWT ${token}`
                },
                success: function(data){
                    console.log(data);
                    buildUserView(data.products);
                },
                error: function(err) {
                    console.log(err);
                    sessionStorage.removeItem('access_token');
                }
            });
        } else {
            loginRegView();
        }
    }

    function accountView() {
        $('.column-display').html(`
            <div class="container has-text-centered">
                <h2 class="title">Account</h2>
                <p class="subtitle is-6">This is the file account section for Bible Quest. Logging in here gives you
                    access to any digital content for Bible Quest products that you own. If you have a new product
                    that includes digital content, enter your product key precisely in the box below to activate
                    your files and make them available to download. <span class="has-text-weight-bold">Please
                        Note:</span> This "files account" is a separate account from the account that allows posting
                    comments on the blog or in the forums. A separate log-in for these community resources will be
                    required.</p>
                <form class="addUserProduct" action="/addProductToUser">
                    <div class="field">
                        <label for="productCode" class="label">Enter Product Code</label>
                        <div class="control">
                            <input id="productCode" class="input" name='acode' type="text" placeholder="code">
                        </div>
                    </div>
                    <div class="control">
                        <button class="button is-primary">Submit</button>
                    </div>
                </form>
                <h2 class='title'>Your products</h2>
            </div>
            <div class="container">
                <article class="user_products">
                </article>
            </div>
            <div class="container has-text-centered">
                <h2 class="title">Contact</h2>
        
                <form action="email" method="post">
                    <div class="field is-horizontal">
                        <div class="field-body">
                            <div class="field">
                                <p class="control has-icons-left">
                                    <input class="input" type="text" name="email_name" placeholder="Name">
                                    <span class="icon is-small is-left">
                                        <i class="fas fa-user"></i>
                                    </span>
                                </p>
                            </div>
                            <div class="field">
                                <p class="control has-icons-left has-icons-right">
                                    <input class="input" type="email" name="email_email" placeholder="Email">
                                    <span class="icon is-small is-left">
                                        <i class="fas fa-envelope"></i>
                                    </span>
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="field is-horizontal">
                        <div class="field-body">
                            <div class="field">
                                <div class="control">
                                    <textarea class="textarea" name="email_message" placeholder="Message us"></textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="field is-horizontal">
                        <div class="field-body">
                            <div class="field">
                                <div class="control">
                                    <button class="button is-primary has-text-white has-text-weight-bold">
                                        Send message
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
            </div>`

        );
    }

    function loginRegView() {
        $('.column-display').html(`
            <div class="columns">
                <div class="column is-6">
                    <h1 class="title is-3">Register</h1>
                    <form id="register" class="formToReset" action="/registerCustomer" method="post">
                        <div class="field">
                            <label for="registerName" class="label">Name</label>
                            <div class="control">
                                <input id="registerName" name="rname" class="input" type="text" placeholder="Name">
                            </div>
                        </div>

                        <div class="field">
                            <label for="registerEmail" class="label">Email</label>
                            <div class="control has-icons-left has-icons-right">
                                <input id="registerEmail" name="remail" class="input" type="email"
                                    placeholder="Email">
                                <span class="icon is-small is-left">
                                    <i class="fas fa-envelope"></i>
                                </span>
                                <span class="icon is-small is-right">
                                    <i class="fas fa-exclamation-triangle"></i>
                                </span>
                            </div>
                        </div>

                        <div class="field">
                            <label for="registerPhoneNumber" class="label">Phone Number</label>
                            <div class="control">
                                <input id="registerPhoneNumber" name="rphone_number" class="input" type="text"
                                    placeholder="xxx-xxx-xxxx">
                            </div>
                        </div>

                        <div class="field">
                            <label for="registerAddress" class="label">Address</label>
                            <div class="control">
                                <input id="registerAddress" name="raddress" class="input" type="text"
                                    placeholder="Address">
                            </div>
                        </div>

                        <div class="field">
                            <label for="registercity" class="label">City</label>
                            <div class="control">
                                <input id="registercity" name="rcity" class="input" type="text"
                                    placeholder="Enter a City">
                            </div>
                        </div>

                        <div class="columns">
                            <div class="field column is-one-thirds">
                                <label for="registerState" class="label">State</label>
                                <div class="control">
                                    <select id="registerState" name="rstate" class="input">
                                    </select>
                                </div>
                            </div>

                            <div class="field column is-one-thirds">
                                <label for="registerZip" class="label">Zip Code</label>
                                <div class="control">
                                    <input id="registerZip" name="rzip" class="input" type="number"
                                        placeholder="Zip Code">
                                </div>
                            </div>
                        </div>

                        <div class="field">
                            <label for="registerPassword" class="label">Password</label>
                            <div class="control">
                                <input id="registerPassword" name="rpassword" class="input" type="password"
                                    placeholder="Enter a Password">
                            </div>
                        </div>

                        <div class="field">
                            <label for="registerConfirm_password" class="label">Confirm Password</label>
                            <div class="control">
                                <input id="registerConfirm_password" name="rconfirm_password" class="input"
                                    type="password" placeholder="Please re-enter password">
                            </div>
                        </div>

                        <div class="field">
                            <label for="registerPurpose" class="label">How will you use our product?</label>
                            <div class="control">
                                <select id="registerPurpose" name="rpurpose" class="input">
                                    <option selected disabled>Choose an option</option>
                                    <option value="1">Home</option>
                                    <option value="2">Church</option>
                                    <option value="3">Other</option>
                                </select>
                            </div>
                        </div>

                        <div class="field is-grouped">
                            <div class="control">
                                <button class="button is-link">Register</button>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="column is-6">
                    <h1 class="title is-3">Login</h1>
                    <form id="login" class="formToReset" action="/loginCustomer" method="post">
                        <div class="field">
                            <label for="loginEmail" class="label">Email</label>
                            <div class="control has-icons-left has-icons-right">
                                <input id="loginEmail" name="lemail" class="input" type="email" placeholder="Email">
                                <span class="icon is-small is-left">
                                    <i class="fas fa-envelope"></i>
                                </span>
                                <span class="icon is-small is-right">
                                    <i class="fas fa-exclamation-triangle"></i>
                                </span>
                            </div>
                        </div>

                        <div class="field">
                            <label for="loginPassword" class="label">Password</label>
                            <div class="control">
                                <input id="loginPassword" name="lpassword" class="input" type="password"
                                    placeholder="Enter Password">
                            </div>
                        </div>

                        <div class="field is-grouped">
                            <div class="control">
                                <button class="button is-link">Login</button>
                            </div>
                        </div>
                    </form>
                </div>
        </div>`);
    }
});