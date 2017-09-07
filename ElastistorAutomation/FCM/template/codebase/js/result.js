function summary(strChartId,strTitle) {
    var chart;
    $(document).ready(function() {
    	
		var strPassCount=document.getElementsByName('PASS').length;
		var strFailCount=document.getElementsByName('FAIL').length;

		document.getElementById('pCount').innerHTML=strPassCount;
		document.getElementById('fCount').innerHTML=strFailCount;

    	 // Radialize the colors
        Highcharts.getOptions().colors = $.map(Highcharts.getOptions().colors, function(color) {
            return {
                radialGradient: { cx: 0.5, cy: 0.3, r: 0.7 },
                stops: [
                    [0, color],
                    [1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
                ]
            };
        });
        
        chart = new Highcharts.Chart({
            chart: {
                renderTo: strChartId,
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Pie Chart'
            },
            tooltip: {
        	    pointFormat: '{series.name}: <b>{point.percentage}%</b>',
            	percentageDecimals: 1
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function() {
                            return '<b>'+ this.point.name +'</b>: '+ Math.round(this.percentage) +' %';
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: strTitle,
                data: [{
                	name: 'Pass',
                	color: '#89A54E',
                	y: strPassCount
                }, {
                	name: 'Fail',
                	color: '#AA4643',
                	y: strFailCount
                }]
            }]
        });
    });
    
}
function detail(strChartId,strTitle) {
    var chart;
    $(document).ready(function() {
    	
		var strPassCount=document.getElementsByName('PASS').length;
		var strFailCount=document.getElementsByName('FAIL').length;


		document.getElementById('pCount').innerHTML=strPassCount;
		document.getElementById('fCount').innerHTML=strFailCount;

    	 // Radialize the colors
        Highcharts.getOptions().colors = $.map(Highcharts.getOptions().colors, function(color) {
            return {
                radialGradient: { cx: 0.5, cy: 0.3, r: 0.7 },
                stops: [
                    [0, color],
                    [1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
                ]
            };
        });
        
        chart = new Highcharts.Chart({
            chart: {
                renderTo: strChartId,
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Pie Chart'
            },
            tooltip: {
        	    pointFormat: '{series.name}: <b>{point.percentage}%</b>',
            	percentageDecimals: 1
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function() {
                            return '<b>'+ this.point.name +'</b>: '+ Math.round(this.percentage) +' %';
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: strTitle,
                data: [{
                	name: 'Pass',
                	color: '#89A54E',
                	y: strPassCount
                }, {
                	name: 'Fail',
                	color: '#AA4643',
                	y: strFailCount
                }]
            }]
        });
    });
    
}