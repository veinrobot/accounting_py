/* globals Chart:false, feather:false */
var iChart, bChart, sChart;
function a(){
  var itx = document.getElementById('incomeChart')
  iChart = echarts.init(itx);
  iChart.setOption({
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [150, 230, 224, 218, 135, 147, 260],
        type: 'line'
      }
    ]
  });
  iChart.resize();
}
function b(){
  var itx = document.getElementById('balanceChart')
  bChart = echarts.init(itx);
  bChart.setOption({
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [230, 224, 218, 135, 147, 260, 150],
        type: 'line'
      }
    ]
  });
  bChart.resize();
}
function c(){
  var itx = document.getElementById('spendChart')
  sChart = echarts.init(itx);
  sChart.setOption({
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [224, 218, 135, 147, 260, 150, 230],
        type: 'line'
      }
    ]
  });
  sChart.resize();
}
(function () {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  a()
  
  // eslint-disable-next-line no-unused-vars
  
  
})()

var pill = document.getElementById('pills-income-tab')
var pill2 = document.getElementById('pills-balance-tab')
var pill3 = document.getElementById('pills-spend-tab')
pill.addEventListener('shown.bs.tab', a)
pill2.addEventListener('shown.bs.tab', b)
pill3.addEventListener('shown.bs.tab', c)
window.addEventListener('resize', function(){
  iChart.resize();
  bChart.resize();
  sChart.resize();
})