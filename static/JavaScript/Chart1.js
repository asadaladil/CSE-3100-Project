
  // Load Google Charts
google.charts.load('current', { packages: ['corechart'] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() 
{
// Retrieve the 2D list from Django
const chartData = JSON.parse(document.getElementById('chart1').textContent);

// Convert to Google Charts DataTable format
const data = google.visualization.arrayToDataTable(chartData);

// Chart options
const options = {
    title: 'Column Chart from Django Data',
    legend: { position: 'none' },
    bars: 'vertical',  // Column chart (use 'horizontal' for bar chart)
};

// Render the chart
const chart = new google.visualization.ColumnChart(document.getElementById('chart1'));
chart.draw(data, options);
}
drawChart();
