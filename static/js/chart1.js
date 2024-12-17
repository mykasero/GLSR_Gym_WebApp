// Style and functionality looks good
$(function () { 

    var $activityChart = $("#profile_activity_chart");
    $.ajax({
        url: $activityChart.data("url"),
        success: function (data) {
            var ctx = $activityChart[0].getContext("2d");
            
            function calculateAxisMax(maxDataValue){
                if (maxDataValue < 10)  {
                    return maxDataValue % 2 === 0 ? axisMax = Math.ceil(maxDataValue+2) : axisMax = Math.ceil(maxDataValue + 3);
                } else if (maxDataValue < 20) {
                    return maxDataValue % 2 === 0 ? axisMax = Math.ceil(maxDataValue + 4) : axisMax = Math.ceil(maxDataValue + 5);

                }  else {
                    return Math.ceil(maxDataValue / 10) % 2 === 1
                        ? axisMax = (Math.ceil(maxDataValue / 10) * 10) + 10
                        : axisMax = (Math.ceil(maxDataValue / 10) * 10);
                }
            }
            
            //change chart to horizontal on small screens
            function getChartOrientation(){
                return window.matchMedia("(max-width:768px)").matches ? 'y' : 'x'; 
            }

            var initialOrientation = getChartOrientation();
            var maxDataValue = Math.max(...data.data);
            var axisMax = calculateAxisMax(maxDataValue);
            
            Chart.defaults.scales.linear.max = axisMax; // set the new default max axis value to the calculated one

            var activityChart = new Chart(ctx, {
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
                    indexAxis: initialOrientation, // Dynamic orientation
                    maintainAspectRatio: false,
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
                }
            });
           
            // Add an event listener to re-render the chart on screen resize
            window.addEventListener('resize', function(){
                var newOrientation = getChartOrientation();
                if (activityChart.options.indexAxis !== newOrientation){
                    activityChart.options.indexAxis = newOrientation;
                    
                    axisMax = calculateAxisMax(maxDataValue);                   
                    
                    if (newOrientation === 'x') {
                        activityChart.options.scales.x = {
                            beginAtZero: true,
                            max: axisMax, // Apply max value explicitly for x-axis
                        };
                        activityChart.options.scales.y = {}; // Clear inactive axis
                    } else {
                        activityChart.options.scales.y = {
                            beginAtZero: true,
                            max: axisMax, // Apply max value explicitly for y-axis
                        };
                        activityChart.options.scales.x = {}; // Clear inactive axis
                    }
                    
                    activityChart.update(); //Update the chart
                }
            });
        }
    });

});