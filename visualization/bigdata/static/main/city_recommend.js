

(function (func) {
    var city=document.getElementById("city").innerHTML;
    //alert(city)
    $.ajax({
        url: "/data/entCountCity/" + city,
        type: "GET",
        dataType: "json",
        success: function (data) {
            func(data.series_data);
        }
    });
})(function (data) {

    //alert(data)
    var myChart = echarts.init(document.getElementById('city_recommend_chart'), 'infographic');
    var data1 = [];
    var data2 = [];
    $(data).each(function (k, v) {
        data1.push(v.city);
        data2.push(v.price);
    });
    // alert("hey");
    // alert(data1)
    // alert(data2);
    option = {
        tooltip: {},
        radar: {
            name: {
                textStyle: {
                    color: 'black',
                    borderRadius: 3,
                    padding: [3, 5]
                }
            },
            indicator: [
                {name: data1[0], max: 160},
                {name: data1[1], max: 160},
                {name: data1[2], max: 160},
                {name: data1[3], max: 160},
                {name: data1[4], max: 160},
                {name: data1[5], max: 160}
            ],
        },
        series: [{
            type: 'radar',
            areaStyle: {normal: {}},
            data: [
                {name: "Popularity", value: data2}
            ]
        }]
    };


    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });

});


//
//
// (function (func) {
//     var city=document.getElementById("city").innerHTML;
//     //alert(city)
//     $.ajax({
//         url: "/data/entCountCity/" + city,
//         type: "GET",
//         dataType: "json",
//         success: function (data) {
//             func(data.series_data);
//         }
//     });
// })(function (data) {
//
//     //alert(data)
//     var myChart = echarts.init(document.getElementById('city_recommend_chart'), 'infographic');
//     var data1 = [];
//     var data2 = [];
//     $(data).each(function (k, v) {
//         data1.push(v.city);
//         data2.push(v.price);
//         //alert(v.city);
//     });
//
//     option = {
//         tooltip: {
//             trigger: 'axis',
//             formatter: "{b} : {c}"
//         },
//         calculable: true,
//         xAxis: [
//             {
//                 type: 'category',
//                 data: data1
//             }
//         ],
//         yAxis: [
//             {
//                 type: 'value'
//             }
//         ],
//         series: [
//             {
//                 name: 'ÈËÊý',
//                 type: 'bar',
//                 data: data2
//             }
//         ]
//     };
//
//
//     myChart.setOption(option);
//     window.addEventListener("resize", function () {
//         myChart.resize();
//     });
//
// });