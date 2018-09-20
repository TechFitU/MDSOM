
$(function() {

    Morris.Area({
        element: 'morris-area-chart',
        data: generateAreaChartData(),
        xkey: 'anho',
        ykeys: ['cantidad'],
        labels: ['Diagnosticos'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });

    //Grafico de pastel, que presenta los accidentes por tipo
    
 

    Morris.Donut({
        element: 'morris-donut-chart',
        data: generatePieChartData(),
        resize: true
    });
    Morris.Donut({
        element: 'morris-donut-chart2',
        data: generatePieChartData2(),
        resize: true
    });

    Morris.Donut({
        element: 'morris-donut-chart3',
        data: generatePieChartData3(),
        resize: true
    });

    Morris.Bar({
        element: 'morris-bar-chart',
        data: generateBarChartData(),
        xkey: 'fecha',
        ykeys: ['cantidad'],
        labels: ['Cantidad'],
        hideHover: 'auto',
        resize: true
    });

});
