var GoodDetail = function () {

};


GoodDetail.prototype.listenAddShoppingCar = function () {
    $("#add-shoppingcar-btn").on("click", function (event) {
       event.preventDefault();
        var $this = $(this);
        var good_id = $this.attr('good-id');
        $.ajax({
            url: "/add_shoppingcar/",
            type: 'POST',
            data: {
                good_id
            },
            success: function (result) {
                if (result['code'] === 200) {
                    alert('加入购物车成功');
                    location.reload()
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};

GoodDetail.prototype.listenAddCommentEvent = function () {
    $("#add-comment-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var good_id = $this.attr('good-id');
        var content = $('#comment-textarea').val();

        $.ajax({
            url: "/add_comment/",
            type: 'POST',
            data: {
                good_id,
                content
            },
            success: function (result) {
                if (result['code'] === 200) {
                    alert('发布成功');
                    location.reload()
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};

GoodDetail.prototype.listenAddScoreEvent = function () {
    $("#score-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var good_id = $this.attr('good-id');
        var score = $('#input-score').val();
        $.ajax({
            url: "/add_score/",
            type: 'POST',
            data: {
                good_id,
                score
            },
            success: function (result) {
                if (result['code'] === 200) {
                    alert('提交成功');
                    location.reload()
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};

GoodDetail.prototype.listenAddCollectEvent = function () {
    $("#add-collect-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var good_id = $this.attr('good-id');
        $.ajax({
            url: "/add_collect/",
            type: 'POST',
            data: {
                good_id
            },
            success: function (result) {
                if (result['code'] === 200) {
                    alert('收藏成功');
                    location.reload()
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};


GoodDetail.prototype.listenAddOrderEvent = function () {
    $("#add-order-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var good_id = $this.attr('good-id');
        $.ajax({
            url: "/add_order/",
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


GoodDetail.prototype.run = function () {
    this.listenAddScoreEvent();
    this.listenAddCommentEvent();
    this.listenAddCollectEvent();
    this.listenAddOrderEvent();
    this.listenAddShoppingCar();
};


$(function () {
    var handler = new GoodDetail();
    handler.run();
});