google.load("visualization", "1", {
	packages: ["corechart"]
});
google.setOnLoadCallback(drawChart);

function drawChart() {
	var table = new google.visualization.DataTable();

	table.addColumn('string', 't');
	table.addColumn('number', 'k_tot');
	table.addColumn('number', 'no_pms');
	table.addColumn({
		type: 'string',
		role: 'annotation'
	});

	//load file and parse it
	$.getJSON('parse.me.json',
		function(data) {
			console.log(data.t_real);
			console.log(data.avg_k);
			console.log(data.avg_pms);
			console.log(data.no_X);
			console.log(data.no_boot);
			console.log(data.no_resize);
			console.log(data.no_delete);
			console.log(data.snapshots);
			prev = [0, 0]
			$.each(data.snapshots,
				function(key, value) {
					console.log(key + ' ' + value);
					var row;
					if (value instanceof Array) {
						row = ['t' + key, value[0], value[1], null];
						prev = value
					} else {
						row = ['t' + key, prev[0], prev[1], 'X'];
					}
					table.addRow(row);
				}
			);

			console.log(data);

			var TOT_K_COL = '#F44336';
			var NO_PMS_COL = '#3F51B5';

			var options = {
				title: 'Simulation History',
				curveType: 'function',
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

			var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

			chart.draw(table, options);
		}
	);
}