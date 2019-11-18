let colors = ["#008FFB", "#00E396", "#FFAD0F", "#FF4560", "#775DD0"];

function getOff(val) {
    let off = 0;
    if (Math.max.apply(null, val)-Math.min.apply(null, val) !== 0) {
        off = parseInt((Math.max.apply(null, val)-Math.min.apply(null, val))*0.03);
    }else{
        off = parseInt(Math.max.apply(null, val)*0.03);
    }
    if (off === 0) {
        off = 1;
    }
    return off;
}

function getMin(val){
    return (Math.min.apply(null, val)-getOff(val)>0 ? Math.min.apply(null, val)-getOff(val) : 0);
}

function getMax(val){
    return Math.max.apply(null, val)+getOff(val);
}

function init_chart(allDates, noData_text){
    let options = {
      chart: {type: (allDates.length <= 1 ? "scatter" : "line"), height: 400, animations: {enabled: false}, toolbar: {tools: {reset: false}}},
      dataLabels: {enabled: false},
      series: [{data: []}],
      xaxis: {
        type: 'datetime',
        min: moment(allDates[0], "DD/MM/YY").valueOf(),
        max: moment(allDates[allDates.length-1], "DD/MM/YYYY").valueOf(),
        tickAmount: 6,
      },
      tooltip: {x: {format: 'dd/MM/yyyy'}},
      stroke: {curve: "smooth"},
      noData: {text: noData_text, align: 'center', verticalAlign: 'middle'}
    }

    let chart = new ApexCharts(
      document.querySelector("#chart"),
      options
    );

    chart.render();

    return chart;
}

function update_chart(chart, name, data_table, dates, allDates){
    let data = [];
    let j = 0;
    let x = null;

    chart.clearAnnotations();

    for (let i = 0; i < allDates.length; i++) {
        if (dates.indexOf(allDates[i]) !== -1) {
            data.push([moment(dates[j], "DD/MM/YY").valueOf(), data_table[name][j]]);
            j++;
            if (x !== null){
                chart.addXaxisAnnotation({x: x, x2: moment(allDates[i], "DD/MM/YY").valueOf(), borderColor: "#FF0000", fillColor: "#FF000011",label: {borderColor: "#FFFFFF00",style: {color: "#FFFFFF00",background: "#FFFFFF00"}, text: "Missing data"}});
                x = null;
            }
        }else{
            data.push([moment(allDates[i], "DD/MM/YY").valueOf(), null]);
            if (x === null){
                x = moment(allDates[(i > 0 ? i-1 : 0)], "DD/MM/YY").valueOf();
            }
        }
    }

    if (x !== null){
        chart.addXaxisAnnotation({x: x, x2: moment(allDates[allDates.length-1], "DD/MM/YY").valueOf(), borderColor: "#FF0000", fillColor: "#FF000011",label: {borderColor: "#FFFFFF00",style: {color: "#FFFFFF00",background: "#FFFFFF00"}, text: "Missing data"}});
    }

    chart.updateOptions({
        title: {text: "Storico " + name, align: "left"},
        series: [{name: name, data: data}],
        yaxis: [{
            min: getMin(data_table[name]),
            max: getMax(data_table[name]),
            axisTicks: {show: true},
            axisBorder: {show: true},
            title: {text: name},
            labels: {formatter: function (value) {
                        return numeral(value).format("0,0");
                    }
            }
        }]
    });
}

function update_chart_eras(chart, name, data_table, dates, allDates){
    let series = [];
    let yaxis = [];
    let c = 0;
    let x = null;

    chart.clearAnnotations();

    for (let i in data_table[name]) {
        let data = [];
        let j = 0;

        for (let k = 0; k < allDates.length; k++) {
            if (dates.indexOf(allDates[k]) !== -1) {
                data.push([moment(dates[j], "DD/MM/YY").valueOf(), data_table[name][i][j]]);
                j++;
                if (x !== null){
                    chart.addXaxisAnnotation({x: x, x2: moment(allDates[k], "DD/MM/YY").valueOf(), borderColor: "#FF0000", fillColor: "#FF000011",label: {borderColor: "#FFFFFF00",style: {color: "#FFFFFF00",background: "#FFFFFF00"}, text: "Missing data"}});
                    x = null;
                }
            }else{
                data.push([moment(allDates[k], "DD/MM/YY").valueOf(), null]);
                if (x === null){
                    x = moment(allDates[(k > 0 ? k-1 : 0)], "DD/MM/YY").valueOf();
                }
            }
        }

        if (x !== null){
            chart.addXaxisAnnotation({x: x, x2: moment(allDates[allDates.length-1], "DD/MM/YY").valueOf(), borderColor: "#FF0000", fillColor: "#FF000011",label: {borderColor: "#FFFFFF00",style: {color: "#FFFFFF00",background: "#FFFFFF00"}, text: "Missing data"}});
        }

        series.push({name: i, data: data});
        yaxis.push({
            min: getMin(data_table[name][i]),
            max: getMax(data_table[name][i]),
            axisTicks: {show: true},
            axisBorder: {show: true, color: colors[c]},
            title: {text: i, style: {color: colors[c]}},
            labels: {style: {color: colors[c]},
                formatter: function (value) {
                    return numeral(value).format("0,0");
                }
            }
        });
        c++;
    }

    chart.updateOptions({
        title: {text: "Storico " + name, align: "left"},
        series: series,
        yaxis: yaxis,
        legend: {horizontalAlign: "left", position: "top"}
    });
}

function update_table(name, data_table, dates, allDates){
    $("#titolo").text(`Dati per '${name}' degli ultimi ${allDates.length} giorni`);
    $("tbody").empty();
    let x = 0;
    for (let i in allDates) {
        $("tbody").append(`<tr id="tr${i}"><td>${allDates[i]}</td></tr>`);
        if (dates.indexOf(allDates[i]) !== -1){
            $(`#tr${i}`).append(`<td>${numeral(data_table[name][x]).format("0,0")}</td>`);
            if (i > 0) {
                let diff = parseInt(data_table[name][x]) - parseInt(data_table[name][x-1]);
                if (diff > 0) {
                    $(`#tr${i}`).append(`<td><p class="green-text">+${numeral(diff).format("0,0")}<i class="material-icons">arrow_upward</i></p></td>`);
                } else if (diff < 0) {
                    $(`#tr${i}`).append(`<td><p class="red-text">${numeral(diff).format("0,0")}<i class="material-icons">arrow_downward</i></p></td>`);
                } else {
                    $(`#tr${i}`).append(`<td><p class="blue-text">${numeral(diff).format("0,0")}</p></td>`);
                }
            }else{
                $(`#tr${i}`).append("<td>No Data</td>");
            }
            x++;
        }else{
            $(`#tr${i}`).append("<td>No Data</td><td>No Data</td>");
        }
    }

    $("tbody").append(`<tr id="trlast"><td>Dal ${dates[0]} al ${dates[dates.length-1]}</td></tr>`);
    $("#trlast").append("<td></td>");
    let firstLast = (parseInt(data_table[name][dates.length-1]) - parseInt(data_table[name][0]));
    if (firstLast > 0) {
        $("#trlast").append(`<td><p class="green-text">+${numeral(firstLast).format("0,0")}<i class='material-icons'>arrow_upward</i></p></td>`);
    } else if (firstLast < 0) {
        $("#trlast").append(`<td><p class="red-text">${numeral(firstLast).format("0,0")}<i class='material-icons'>arrow_downward</i></p></td>`);
    } else {
        $("#trlast").append(`<td><p class="blue-text">${numeral(firstLast).format("0,0")}</p></td>`);
    }
}