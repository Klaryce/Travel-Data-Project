(function (func) {
    $.ajax({
        url: "/data/getMap",
        type: "GET",
        dataType: "json",
        success: function (data) {
            func(data);
        }
    });
})(function (data) {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('chart_map'));

    var mapName = 'china'

    /*获取地图数据*/
    myChart.showLoading();
    var mapFeatures = echarts.getMap(mapName).geoJson.features;
    myChart.hideLoading();
    var geoCoordMap = {
        '福州': [119.4543, 25.9222],
        '长春': [125.8154, 44.2584],
        '重庆': [107.7539, 30.1904],
        '西安': [109.1162, 34.2004],
        '成都': [103.9526, 30.7617],
        '常州': [119.4543, 31.5582],
        '北京': [116.4551, 40.2539],
        '北海': [109.314, 21.6211],
        '海口': [110.3893, 19.8516],
        '长沙': [113.019455, 28.200103],
        '上海': [121.40, 31.73],
        '内蒙古': [106.82, 39.67]
    };

    function get_latitude_longitude(item) {
        return item["name"].indexOf(window.cityname) > -1;
    }

    var color = ['#b77b49'];
    var series = [];
    var tmp_data = data.series.map(function (dataItem) {
        var cityname = dataItem[0].name;
        window.cityname = cityname;
        var tmp_area = areas.filter(get_latitude_longitude)[0];
        var data1 = [parseFloat(tmp_area["longitude"]),parseFloat(tmp_area["latitude"]),  dataItem[0].value];
        //alert(dataItem[0].value);
        return {
            name: cityname,
            value: data1
        };
    });

    series.push({
        name: "地理位置与受欢迎度",
        type: 'effectScatter',
        coordinateSystem: 'geo',
        zlevel: 2,
        rippleEffect: {
            brushType: 'stroke'
        },
        label: {
            normal: {
                show: true,
                position: 'right',
                formatter: '{b}'
            }
        },
        symbolSize: function (val) {
            return val[2] / 8;
        },
        itemStyle: {
            normal: {
                color: color[0]
            }
        },
        data: tmp_data
    });

    option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c}人"
        },
        geo: {
            map: 'china',
            label: {
                emphasis: {
                    show: false
                }
            },
            roam: true,
            itemStyle: {
                normal: {
                    borderColor: "#ffffff",
                    borderWidth: 1,
                    areaColor: {
                        type: 'radial',
                        x: 0.5,
                        y: 0.5,
                        r: 0.8,
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(175,175,100, 0)' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: 'rgba(30,30,10, .1)' // 100% 处的颜色
                        }],
                        globalCoord: false // 缺省为 false
                    },
                    shadowColor: '#d8ac7c',
                    // shadowColor: 'rgba(255, 255, 255, 1)',
                    shadowOffsetX: -2,
                    shadowOffsetY: 2,
                    shadowBlur: 10
                },
                emphasis: {
                    areaColor: '#d8ac7c',
                    borderWidth: 0
                }
            }
        },
        series: series
    };

    // 使用刚指定的配置项和数据显示图表。
    debugger;
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });

});

