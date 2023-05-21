/////////////////////////////////////////////////////       JS START   ///////////////////////////////
var d = new Date();
var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
document.getElementById("month_name").innerHTML = months[d.getMonth()];

//////////////////////////////////////////////////////  bar chart-Yearly  //////////////////////////////////////

  var data = [
  {x: months,y: {{yearly_data[2]}},type: 'bar',line: {color: '#17BECF'},visible: true},
  {x: months, y: {{yearly_data[1]}} ,type: 'bar',line: {color: '#17BECF'},visible: false},
  {x: months, y: {{yearly_data[0]}},type: 'bar',line: {color: '#17BECF'},visible: false}
]


var layout = {
title: 'Yearly Consimued Energy',
updatemenus: [{
  // label:"Year",
  direction: 'right',
        pad: {'r': 10, 't': 10},
        showactive: true,
        type: 'buttons',
        // x: 0.1,
        xanchor: 'left',
        y: 1.2,
        yanchor: 'top', 
        buttons: [{
            method: 'restyle',
            args: ['visible', [true, false,false]],
            label: '2020'
        }, {
            method: 'restyle',
            args: ['visible', [false, true,false]],
            label: '2019'
        }, {
            method: 'restyle',
            args: ['visible', [false,false, true]],
            label: '2018'
        }]
    }],
xaxis: {
  //range: ['2020-06-10 01:00', '2020-06-10 23:59'],
  title: 'Time',
  autorange: true,
 // type: 'time',
  fixedrange: true
  
},
yaxis: {
  // autorange: true,
  title: 'Consimued Energy (KWH)',
  fixedrange: true,
  // range: [1300, 1500],
  // type: 'linear'
}
};

Plotly.newPlot('yearly_plot', data, layout,{displayModeBar: false});

//////////////////////////////////////////////////////  bar chart-month  //////////////////////////////////////


// function monthly_plot(){  
var data = [
                    {x: {{monthly_date[1]|tojson}},y: {{monthly_data[0]}},line: {color: '#17BECF'},visible: true,type: 'bar'},
                    {x: {{monthly_date[1]|tojson}},y: {{monthly_data[1]}},line: {color: '#17BECF'},visible: false,type: 'bar'},
                    {x: {{monthly_date[2]|tojson}},y: {{monthly_data[2]}},line: {color: '#17BECF'},visible: false,type: 'bar'},
                    {x: {{monthly_date[3]|tojson}},y: {{monthly_data[3]}},line: {color: '#17BECF'},visible: false,type: 'bar'},
                    {x: {{monthly_date[4]|tojson}},y: {{monthly_data[4]}},line: {color: '#17BECF'},visible: false,type: 'bar'},
                    {x: {{monthly_date[5]|tojson}},y: {{monthly_data[5]}},line: {color: '#17BECF'},visible: false,type: 'bar'},
                    {x: {{monthly_date[6]|tojson}},y: {{monthly_data[6]}},line: {color: '#17BECF'},visible: false,type: 'bar'},
                    {x: {{monthly_date[7]|tojson}},y: {{monthly_data[7]}},line: {color: '#17BECF'},visible: false,type: 'bar'},
                    {x: {{monthly_date[8]|tojson}},y: {{monthly_data[8]}},line: {color: '#17BECF'},visible: false,type: 'bar'},
                    {x: {{monthly_date[9]|tojson}},y: {{monthly_data[9]}},line: {color: '#17BECF'},visible: false,type: 'bar'},
                    {x: {{monthly_date[10]|tojson}},y: {{monthly_data[10]}},line: {color: '#17BECF'},visible: false,type: 'bar'},
                    {x: {{monthly_date[11]|tojson}},y: {{monthly_data[11]}},line: {color: '#17BECF'},visible: false,type: 'bar'}
                    ];

