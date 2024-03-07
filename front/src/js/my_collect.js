var MyCollect = function () {
};

MyCollect.prototype.listenSubmitEvent = function () {
    $(".delete-collect-btn").on("click", function (event) {
        event.preventDefault();
        var $this = $(this);
        var collect_id = $this.attr('collect-id');
        $.ajax({
            url: "/delete_collect/",
            type: 'POST',
            data: {
                collect_id
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

MyCollect.prototype.run = function () {
    this.listenSubmitEvent();
};


$(function () {
    var handler = new MyCollect();
    handler.run();
});