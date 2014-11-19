var truncateDecimal = function(num) {
    return Math.round(num * 100) / 100;
};

var parseSimStats = function(statsInfo) {
    rows = [];

    $.ajax({
        url: statsInfo.fileName,
        dataType: 'json',
        async: false,
        success: function(data) {

            data.avg_k = truncateDecimal(data.avg_k);
            data.avg_pms = truncateDecimal(data.avg_pms);
            statsInfo.stats.data = data;
            prev = [0, 0];
            $.each(data.snapshots,
                function(key, value) {
                    var row;
                    if (value instanceof Array) {
                        row = ['t' + key, value[0], value[1], null];
                        prev = value
                    } else {
                        row = ['t' + key, prev[0], prev[1], 'X'];
                    }
                    rows.push(row);
                }
            );


        }
    });

    var TOT_K_COL = '#D50000';
    var NO_PMS_COL = '#CDDC39';

    var options = {
        curveType: 'none',
        series: {
            0: {
                targetAxisIndex: 0
            },
            1: {
                targetAxisIndex: 1
            }
        },
        hAxis: {
            showTextEvery: 10
        },
        vAxes: {
            0: {
                title: 'Total Consumption',
            },
            1: {
                title: 'Number of PMs',
            }
        },
        colors: [TOT_K_COL, NO_PMS_COL, 'black']
    };
    var cols = [{
        label: "t",
        type: "string"
    }, {
        label: "Total Consumption",
        type: "number"
    }, {
        label: "Number of PMs",
        type: "number"
    }, {
        role: "annotation",
        type: "string"
    }];
    var chart = statsInfo.chart;
    chart.setAttribute("options", JSON.stringify(options));
    chart.setAttribute("cols", JSON.stringify(cols));
    chart.setAttribute("rows", JSON.stringify(rows));
}

var parseAggrStats = function (aggrStats) {
    $.ajax({
        url: 'data/aggregate.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            aggrStats.data = {};
            aggrStats.data.perc_no_pms = data.perc_no_pms * 100;
            aggrStats.data.perc_k = data.perc_x * 100;
            aggrStats.data.perc_x = data.perc_k * 100;
        }
    });
};

var smartChart = document.querySelector('#smart-chart');
var smartStats = document.querySelector('#smart-stats');
var smartStatsInfo = {
    chart: smartChart,
    stats: smartStats,
    fileName: 'data/smart_chart.json',
};
parseSimStats(smartStatsInfo);


var normChart = document.querySelector('#norm-chart');
var normStats = document.querySelector('#norm-stats');
var normStatsInfo = {
    chart: normChart,
    stats: normStats,
    fileName: 'data/chart.json',
};
parseSimStats(normStatsInfo);

var aggrStats = document.querySelector('#aggr-stats');
parseAggrStats(aggrStats);

smartChart.addEventListener("google-chart-render", function  () {
    //smartChart.drawChart();
})

$(window).resize(function() {
    smartChart.drawChart();
    normChart.drawChart();
});