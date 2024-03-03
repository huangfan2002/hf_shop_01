var GoodDetail = function () {

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

GoodDetail.prototype.run = function () {
    this.listenAddScoreEvent();
};


$(function () {
    var handler = new GoodDetail();
    handler.run();
});