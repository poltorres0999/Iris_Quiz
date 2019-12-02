//doughnut
function doughnutChart(chart_id, data, labels, title, colors) {
   return new Chart(document.getElementById(chart_id), {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [
        {
          label: title,
          backgroundColor: colors,
          data: data
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: title
      }
    }
	});
}