var layout = {
    title: 'Monthly Consimued Energy',
updatemenus: [{
               // label:"Year",
               direction: 'right',
                pad: {'r': 10, 't': 10},
                showactive: true,
                // type: 'buttons',
                // x: 0.1,
                xanchor: 'left',
                y: 1.2,
                yanchor: 'top', 
                buttons: [   
                    {method: 'restyle',args: ['visible', [true, false,false,false,false,false,false,false,false,false,false,false]],label: months[0]},
                    {method: 'restyle',args: ['visible', [false, true,false,false,false,false,false,false,false,false,false,false]],label: months[1]},
                    {method: 'restyle',args: ['visible', [false, false,true,false,false,false,false,false,false,false,false,false]],label: months[2]},
                    {method: 'restyle',args: ['visible', [false, false,false,true,false,false,false,false,false,false,false,false]],label: months[3]},
                    {method: 'restyle',args: ['visible', [false, false,false,false,true,false,false,false,false,false,false,false]],label: months[4]},
                    {method: 'restyle',args: ['visible', [false, false,false,false,false,true,false,false,false,false,false,false]],label: months[5]},
                    {method: 'restyle',args: ['visible', [false, false,false,false,false,false,true,false,false,false,false,false]],label: months[6]},
                    {method: 'restyle',args: ['visible', [false, false,false,false,false,false,false,true,false,false,false,false]],label: months[7]},
                    {method: 'restyle',args: ['visible', [false, false,false,false,false,false,false,false,true,false,false,false]],label: months[8]},
                    {method: 'restyle',args: ['visible', [false, false,false,false,false,false,false,false,false,true,false,false]],label: months[9]},
                    {method: 'restyle',args: ['visible', [false, false,false,false,false,false,false,false,false,false,true,false]],label: months[10]},
                    {method: 'restyle',args: ['visible', [false, false,false,false,false,false,false,false,false,false,false,true]],label: months[11]}
                  ]
                   }],
            xaxis: {
              title: 'Time',
              autorange: true,
            // type: 'time',
              fixedrange: true
              
            },
            yaxis: {
              // autorange: true,
              title: 'Consimued Energy (KWH)',
              fixedrange: true,
              // range: [0, 5],
              // type: 'linear'
            }
  };


// Plotly.newPlot('monthly_plot', data, layout,{displayModeBar: false});
Plotly.newPlot('monthly_plot', data, layout,{displayModeBar: false});
// }
// monthly_plot()

////////////////////////////////   Pie Chart ///////////////////////////////////////////
var day_used = {{day_used}}
function pie_char(day_used){
var today = new Date();
var h = today.getHours();
var m = today.getMinutes();
h = (h + (m/60)).toFixed(2)
var data = [{
  values: [24-h,h],
  labels: [' ', h+' Hour'],  
  name: 'Hour',
  textinfo: 'label',
  hole: .55,
  type: 'pie',
  marker: {
  colors: ['rgba(57, 73, 219,.2)','rgba(57, 73, 219,1)']
}
}]
var layout = {
  title: {
      text: 'Daily Used Energy',
      font: {
        family: 'Times New Roman, monospace',
        size: 30,
        // color: '#7f7f7f'
      }
    },
  // font: [size: 25],
  annotations: [
    {
      font: {
        size: 26,
        family: 'Times New Roman, monospace',
        color: 'green'
      },
      showarrow: false,
      text: day_used + ' kWh',
      x: 0.5,
      y: 0.5
    },
  ],

  showlegend: false
};
Plotly.newPlot('daily_used', data, layout);
}
pie_char(day_used=day_used)
//////////////////////////////////////////////////////// Clock //////////////////////////////
function startTime(){
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  var d = today.getDate();
  var mn = today.getMonth()
  var y = today.getFullYear()
  h = checkTime(h)
  m = checkTime(m);
  s = checkTime(s);
  document.getElementById('datetime_1').innerHTML =+ h + ":" + m + ":" + s + ' - ' + d +'/'+ mn +'/'+ y;
  var t = setTimeout(startTime, 500);
}
function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
};

//////////////////////////////////////// Auto Update data //////////////////////////////

var refreshIntervalId = setInterval(httpReqIn, 30000)
    
function httpReqIn(){
      req = $.ajax({
        url : '/update',
        type : 'POST',
        data : { meter_id : {{current_user.meter_id}}, current_reading : {{current_reading}} }
    });
          
    req.done(function(data){  
      req_status = data.update_commit
      if(data.update=='yes'){     
      document.getElementById("monthly_used").innerHTML = data.month_used;
      document.getElementById("current_bill").innerHTML = (data.month_used*5).toFixed(2);
      document.getElementById("current_reading").innerHTML = data.current_reading;
      pie_char(day_used=data.day_used)
      monthly_plot(x_data=data.monthly_data_datetime,y_data=data.monthly_data_kwh)
      }
    });
}
