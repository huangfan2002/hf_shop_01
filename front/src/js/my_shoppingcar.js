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




MyShoppingCar.prototype.run = function () {
    this.listenRemoveEvent();
};


$(function () {
    var handler = new MyShoppingCar();
    handler.run();
});