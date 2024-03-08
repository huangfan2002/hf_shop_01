var MyOrder = function () {
};

MyOrder.prototype.listenSubmitEvent = function () {
    $(".cancel-order-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var order_id = $this.attr('order-id');
        $.ajax({
            url: "/cancel_order/", // 修改 URL
            type: 'POST',
            data: {
                order_id: order_id
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




MyOrder.prototype.run = function () {
    this.listenSubmitEvent();
};


$(function () {
    var handler = new MyOrder();
    handler.run();
});