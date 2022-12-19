(function (func) {
    $.ajax({
        url: "/data/getWhoCount",
        type: "GET",
        dataType: "json",
        success: function (data) {
            func(data);
        }
    });
})(function (data) {

    var myChart = echarts.init(document.getElementById('chart_10'), 'infographic');

    myChart.clear();


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
                radius: [30, 110],
                roseType: 'area',
                x: '50%',               // for funnel
                max: 40,                // for funnel
                sort: 'ascending',     // for funnel
                data: data.series1
            }
        ]
    };


    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });

});