(function (func) {
    $.ajax({
        url: "/data/getMoneyTrend",
        type: "GET",
        dataType: "json",
        success: function (data) {
            func(data);
        }
    });
})(function (data) {

    var myChart = echarts.init(document.getElementById('chart_3'), 'infographic');

    myChart.clear();
    var option = {
        title: {
            text: ''
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['旅游人均消费'],
            textStyle: {
                color: '#fff'
            },
            top: '8%'
        },
        grid: {
            top: '40%',
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        color: ['#FF4949', '#FFA74D', '#FFEA51', '#4BF0FF', '#44AFF0', '#4E82FF', '#584BFF', '#BE4DFF', '#F845F1'],
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: data.xAxis,
            splitLine: {
                show: false
            },
            axisLine: {
                lineStyle: {
                    color: '#fff'
                }
            }
        },
        yAxis: {
            name: '元',
            type: 'value',
            splitLine: {
                show: false
            },
            axisLine: {
                lineStyle: {
                    color: '#fff'
                }
            }
        },
        series: [
            {
                name: '人均消费（元）',
                type: 'line',
                data: data.series1
            }
        ]
    };
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });

});