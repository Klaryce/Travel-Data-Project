(function (func) {
    var who=document.getElementById("who").innerHTML;
    //alert(who)
    $.ajax({
        url: "/data/cityCountWho/" + who,
        type: "GET",
        dataType: "json",
        success: function (data) {
            func(data.series_data);
            //alert(data.series_data)
        }
    });
})(function (data) {

    //alert(data)
    var myChart = echarts.init(document.getElementById('who_recommend_chart'), 'infographic');
    var data1 = [];
    var data2 = [];
    $(data).each(function (k, v) {
        data1.push(v.city);
        data2.push(v.price);
        //alert(v.city);
    });

    option = {
        tooltip: {
            trigger: 'axis',
            formatter: "{b} : {c}"
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                data: data1
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: 'Κά»¶Σ­¶Θ',
                type: 'bar',
                data: data2
            }
        ]
    };


    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });

});