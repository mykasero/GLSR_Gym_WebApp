// Style and functionality looks good
$(function () { 

    var $activityChart = $("#profile_activity_chart");
    $.ajax({
        url: $activityChart.data("url"),
        success: function (data) {
            var ctx = $activityChart[0].getContext("2d");

            var maxDataValue = Math.max(...data.data);
                    
            if (maxDataValue < 10)  {
                if (maxDataValue % 2 == 0){
                    yAxisMax = Math.ceil(maxDataValue + 2);
                } else {
                    yAxisMax = Math.ceil(maxDataValue + 3);
                }
            } else if (maxDataValue < 20) {
                if (maxDataValue % 2 == 0){
                    yAxisMax = Math.ceil(maxDataValue + 4);
                } else {
                    yAxisMax = Math.ceil(maxDataValue + 5);
                }
            }  else {
                if (Math.ceil(maxDataValue/10)%2 == 1){
                    yAxisMax = (Math.ceil(maxDataValue/10)*10) + 10;
                } else {
                    yAxisMax = (Math.ceil(maxDataValue/10)*10);
                }
            }
            
            

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Dni w danym miesiącu',
                        backgroundColor: [
                            'rgba(0, 0, 255, 0.3)',
                            'rgba(0, 255, 55, 0.3)',
                        ],
                        borderColor: [
                            'rgba(0, 0, 200, 0.5)',
                            'rgba(0, 255, 0, 0.5)',
                        ],
                        borderWidth: 1,
                        data: data.data
                    }]
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'top',
                        align: 'start',
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Wykres aktywności',
                            position: 'top',
                            align: 'center',
                            font: {
                                weight: 'bold',
                                family: 'Helvetica',
                                size: 26,
                            },
                        },
                    },  
                scales: {
                    y: {
                        beginAtZero: true,
                        max: yAxisMax,
                    },
                },
                }
            });
        }
    });

});