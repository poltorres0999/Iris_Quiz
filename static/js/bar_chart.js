function barChart(chart_id, data, labels, label_value, title, colors) {
    var ctx = document.getElementById(chart_id).getContext('2d');
    return new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: label_value,
              backgroundColor: colors,
              data: data
            }
          ]
        },
        options: {
          legend: { display: false },
          title: {
            display: true,
            text: title
          }
        }
    });
}
