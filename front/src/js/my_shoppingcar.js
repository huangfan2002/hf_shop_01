var MyShoppingCar = function () {
};

MyShoppingCar.prototype.listenRemoveEvent = function () {
    $(".cancel-order-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var my_shopping_car_id = $this.attr('sp-id');
        $.ajax({
            url: "/delete_shoppingcar/", // 修改 URL
            type: 'POST',
            data: {
                my_shopping_car_id
            },
            success: function (result) {
                if (result['code'] === 200) {
                    alert('取消成功');
                    location.reload()
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};

// GoodDetail.prototype.listenAddOrderEvent = function () {
//     $("#add-order-btn").on("click", function (event) {
//         event.preventDefault();
//         var $this = $(this);
//         var good_id = $this.attr('good-id');
//         $.ajax({
//             url: "/add_order/",
//             type: 'POST',
//             data: {
//                 good_id
//             },
//             success: function (result) {
//                 if (result['code'] === 200) {
//                     alert('购买成功');
//                     location.reload()
//                 } else {
//                     alert(result['message']);
//                 }
//             }
//         })
//     });
// };

MyShoppingCar.prototype.listenBuyEvent = function () {
    $(".get-order-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var good_id = $this.attr('sp-id');
        $.ajax({
            url: "/buy_shoppingcar/", // 修改 URL
            type: 'POST',
            data: {
                good_id
            },
            success: function (result) {
                if (result['code'] === 200) {
                    alert('购买成功');
                    location.reload()
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};



MyShoppingCar.prototype.run = function () {
    this.listenRemoveEvent();
    this.listenBuyEvent();
};


$(function () {
    var handler = new MyShoppingCar();
    handler.run();
});