$(document).ready(function () {
    var infoMessage = $(".recent-purchase");
    const phoneInput = document.getElementById('id_phone_number');
    
    /*----------------------------- Добавление товара в корзину со страницы каталога ------------------------------ */
    $(document).on("click", ".ec-pro-actions .add-to-cart", function (e) {
        e.preventDefault();

        var product_id = $(this).data("product-id");
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                var count = $(".cart-count-lable").html();        
                count++;

                $(".cart-count-lable").html(count);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

                var modalCartItemsContainer = $("#ec-side-cart");
                modalCartItemsContainer.html(data.modal_cart_items_html);
            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    /*----------------------------- Добавление товара в корзину со страницы товара ------------------------------ */
    $(document).on("click", ".ec-single-qty .qty-plus-minus .ec_qtybtn", function(e) {
        e.preventDefault();
        var $productqtybutton = $(this);
        var ProductQtyoldValue = $productqtybutton.parent().parent().find("input").val();

        if ($productqtybutton.text() === "+") {
            var ProductQtynewVal = parseFloat(ProductQtyoldValue) + 1;
        } else {

            if (ProductQtyoldValue > 1) {
                var ProductQtynewVal = parseFloat(ProductQtyoldValue) - 1;
            } else {
                ProductQtynewVal = 1;
            }
        }
        $productqtybutton.parent().parent().find("input").val(ProductQtynewVal);
    })

    $(document).on("click", ".ec-single-cart .add-to-cart", function(e) {
        e.preventDefault();

        var product_id = $(this).parent().parent().find("input").data("product-id");
        var add_to_cart_url = $(this).attr("href");

        var product_qty = parseInt($(this).parent().parent().find("input").val());

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                product_qty: product_qty,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                var count = parseInt($(".cart-count-lable").html());  
                count += product_qty;       
                $(".cart-count-lable").html(count);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

                var modalCartItemsContainer = $("#ec-side-cart");
                modalCartItemsContainer.html(data.modal_cart_items_html);

                var cartSummaryContainer = $("#cart-summary-container");
                cartSummaryContainer.html(data.total);
                },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    })

    /*----------------------------- Изменение корзины в модальном окне ------------------------------ */
    $(document).on("click", ".ec-pro-content .qty-plus-minus .ec_qtybtn", function(e) {
        e.preventDefault();

        var $cartqtybutton = $(this);
        var CartQtyoldValue = $cartqtybutton.parent().parent().find("input").val();

        var url = $cartqtybutton.parent().parent().find("input").data("cart-change-url");
        var cartID = $cartqtybutton.parent().parent().find("input").data("cart-id");

        if ($cartqtybutton.text() === "+") {
            var CartQtynewVal = parseFloat(CartQtyoldValue) + 1;
            updateCart(cartID, CartQtynewVal, 1, url);
        } else {

            if (CartQtyoldValue > 1) {
                var CartQtynewVal = parseFloat(CartQtyoldValue) - 1;
                updateCart(cartID, CartQtynewVal, -1, url);
            } else {
                CartQtynewVal = 1;
            }
        }
        
        $cartqtybutton.parent().parent().find("input").val(CartQtynewVal);
    });

    /*----------------------------- Изменение корзины на странице корзины  ------------------------------ */
    $(document).on("click", ".cart-qty-plus-minus .ec_cart_qtybtn .ec_qtybtn", function(e) {
        e.preventDefault();

        var $qtybutton = $(this);
        var QtyoldValue = $qtybutton.parent().parent().find("input").val();

        var url = $qtybutton.parent().parent().find("input").data("cart-change-url");
        var cartID = $qtybutton.parent().parent().find("input").data("cart-id");

        if ($qtybutton.text() === "+") {
            var QtynewVal = parseFloat(QtyoldValue) + 1;
            updateCart(cartID, QtynewVal, 1, url);
        } else {

            if (QtyoldValue > 1) {
                var QtynewVal = parseFloat(QtyoldValue) - 1;
                updateCart(cartID, QtynewVal, -1, url);
            } else {
                QtynewVal = 1;
            }
        }

        $qtybutton.parent().find("input").val(QtynewVal);
    });

    /*----------------------------- Обновление данных в корзине  ------------------------------ */
    function updateCart(cartID, quantity, change, url) {

        var count = parseInt($(".cart-count-lable").html());    

        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                change: change,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {

                if (data.message) {
                    $("#recent-notification").html(data.message);
                    infoMessage.removeClass("invisible")

                    // count = data.qty;
                    $(".cart-count-lable").html(data.qty);

                    setTimeout(function () {
                        infoMessage.addClass("invisible");
                    }, 4000);

                } else {
                    count += change; 
                    $(".cart-count-lable").html(count);
                }

                // Изменяем количество товаров в значке корзины
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

                var modalCartItemsContainer = $("#ec-side-cart");
                modalCartItemsContainer.html(data.modal_cart_items_html);

                var cartSummaryContainer = $("#cart-summary-container");
                cartSummaryContainer.html(data.total);

            },
            error: function (data) {
                console.log("Ошибка при изменении количества товара в корзине");
            },
        });
    }

    /*----------------------------- Удаление товаров из корзины  ------------------------------ */
    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault()

        var cart_id = $(this).data("cart-id");
        var remove_from_cart = $(this).attr("href");
        var count = parseInt($(".cart-count-lable").html());  

        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {

                if (data.message) {
                    $("#recent-notification").html(data.message);
                    infoMessage.removeClass("invisible")

                    count = data.qty;

                    setTimeout(function () {
                        infoMessage.addClass("invisible");
                    }, 4000);
        
                } else {
                    count -= data.quantity_deleted;    

                }
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

                var modalCartItemsContainer = $("#ec-side-cart");
                modalCartItemsContainer.html(data.modal_cart_items_html);

                var cartSummaryContainer = $("#cart-summary-container");
                cartSummaryContainer.html(data.total);

                $(".cart-count-lable").html(count);

            },
            error: function (data) {
                console.log("Ошибка при удалении товара из корзины");
            },
        });
    });

    /*----------------------------- Форматирование номера телефона  ------------------------------ */
    if (phoneInput) {
        phoneInput.addEventListener('input', function (e) {
            var digits = e.target.value.replace(/\D/g, '').replace(/^7/, '');

            if (digits.startsWith('7') || digits.startsWith('8')) {
                digits = digits.slice(1);
            }
        
            var x = digits.match(/(\d{0,3})(\d{0,3})(\d{0,4})/);

            e.target.value = '+7(' + (
                !x[2] 
                    ? x[1]
                    : x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '')
            );
        });
    }

      /*----------------------------- Показ и скрытие поля для адреса доставки  ------------------------------ */
    $("#id_delivery_address_field").hide();
    $("#id_plus_delivery").hide();

    $("input[name='delivery_method']").change(function () {
        var selectedValue = $(this)

        var baseTotal = parseFloat($("#id_total_price").data("price").replace(",", "."));
        var totalprice = parseFloat($("#id_total_price").text().replace(",", "."));
        
        if (selectedValue.data("option") === "False") {
            $("#id_delivery_address_field").hide();
            $("#id_plus_delivery").hide();
            
            if (totalprice > baseTotal) {
                totalprice = baseTotal
            }
            
        } else {
            $("#id_delivery_address_field").show();
            $("#id_plus_delivery").show();
            
            var deliveryPrice = parseFloat($("#id_plus_delivery").data("delivery").replace(",", "."));
            totalprice = baseTotal + deliveryPrice;
        }
        $("#id_total_price").text(totalprice.toFixed(2).replace(".", ",") + " ₽");
    
    });

    /*----------------------------- Создание заказа  ------------------------------ */
    $(document).on("click", "#id_create_order_button", function (e) {

        var phoneNumber = $('#id_phone_number').val();
        var regex = /^\+7\(\d{3}\) \d{3}-\d{4}$/;
    
        if (!regex.test(phoneNumber)) {

            $('#phone_number_error').show();
            e.preventDefault();

        } else {

            $('#phone_number_error').hide();

            let allData = [];

            allData = allData.concat($("#id_user_info_form").serializeArray());
            allData = allData.concat($("#id_delivery_form").serializeArray());
            allData = allData.concat($("#id_payment_form").serializeArray());

            var url = $('#create_order_form').attr('action');

            createOrder(allData, url);
        }
    });

    function createOrder(allData, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: $.param(allData),
            
            success: function (data) {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                }
            },
            error: function (xhr) {

            $('.form-error').remove();

                if (xhr.responseJSON) {
                    const allErrors = {
                        ...xhr.responseJSON.user_errors,
                        ...xhr.responseJSON.delivery_errors,
                        ...xhr.responseJSON.payment_errors,
                    };

                    for (const [field, msgs] of Object.entries(allErrors)) {
                        const $input = $(`[name="${field}"]`);
                        if ($input.length) {
                            $('<div class="form-error alert alert-danger">')
                                .text(msgs.join(', '))
                                .insertAfter($input);
                        }
                    }
                }

                if (xhr.responseJSON.message) {
                    $("#recent-notification").html(xhr.responseJSON.message);
                    infoMessage.removeClass("invisible")
    
                    setTimeout(function () {
                        infoMessage.addClass("invisible");
                    }, 4000);
    
                }
            },
        });
    }

    /*----------------------------- Редактирование профиля  ------------------------------ */
    $('#updateForm').on('submit', function (e) {
        e.preventDefault();
    
        var formData = new FormData(this);

        $.ajax({
            url: "/user/update-profile/",
            type: "POST",
            data: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
              },
            contentType: false,
            processData: false,
            success: function (data) {

                if (data.success) {
                    setTimeout(() => {
                        $('#edit_modal').modal('hide');
                        location.reload();
                      }, 100);
                }
            },
            error: function (data) {

                const errors = data.responseJSON.errors;
                $('.form-error').remove();

                for (let field in errors) {
                    const messages = errors[field];
                    const $input = $(`[name="${field}"]`);
                    if ($input.length) {
                        $('<div class="form-error alert alert-danger mt-1">')
                        .html(messages.map(msg => `<div>${msg}</div>`).join(''))
                        .insertAfter($input);
                    }
                }
            },
        });
    });
        
});