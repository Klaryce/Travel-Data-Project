(function (func) {
    $.ajax({
        url: "/data/getMonthCount",
        type: "GET",
        dataType: "json",
        success: function (data) {
            func(data);
        }
    });
})(function (data) {

    var myChart = echarts.init(document.getElementById('chart_2'), 'infographic');

    myChart.clear();
    //alert(data.count);
    // var data1 = [];
    // var data2 = [];
    // $(data).each(function (k, v) {
    //     data1.push(v.xAxis);
    //     data2.push(v.series1.value);
    // });
    // alert(data1);
    // alert(data2);

    var option = {
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
        orient: 'horizontal',
        bottom: 10,
        data: data.xAxis
    },
    series: [
        {
            name: '受欢迎度（人数）',
            type: 'pie',
            selectedMode: 'single',
            radius: [0, '30%'],

            label: {
                position: 'inner'
            },
            labelLine: {
                show: false
            },
            data: [
                {value: data.count[0] + data.count[1] + data.count[2], name: '春季', selected: true},
                {value: data.count[3] + data.count[4] + data.count[5], name: '夏季'},
                {value: data.count[6] + data.count[7] + data.count[8], name: '秋季'},
                {value: data.count[9] + data.count[10] + data.count[11], name: '冬季'}
            ]
        },
        {
            name: '受欢迎度（人数）',
            type: 'pie',
            radius: ['40%', '55%'],
            label: {
                formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                backgroundColor: '#eee',
                borderColor: '#aaa',
                borderWidth: 1,
                borderRadius: 4,
                // shadowBlur:3,
                // shadowOffsetX: 2,
                // shadowOffsetY: 2,
                // shadowColor: '#999',
                // padding: [0, 7],
                rich: {
                    a: {
                        color: '#999',
                        lineHeight: 22,
                        align: 'center'
                    },
                    // abg: {
                    //     backgroundColor: '#333',
                    //     width: '100%',
                    //     align: 'right',
                    //     height: 22,
                    //     borderRadius: [4, 4, 0, 0]
                    // },
                    hr: {
                        borderColor: '#aaa',
                        width: '100%',
                        borderWidth: 0.5,
                        height: 0
                    },
                    b: {
                        fontSize: 16,
                        lineHeight: 33
                    },
                    per: {
                        color: '#eee',
                        backgroundColor: '#334455',
                        padding: [2, 4],
                        borderRadius: 2
                    }
                }
            },
            data: [
                {value: data.count[0], name: data.xAxis[0]},
                {value: data.count[1], name: data.xAxis[1]},
                {value: data.count[2], name: data.xAxis[2]},
                {value: data.count[3], name: data.xAxis[3]},
                {value: data.count[4], name: data.xAxis[4]},
                {value: data.count[5], name: data.xAxis[5]},
                {value: data.count[6], name: data.xAxis[6]},
                {value: data.count[7], name: data.xAxis[7]},
                {value: data.count[8], name: data.xAxis[8]},
                {value: data.count[9], name: data.xAxis[9]},
                {value: data.count[10], name: data.xAxis[10]},
                {value: data.count[11], name: data.xAxis[11]}
            ]
        }
    ]
};

    // var option = {
    //     tooltip: {
    //         trigger: 'item',
    //         formatter: "{a} <br/>{b} : {c} ({d}%)"
    //     },
    //     legend: {
    //         orient: 'vertical',
    //         x: 'left',
    //         data: data.xAxis
    //     },
    //
    //     calculable: true,
    //     series: [
    //         {
    //             name: '受欢迎度',
    //             type: 'pie',
    //             radius: ['50%', '70%'],
    //             itemStyle: {
    //                 normal: {
    //                     label: {
    //                         show: false
    //                     },
    //                     labelLine: {
    //                         show: false
    //                     }
    //                 },
    //                 emphasis: {
    //                     label: {
    //                         show: true,
    //                         position: 'center',
    //                         textStyle: {
    //                             fontSize: '30',
    //                             fontWeight: 'bold'
    //                         }
    //                     }
    //                 }
    //             },
    //             data: data.series1
    //         }
    //     ]
    // };


    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });

});