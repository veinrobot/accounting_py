/* globals Chart:false, feather:false */
var wChart, mChart, yChart;
function a(din, dout, pin, pout){
  var itx = document.getElementById('weeksChart')
  var datapin = Array(7);
  var datapout = Array(7);
  datapin.fill(pin);
  datapout.fill(pout);
  wChart = echarts.init(itx);
  wChart.setOption({
    xAxis: [{
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },{
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      gridIndex: 1
    }],
    yAxis: [{
      type: 'value'
    },{
      type: 'value',
      gridIndex: 1
    }],
    tooltip: {
      trigger: 'axis'
    },
    title: [
      {
        left: '20%',
        text: '週收入'
      },
      {
        right: '20%',
        text: '週支出'
      }
    ],
    grid: [
      {
        left:'5%',
        right:'55%'
      },
      {
        right:'5%',
        left:'55%'
      }
    ],
    series: [
      {
        name: '實際收入',
        data: din,
        type: 'line'
      },
      {
        name: '預算收入',
        data: datapin,
        type: 'line'
      },
      {
        name: '實際支出',
        data: dout,
        type: 'line',
        xAxisIndex: 1,
        yAxisIndex: 1
      },
      {
        name: '預算支出',
        data: datapout,
        type: 'line',
        xAxisIndex: 1,
        yAxisIndex: 1
      }
    ]
  });
  wChart.resize();
}
function b(din, dout, pin, pout){
  var itx = document.getElementById('monthsChart')
  var now = new Date();
  var len = new Date(now.getFullYear(), now.getMonth()+1, 0).getDate();
  dates = Array.from({length: len}, (_, i) => i + 1)
  var datapin = Array(len);
  var datapout = Array(len);
  datapin.fill(pin);
  datapout.fill(pout);
  mChart = echarts.init(itx);
  mChart.setOption({
    xAxis: [{
      type: 'category',
      data: dates
    },{
      type: 'category',
      data: dates,
      gridIndex: 1
    }],
    yAxis: [{
      type: 'value'
    },{
      type: 'value',
      gridIndex: 1
    }],
    tooltip: {
      trigger: 'axis'
    },
    title: [
      {
        left: '20%',
        text: '月收入'
      },
      {
        right: '20%',
        text: '月支出'
      }
    ],
    grid: [
      {
        left:'5%',
        right:'55%'
      },
      {
        right:'5%',
        left:'55%'
      }
    ],
    series: [
      {
        name: '實際收入',
        data: din,
        type: 'line'
      },
      {
        name: '預算收入',
        data: datapin,
        type: 'line'
      },
      {
        name: '實際支出',
        data: dout,
        type: 'line',
        xAxisIndex: 1,
        yAxisIndex: 1
      },
      {
        name: '預算支出',
        data: datapout,
        type: 'line',
        xAxisIndex: 1,
        yAxisIndex: 1
      }
    ]
  });
  mChart.resize();
}
function c(din, dout, pin, pout){
  var itx = document.getElementById('yearsChart')
  var datapin = Array(12);
  var datapout = Array(12);
  datapin.fill(pin);
  datapout.fill(pout);
  yChart = echarts.init(itx);
  yChart.setOption({
    xAxis: [{
      type: 'category',
      data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },{
      type: 'category',
      data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      gridIndex: 1
    }],
    yAxis: [{
      type: 'value'
    },{
      type: 'value',
      gridIndex: 1
    }],
    tooltip: {
      trigger: 'axis'
    },
    title: [
      {
        left: '20%',
        text: '年收入'
      },
      {
        right: '20%',
        text: '年支出'
      }
    ],
    grid: [
      {
        left:'5%',
        right:'55%'
      },
      {
        right:'5%',
        left:'55%'
      }
    ],
    series: [
      {
        name: '實際收入',
        data: din,
        type: 'line'
      },
      {
        name: '預算收入',
        data: datapin,
        type: 'line'
      },
      {
        name: '實際支出',
        data: dout,
        type: 'line',
        xAxisIndex: 1,
        yAxisIndex: 1
      },
      {
        name: '預算支出',
        data: datapout,
        type: 'line',
        xAxisIndex: 1,
        yAxisIndex: 1
      }
    ]
  });
  yChart.resize();
}
function getData(obj){
  var cur = new Date();
  var monthDay = new Date(cur.getFullYear(), cur.getMonth()+1, 0).getDate();
  var i_day = 0, s_day = 0, iaw = 0, saw = 0, iam = 0, sam = 0, iay = 0, say = 0;
  var i_week = new Array(7).fill(0);
  var s_week = new Array(7).fill(0);
  var i_month = new Array(monthDay).fill(0);
  var s_month = new Array(monthDay).fill(0);
  var i_year = new Array(12).fill(0);
  var s_year = new Array(12).fill(0);
  for(var i = 0; i < obj.length; i++){
    var time = obj[i].date.split('-');
    if(sameYear(obj[i].date)){
      if(obj[i].types == '收入'){
        i_year[time[1]-1] += obj[i].amount;
        iay += obj[i].amount;
      }
      else{
        s_year[time[1]-1] += obj[i].amount;
        say += obj[i].amount;
      }
      if(sameMonth(obj[i].date)){
        if(obj[i].types == '收入'){
          i_month[time[2]-1] += obj[i].amount;
          iam += obj[i].amount;
        }
        else{
          s_month[time[2]-1] += obj[i].amount;
          sam += obj[i].amount;
        }
      }
    }
    if(week().includes(obj[i].date)){
      var weekDay = new Date(obj[i].date).getDay;
      if(weekDay == 0) weekDay = 7;
      if(obj[i].types == '收入'){
        i_week[weekDay-1] += obj[i].amount;
        iaw += obj[i].amount;
      }
      else{
        s_week[weekDay-1] += obj[i].amount;
        saw += obj[i].amount;
      }
    }
    if(obj[i].date == days(cur)){
      if(obj[i].types == '收入') i_day += obj[i].amount;
      else s_day += obj[i].amount;
    }
  }
  var data = {ia: [i_day, iaw, iam, iay], sa: [s_day, saw, sam, say], iw: sums(i_week), sw: sums(s_week), im: sums(i_month), sm: sums(s_month), iy: sums(i_year), sy: sums(s_year)};
  return data;
  
}
window.addEventListener('resize', function(){
  wChart.resize();
})
window.addEventListener('resize', function(){
  mChart.resize();
})
window.addEventListener('resize', function(){
  yChart.resize();
})
function week(){
  const today = new Date();
  const gD = today.getDay() == 0? 7 : today.getDay();
  var this_week = [];
  this_week.unshift(days(today));
  for(var i = 1; i < gD; i++){
    this_week.unshift(days(new Date(today.getTime()-(i*24*60*60*1000))));
  }
  for(var i = 1; i < 8-gD; i++){
    this_week.push(days(new Date(today.getTime()+(i*24*60*60*1000))));
  }
  return this_week;
}
function days(day){
  return new Intl.DateTimeFormat("fr-CA", {year: "numeric", month: "2-digit", day: "2-digit"}).format(day);
}
function sameMonth(dates){
  var x = dates.split('-');
  return new Date().getMonth()+1 == x[1] ? true : false;
}
function sameYear(dates){
  var x = dates.split('-');
  return new Date().getFullYear() == x[0] ? true : false;
}
function sums(array){
  var tmp = Array.from(array);
  for(var i = 1; i < tmp.length; i++) tmp[i] += tmp[i-1];
  return tmp;
}
function review(money){
  return (money/10).toFixed(2) + '瓶多多、' + (money/788).toFixed(2) + '份 minecraft、' + (money/3240).toFixed(2) + '單原神、' + (money/400000).toFixed(2) + '台重機';
}
function words(types, din, dout, pin, pout){
  var tps, tips, tips2;
  var balin = din - pin;
  var balout = dout - pout;
  var balall = balin - balout;
  var i = (balin > 0)? '多' : '少'
  var o = (balout > 0)? '多' : '少'
  var a = balall > 0? '賺' : '虧'
  var h = document.getElementById(types);
  if(types == 'daily') tps = '日';
  else if(types == 'weekly') tps = '週';
  else if(types == 'monthly') tps = '月';
  else if(types == 'annual') tps = '年';
  if(balin >= 0){
    tips = '做得好，繼續維持下去，你多賺的錢有' + Math.abs(balin) + '元，已經可以多買';
    if(balout > 0) tips2 = '但是你多花了' + Math.abs(balout) + '元，代表你大概浪費了'
    else tips2 = '而且你少花了' + Math.abs(balout) + '元，代表你又賺了'
  }
  else{
    tips = '你花太多錢了，已經超過預計' + Math.abs(balin) + '元，已經浪費了';
    if(balout > 0) tips2 = '而且你多花了' + Math.abs(balout) + '元，代表你的購買力又下降了'
    else tips2 = '但是你少花了' + Math.abs(balout) + '元，代表你購買力上升了'
  }
  h.getElementsByClassName("rev-in")[0].innerHTML = '你目前收入了' + din + '元，距離你預計的收入' + pin + '元' + i +'賺了'+ Math.abs(balin) +'元';
  h.getElementsByClassName("rev-out")[0].innerHTML = '你目前支出了' + dout + '元，距離你預計的支出' + pout + '元' + o +'花了'+ Math.abs(balout) +'元';
  h.getElementsByClassName("rev-earn")[0].innerHTML = tips + review(Math.abs(balin));
  h.getElementsByClassName("rev-spend")[0].innerHTML = tips2 + review(Math.abs(balout));
  h.getElementsByClassName("rev-con")[0].innerHTML = '盱衡上述，你當' + tps + '總共比預計多' + a + '了' + Math.abs(balall) + '元，相當於' + review(Math.abs(balall));
}
