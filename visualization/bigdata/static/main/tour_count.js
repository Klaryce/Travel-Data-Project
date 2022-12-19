(function (func) {
    $.ajax({
        url: "/data/getTourCount",
        type: "GET",
        dataType: "json",
        success: function (data) {
            func(data);
        }
    });
})(function (data) {

    var myChart = echarts.init(document.getElementById('chart_addition2'), 'infographic');

    var option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        calculable: true,
        series: [
            {
                name: '受欢迎度',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: data.series
            }
        ]
    };


    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });

});