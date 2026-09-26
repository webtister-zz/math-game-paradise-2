#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成长方形和正方形 - 含可交互方格绘图PK游戏"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))

T = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{title} - PK对战</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Microsoft YaHei',sans-serif;background:linear-gradient(180deg,#1a1a2e,#16213e,#0f3460);min-height:100vh;overflow-y:auto;user-select:none;-webkit-user-select:none;color:#fff}}
.top-bar{{display:flex;align-items:center;justify-content:center;padding:8px;gap:10px;background:rgba(0,0,0,0.4);flex-wrap:wrap}}
.top-bar h1{{font-size:1.1em;background:linear-gradient(90deg,#FFD700,#6C5CE7,#4ECDC4);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.timer{{font-size:1.5em;font-weight:bold;color:#FFD700;min-width:60px;text-align:center}}
.round-info{{font-size:0.85em;color:#aaa}}
.module-badge{{font-size:0.75em;background:rgba(108,92,231,0.25);color:#a78bfa;padding:2px 10px;border-radius:10px}}
.main-area{{display:flex;flex:1;gap:0;min-height:calc(100vh - 200px)}}
.player-panel{{flex:1;display:flex;flex-direction:column;align-items:center;padding:10px 8px;position:relative;overflow-y:auto;transition:all 0.3s}}
.player-panel.left{{background:linear-gradient(180deg,rgba(255,107,107,0.12),rgba(0,0,0,0.3));border-right:3px solid #FF6B6B}}
.player-panel.right{{background:linear-gradient(180deg,rgba(78,205,196,0.12),rgba(0,0,0,0.3));border-left:3px solid #4ECDC4}}
.player-name{{font-size:1.1em;font-weight:bold;margin-bottom:4px;display:flex;align-items:center;gap:6px}}
.left .player-name{{color:#FF6B6B}}
.right .player-name{{color:#4ECDC4}}
.player-score{{font-size:2em;font-weight:bold;margin:4px 0}}
.left .player-score{{color:#FF6B6B}}
.right .player-score{{color:#4ECDC4}}
.streak{{font-size:0.8em;color:#FFD700;min-height:20px}}

/* 绘图区域 */
.draw-wrap{{background:rgba(255,255,255,0.06);border-radius:14px;padding:12px;margin:6px 0;text-align:center;display:flex;flex-direction:column;align-items:center}}
.draw-task{{font-size:0.9em;color:#FFD700;margin-bottom:6px;font-weight:bold;line-height:1.3}}
.draw-hint{{font-size:0.75em;color:#aaa;margin-bottom:4px}}
canvas{{display:block;border-radius:6px;cursor:crosshair;background:#1a1a2e;margin:0 auto;max-width:100%;touch-action:none}}
.draw-btns{{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;justify-content:center}}
.draw-btn{{padding:6px 14px;border-radius:14px;border:1.5px solid rgba(255,255,255,0.3);background:rgba(255,255,255,0.08);color:#ccc;font-size:0.78em;font-weight:bold;cursor:pointer;font-family:inherit;transition:all 0.2s}}
.draw-btn:hover{{border-color:#fff;background:rgba(255,255,255,0.15);color:#fff}}
.draw-btn.submit{{background:linear-gradient(135deg,#FFD700,#FF9800);color:#333;border:none}}
.left .draw-btn.submit{{background:linear-gradient(135deg,#FF6B6B,#ee5a5a);color:#fff;border:none}}
.right .draw-btn.submit{{background:linear-gradient(135deg,#4ECDC4,#2aa);color:#fff;border:none}}
.draw-btn:disabled{{opacity:0.4;pointer-events:none}}

/* 选择题（与之前相同） */
.question-box{{background:rgba(255,255,255,0.1);border-radius:14px;padding:14px 10px;margin:6px 0;width:100%;text-align:center;min-height:50px;display:flex;align-items:center;justify-content:center;font-size:1.05em;line-height:1.4;flex-direction:column}}
.options-grid{{display:grid;grid-template-columns:1fr 1fr;gap:6px;width:100%;margin:6px 0}}
.p-opt{{padding:10px 6px;border-radius:12px;border:2px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.05);color:#fff;font-size:0.85em;font-weight:bold;cursor:pointer;transition:all 0.2s;font-family:inherit;text-align:center;line-height:1.3;min-height:44px;display:flex;align-items:center;justify-content:center}}
.p-opt:hover{{background:rgba(255,255,255,0.15);border-color:rgba(255,255,255,0.5);transform:scale(1.04)}}
.p-opt:active{{transform:scale(0.94)}}
.p-opt.correct{{background:#10B981!important;border-color:#10B981!important;animation:pop 0.4s}}
.p-opt.wrong{{background:#EF4444!important;border-color:#EF4444!important;animation:shake 0.4s}}
.p-opt:disabled{{pointer-events:none;opacity:0.5}}
@keyframes pop{{0%{{transform:scale(1)}}50%{{transform:scale(1.1)}}100%{{transform:scale(1)}}}}
@keyframes shake{{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-6px)}}75%{{transform:translateX(6px)}}}}

.feedback{{font-size:0.85em;font-weight:bold;min-height:22px;text-align:center;margin:3px 0}}
.vs-badge{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:2.5em;font-weight:bold;z-index:10;text-shadow:0 0 30px rgba(255,215,0,0.8);pointer-events:none;animation:vsPulse 1.5s infinite}}
@keyframes vsPulse{{0%,100%{{opacity:0.6;transform:translate(-50%,-50%)scale(1)}}50%{{opacity:1;transform:translate(-50%,-50%)scale(1.1)}}}}
.bottom-bar{{display:flex;align-items:center;justify-content:center;gap:16px;padding:8px;background:rgba(0,0,0,0.5);flex-wrap:wrap}}
.module-bar{{display:flex;align-items:center;justify-content:center;gap:6px;padding:6px 8px;background:rgba(0,0,0,0.3);flex-wrap:wrap}}
.mod-btn{{padding:7px 10px;border-radius:14px;border:2px solid rgba(255,255,255,0.25);background:rgba(255,255,255,0.05);color:#ccc;font-size:0.72em;font-weight:bold;cursor:pointer;font-family:inherit;transition:all 0.2s;white-space:nowrap;line-height:1.3}}
.mod-btn:hover{{border-color:rgba(255,255,255,0.5);background:rgba(255,255,255,0.1);color:#fff}}
.mod-btn.active{{border-color:#a78bfa!important;background:rgba(108,92,231,0.25)!important;color:#a78bfa!important;box-shadow:0 0 12px rgba(108,92,231,0.35)}}
.ctrl-btn{{padding:10px 22px;border-radius:20px;border:none;font-size:0.9em;font-weight:bold;cursor:pointer;font-family:inherit;transition:all 0.2s}}
.ctrl-btn.start{{background:linear-gradient(135deg,#FFD700,#FF9800);color:#333}}
.ctrl-btn.restart{{background:linear-gradient(135deg,#FF6B6B,#ee5a5a);color:#fff}}
.ctrl-btn.music{{background:rgba(255,255,255,0.1);color:#fff;border:1px solid rgba(255,255,255,0.3)}}
.ctrl-btn:hover{{transform:translateY(-2px);box-shadow:0 4px 15px rgba(0,0,0,0.3)}}
.win-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:100;display:none;align-items:center;justify-content:center;flex-direction:column}}
.win-overlay.show{{display:flex}}
.win-title{{font-size:2.5em;font-weight:bold;margin-bottom:10px;animation:bounceIn 0.6s}}
.win-subtitle{{font-size:1.2em;color:#ccc;margin-bottom:20px}}
.win-scores{{display:flex;gap:40px;margin-bottom:20px}}
.win-player{{text-align:center}}
.win-player .wscore{{font-size:3em;font-weight:bold}}
@keyframes bounceIn{{0%{{transform:scale(0.3);opacity:0}}50%{{transform:scale(1.1)}}100%{{transform:scale(1);opacity:1}}}}
.confetti{{position:fixed;pointer-events:none;z-index:101;animation:fall linear forwards}}
@keyframes fall{{0%{{transform:translateY(-100px)rotate(0);opacity:1}}100%{{transform:translateY(105vh)rotate(720deg);opacity:0}}}}
.feedback-popup{{position:fixed;top:20px;left:50%;transform:translateX(-50%);padding:10px 24px;border-radius:20px;font-weight:bold;font-size:1em;z-index:90;animation:fadeInOut 1.5s forwards;pointer-events:none}}
@keyframes fadeInOut{{0%{{opacity:0;top:30px}}20%{{opacity:1;top:20px}}80%{{opacity:1;top:20px}}100%{{opacity:0;top:10px}}}}

@media(max-width:700px){{
  .main-area{{flex-direction:column}}
  .player-panel.left{{border-right:none;border-bottom:3px solid #FF6B6B}}
  .player-panel.right{{border-left:none;border-top:3px solid #4ECDC4}}
  canvas{{width:260px!important;height:260px!important}}
  .mod-btn{{font-size:0.65em;padding:5px 7px}}
}}
</style>
</head>
<body>
<div class="top-bar">
  <h1>{title} ⚔️ PK对战</h1>
  <span class="module-badge" id="mdBadge">模块一</span>
  <span class="round-info">第 <span id="rn">1</span>/10 轮</span>
  <span class="timer">⏱ <span id="tm">20</span>s</span>
</div>

<div class="module-bar" id="moduleBar">
  <button class="mod-btn active" onclick="switchModule(0)">模块一<br>垂线和平行线</button>
  <button class="mod-btn" onclick="switchModule(1)">模块二<br>画垂线•绘</button>
  <button class="mod-btn" onclick="switchModule(2)">模块三<br>点到直线距离•绘</button>
  <button class="mod-btn" onclick="switchModule(3)">模块四<br>平行线距离•绘</button>
  <button class="mod-btn" onclick="switchModule(4)">模块五<br>长方形正方形特征</button>
  <button class="mod-btn" onclick="switchModule(5)">模块六<br>画长方形正方形•绘</button>
</div>

<div class="main-area">
  <div class="player-panel left" id="p1panel">
    <div class="player-name">🔴 红方玩家</div>
    <div class="player-score" id="s1">0</div>
    <div class="streak" id="st1"></div>
    <div id="content1">选择模块后<br>点击开始对战</div>
    <div class="feedback" id="fb1"></div>
  </div>
  <div class="vs-badge">⚡VS⚡</div>
  <div class="player-panel right" id="p2panel">
    <div class="player-name">🔵 蓝方玩家</div>
    <div class="player-score" id="s2">0</div>
    <div class="streak" id="st2"></div>
    <div id="content2">选择模块后<br>点击开始对战</div>
    <div class="feedback" id="fb2"></div>
  </div>
</div>

<div class="bottom-bar">
  <button class="ctrl-btn start" id="btnStart" onclick="startGame()">⚔️ 开始对战</button>
  <button class="ctrl-btn music" id="btnMusic" onclick="toggleMusic()">🔊 音乐</button>
  <button class="ctrl-btn restart" onclick="restartGame()">🔄 重新开始</button>
</div>

<div class="win-overlay" id="winOverlay">
  <div class="win-title" id="winTitle"></div>
  <div class="win-subtitle" id="winSub"></div>
  <div class="win-scores">
    <div class="win-player left-w"><div style="color:#FF6B6B">🔴 红方</div><div class="wscore" id="ws1">0</div></div>
    <div class="win-player right-w"><div style="color:#4ECDC4">🔵 蓝方</div><div class="wscore" id="ws2">0</div></div>
  </div>
  <button class="ctrl-btn restart" onclick="restartGame()" style="font-size:1.2em;padding:14px 36px">🔄 再来一局</button>
  <button class="ctrl-btn restart" onclick="backToMenu()" style="font-size:1em;padding:10px 28px;margin-top:10px;background:rgba(255,255,255,0.1);color:#fff;border:1px solid rgba(255,255,255,0.3)">📋 选择其他模块</button>
</div>

<script>
// ─── GLOBAL STATE ───
var ALL_Q = {all_questions};
var Q = [];
var curModule = 0;
var sc=[0,0],cr=0,tr=10,tm=20,ti=null,go=false,ans=[false,false];
var sk='pk_'+window.location.pathname.replace(/[^a-zA-Z0-9]/g,'_');
var musicOn=true,actx=null;
// per-player draw state
var drawState = [null, null]; // {{lines:[], firstPt:null, canvas:null, ctx:null, gridSize:10, spacing:28}}

var modNames = ['模块一：判断垂线和平行线','模块二：画垂线','模块三：点到直线的距离','模块四：平行线之间的距离','模块五：长方形和正方形特征','模块六：画长方形和正方形'];

function sf(a){{var r=a.slice();for(var i=r.length-1;i>0;i--){{var j=Math.floor(Math.random()*(i+1));var t=r[i];r[i]=r[j];r[j]=t;}}return r;}}

function initAudio(){{if(!actx){{actx=new(window.AudioContext||window.webkitAudioContext)();}}}}
function playTone(f,d,ty,vol){{if(!musicOn||!actx)return;try{{var o=actx.createOscillator();var g=actx.createGain();o.type=ty||'sine';o.frequency.setValueAtTime(f,actx.currentTime);g.gain.setValueAtTime(vol||0.1,actx.currentTime);g.gain.exponentialRampToValueAtTime(0.001,actx.currentTime+d);o.connect(g);g.connect(actx.destination);o.start();o.stop(actx.currentTime+d);}}catch(e){{}}}}
function sfxCorrect(){{playTone(523,0.15,'square',0.08);setTimeout(function(){{playTone(659,0.15,'square',0.08);}},100);setTimeout(function(){{playTone(784,0.2,'square',0.08);}},200);}}
function sfxWrong(){{playTone(200,0.3,'sawtooth',0.06);}}
function sfxWin(){{for(var i=0;i<5;i++){{setTimeout(function(){{playTone(523+Math.random()*500,0.2,'square',0.07);}},i*150);}}}}
function sfxTick(){{playTone(800,0.05,'sine',0.04);}}
function toggleMusic(){{initAudio();musicOn=!musicOn;document.getElementById('btnMusic').textContent=musicOn?'🔊 音乐':'🔇 静音';if(musicOn)playTone(440,0.1,'sine',0.05);}}

function switchModule(idx){{
  if(go)return;
  curModule=idx;
  Q=ALL_Q[idx].slice();
  document.getElementById('mdBadge').textContent=modNames[idx].substring(0,6);
  var btns=document.querySelectorAll('.mod-btn');
  btns.forEach(function(b,i){{b.classList.toggle('active',i===idx);}});
  document.getElementById('content1').innerHTML='已选：'+modNames[idx]+'<br>点击开始对战';
  document.getElementById('content2').innerHTML='已选：'+modNames[idx]+'<br>点击开始对战';
  document.getElementById('fb1').innerHTML='';
  document.getElementById('fb2').innerHTML='';
}}

function startGame(){{
  initAudio();
  if(Q.length===0)Q=ALL_Q[curModule].slice();
  document.getElementById('btnStart').style.display='none';
  document.getElementById('moduleBar').style.display='none';
  go=true;sc=[0,0];cr=0;ans=[false,false];
  document.getElementById('s1').textContent='0';
  document.getElementById('s2').textContent='0';
  document.getElementById('winOverlay').classList.remove('show');
  Q=sf(Q);
  nextRound();
}}

function nextRound(){{
  if(cr>=tr){{endGame();return;}}
  ans=[false,false];
  document.getElementById('rn').textContent=cr+1;
  var q=Q[cr];
  var isDraw = (q.draw!==undefined);
  renderQuestion(1,q,isDraw);
  renderQuestion(2,q,isDraw);
  tm=isDraw?25:12;
  document.getElementById('tm').textContent=tm;
  clearInterval(ti);
  ti=setInterval(function(){{
    tm--;
    document.getElementById('tm').textContent=tm;
    if(tm<=5)sfxTick();
    if(tm<=0){{clearInterval(ti);timeUp();}}
  }},1000);
}}

// ====== 绘图模式 ======
function renderDraw(pn, drawDef){{
  var h='<div class="draw-wrap">';
  h+='<div class="draw-task">'+drawDef.task+'</div>';
  if(drawDef.hint)h+='<div class="draw-hint">'+drawDef.hint+'</div>';
  h+='<canvas id="cv'+pn+'" width="'+drawDef.w+'" height="'+drawDef.h+'"></canvas>';
  h+='<div class="draw-btns">';
  h+='<button class="draw-btn" onclick="clearDraw('+pn+')">🔄 清除</button>';
  h+='<button class="draw-btn" onclick="undoDraw('+pn+')">↩ 撤销</button>';
  h+='<button class="draw-btn submit" onclick="submitDraw('+pn+','+cr+',this)" id="subBtn'+pn+'">✓ 提交答案</button>';
  h+='</div></div>';
  document.getElementById('content'+pn).innerHTML=h;
  document.getElementById('fb'+pn).innerHTML='';

  // Init canvas
  var cv=document.getElementById('cv'+pn);
  var ctx=cv.getContext('2d');
  var gs=drawDef.gridSize||10;
  var sp=Math.floor(Math.min(cv.width,cv.height)/(gs+1));
  var st={{lines:[], firstPt:null, canvas:cv, ctx:ctx, gridSize:gs, spacing:sp, givenLines:drawDef.given||[], givenPoints:drawDef.points||[], check:drawDef.check, labels:drawDef.labels||{{}}}};
  drawState[pn-1]=st;
  renderGrid(pn);
  // click handler
  cv.onclick=function(e){{
    if(!go||ans[pn-1])return;
    var rect=cv.getBoundingClientRect();
    var scaleX=cv.width/rect.width;
    var scaleY=cv.height/rect.height;
    var mx=(e.clientX-rect.left)*scaleX;
    var my=(e.clientY-rect.top)*scaleY;
    var st2=drawState[pn-1];
    if(!st2)return;
    // snap to nearest grid point
    var col=Math.round(mx/st2.spacing);
    var row=Math.round(my/st2.spacing);
    if(col<0||col>st2.gridSize||row<0||row>st2.gridSize)return;
    var px=col*st2.spacing;
    var py=row*st2.spacing;
    if(st2.firstPt===null){{
      st2.firstPt={{col:col,row:row,x:px,y:py}};
    }}else{{
      // draw line from firstPt to this point
      if(st2.firstPt.col===col && st2.firstPt.row===row){{st2.firstPt=null;renderGrid(pn);return;}} // deselect
      st2.lines.push({{
        x1:st2.firstPt.x, y1:st2.firstPt.y,
        x2:px, y2:py,
        c1:st2.firstPt.col, r1:st2.firstPt.row,
        c2:col, r2:row
      }});
      st2.firstPt=null;
    }}
    renderGrid(pn);
  }};
}}

function renderGrid(pn){{
  var st=drawState[pn-1];
  if(!st)return;
  var ctx=st.ctx, cv=st.canvas, gs=st.gridSize, sp=st.spacing;
  var w=cv.width, h=cv.height;
  ctx.clearRect(0,0,w,h);
  // background
  ctx.fillStyle='#1a1a2e';
  ctx.fillRect(0,0,w,h);
  // grid dots
  for(var r=0;r<=gs;r++){{
    for(var c=0;c<=gs;c++){{
      var x=c*sp, y=r*sp;
      ctx.fillStyle='rgba(255,255,255,0.25)';
      ctx.beginPath();ctx.arc(x,y,2,0,Math.PI*2);ctx.fill();
    }}
  }}
  // given lines (pre-drawn, by teacher)
  var given=st.givenLines||[];
  for(var i=0;i<given.length;i++){{
    var gl=given[i];
    ctx.strokeStyle='rgba(255,255,255,0.5)';
    ctx.lineWidth=2;
    ctx.setLineDash([6,3]);
    ctx.beginPath();
    ctx.moveTo(gl.c1*sp, gl.r1*sp);
    ctx.lineTo(gl.c2*sp, gl.r2*sp);
    ctx.stroke();
    ctx.setLineDash([]);
  }}
  // given points (highlighted)
  var pts=st.givenPoints||[];
  for(var i=0;i<pts.length;i++){{
    var p=pts[i];
    ctx.fillStyle='#FFD700';
    ctx.beginPath();ctx.arc(p.c*sp, p.r*sp,5,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle='#FFD700';ctx.lineWidth=1.5;
    ctx.beginPath();ctx.arc(p.c*sp, p.r*sp,5,0,Math.PI*2);ctx.stroke();
  }}
  // labels
  var lbs=st.labels||{{}};
  for(var key in lbs){{
    if(!lbs.hasOwnProperty(key))continue;
    var lp=lbs[key];
    ctx.fillStyle='#FFD700';
    ctx.font='bold 11px "Courier New",monospace';
    ctx.fillText(key, lp.c*sp+6, lp.r*sp-6);
  }}
  // first selected point
  if(st.firstPt!==null){{
    ctx.fillStyle='#4ECDC4';
    ctx.beginPath();ctx.arc(st.firstPt.x, st.firstPt.y,6,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle='#fff';ctx.lineWidth=2;
    ctx.beginPath();ctx.arc(st.firstPt.x, st.firstPt.y,6,0,Math.PI*2);ctx.stroke();
  }}
  // drawn lines
  var color=pn===1?'#FF6B6B':'#4ECDC4';
  for(var i=0;i<st.lines.length;i++){{
    var l=st.lines[i];
    ctx.strokeStyle=l.correct? '#10B981' : (l.wrong? '#EF4444' : color);
    ctx.lineWidth=l.correct||l.wrong?3:2.5;
    ctx.beginPath();
    ctx.moveTo(l.x1,l.y1);
    ctx.lineTo(l.x2,l.y2);
    ctx.stroke();
    // endpoints
    ctx.fillStyle=ctx.strokeStyle;
    ctx.beginPath();ctx.arc(l.x1,l.y1,3.5,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(l.x2,l.y2,3.5,0,Math.PI*2);ctx.fill();
  }}
}}

function clearDraw(pn){{
  if(!go||ans[pn-1])return;
  var st=drawState[pn-1];
  if(!st)return;
  st.lines=[];
  st.firstPt=null;
  renderGrid(pn);
}}

function undoDraw(pn){{
  if(!go||ans[pn-1])return;
  var st=drawState[pn-1];
  if(!st)return;
  if(st.firstPt!==null){{st.firstPt=null;renderGrid(pn);return;}}
  if(st.lines.length>0)st.lines.pop();
  renderGrid(pn);
}}

function submitDraw(pn,round,btn){{
  if(!go||ans[pn-1])return;
  ans[pn-1]=true;
  var q=Q[round];
  var st=drawState[pn-1];
  btn.disabled=true;
  var ok=false;
  try{{
    var checkFn=new Function('lines','gs',q.draw.checkBody);
    ok=checkFn(st.lines, st.gridSize);
  }}catch(e){{ok=false;console.log(e);}}
  if(ok){{
    sc[pn-1]+=10;
    document.getElementById('s'+pn).textContent=sc[pn-1];
    document.getElementById('fb'+pn).innerHTML='✅ 绘图正确！+10';
    document.getElementById('st'+pn).textContent='🔥 连击！';
    sfxCorrect();
    for(var i=0;i<st.lines.length;i++)st.lines[i].correct=true;
    renderGrid(pn);
  }}else{{
    document.getElementById('fb'+pn).innerHTML='❌ 绘图不正确';
    document.getElementById('st'+pn).textContent='';
    sfxWrong();
    for(var i=0;i<st.lines.length;i++)st.lines[i].wrong=true;
    renderGrid(pn);
    // show expected answer
    if(q.draw.showAnswerBody){{
      setTimeout(function(){{
        try{{
          var showFn=new Function('st',q.draw.showAnswerBody);
          showFn(st);renderGrid(pn);
        }}catch(e){{}}
      }},600);
    }}
  }}
  if(ans[0]&&ans[1]){{clearInterval(ti);cr++;setTimeout(function(){{nextRound();}},1800);}}
}}

// ====== 选择模式 ======
function renderChoice(pn, q){{
  var qText=q.q1||q.q;
  var opts=q.o1||q.o;
  var ansIdx=q.a1!==undefined?q.a1:q.a;
  document.getElementById('content'+pn).innerHTML=
    '<div class="question-box"><div style="font-size:0.82em;color:#ccc;margin-bottom:3px">第'+(cr+1)+'题</div>'+qText+'</div>'+
    '<div id="optsArea'+pn+'"></div>';
  document.getElementById('fb'+pn).innerHTML='';
  document.getElementById('st'+pn).textContent='';
  var ix=[0,1,2,3];
  for(var i=ix.length-1;i>0;i--){{var j=Math.floor(Math.random()*(i+1));var t=ix[i];ix[i]=ix[j];ix[j]=t;}}
  var lb=['A','B','C','D'];
  var h='<div class="options-grid">';
  for(var i=0;i<4;i++){{
    var oi=ix[i];
    h+='<button class="p-opt" onclick="answerChoice('+pn+','+oi+','+ansIdx+',this)" id="ob'+pn+'_'+i+'">'+lb[i]+'. '+opts[oi]+'</button>';
  }}
  h+='</div>';
  document.getElementById('optsArea'+pn).innerHTML=h;
}}

function renderQuestion(pn, q, isDraw){{
  if(isDraw)renderDraw(pn, q.draw);
  else renderChoice(pn, q);
}}

function answerChoice(pn,oi,ai,btn){{
  if(!go||ans[pn-1])return;
  ans[pn-1]=true;
  var bs=document.querySelectorAll('#optsArea'+pn+' .p-opt');
  bs.forEach(function(b){{b.disabled=true;}});
  if(oi===ai){{
    btn.classList.add('correct');
    sc[pn-1]+=10;
    document.getElementById('s'+pn).textContent=sc[pn-1];
    document.getElementById('fb'+pn).innerHTML='✅ 正确！+10';
    document.getElementById('st'+pn).textContent='🔥 连击！';
    sfxCorrect();
  }}else{{
    btn.classList.add('wrong');
    document.getElementById('fb'+pn).innerHTML='❌ 答错了';
    document.getElementById('st'+pn).textContent='';
    sfxWrong();
    for(var i=0;i<bs.length;i++){{
      var lb=['A','B','C','D'];
      if(bs[i].textContent.indexOf(lb[ai]+'.')>=0)bs[i].classList.add('correct');
    }}
  }}
  if(ans[0]&&ans[1]){{clearInterval(ti);cr++;setTimeout(function(){{nextRound();}},1200);}}
}}

function timeUp(){{
  for(var p=1;p<=2;p++){{
    if(!ans[p-1]){{
      var sbtn=document.getElementById('subBtn'+p);if(sbtn)sbtn.disabled=true;
      var cv=document.getElementById('cv'+p);if(cv)cv.onclick=null;
      var opts=document.querySelectorAll('#optsArea'+p+' .p-opt');
      opts.forEach(function(b){{b.disabled=true;}});
      document.getElementById('fb'+p).innerHTML='⏰ 时间到！';
    }}
  }}
  cr++;setTimeout(function(){{nextRound();}},1200);
}}

function endGame(){{
  go=false;clearInterval(ti);
  document.getElementById('winOverlay').classList.add('show');
  document.getElementById('ws1').textContent=sc[0];
  document.getElementById('ws2').textContent=sc[1];
  if(sc[0]>sc[1]){{
    document.getElementById('winTitle').innerHTML='🔴 红方获胜！';
    document.getElementById('winTitle').style.color='#FF6B6B';
    document.getElementById('winSub').innerHTML=modNames[curModule]+'<br>红方 '+sc[0]+' : '+sc[1]+' 蓝方';
    sfxWin();
  }}else if(sc[1]>sc[0]){{
    document.getElementById('winTitle').innerHTML='🔵 蓝方获胜！';
    document.getElementById('winTitle').style.color='#4ECDC4';
    document.getElementById('winSub').innerHTML=modNames[curModule]+'<br>蓝方 '+sc[1]+' : '+sc[0]+' 红方';
    sfxWin();
  }}else{{
    document.getElementById('winTitle').innerHTML='🤝 平局！';
    document.getElementById('winTitle').style.color='#FFD700';
    document.getElementById('winSub').innerHTML=modNames[curModule]+'<br>双方都是 '+sc[0]+' 分';
    playTone(523,0.3,'sine',0.08);
  }}
  spawnConfetti();
  var best=parseInt(localStorage.getItem(sk)||'0');var mx=Math.max(sc[0],sc[1]);
  if(mx>best){{localStorage.setItem(sk,mx);}}
}}

function spawnConfetti(){{var colors=['#FF6B6B','#4ECDC4','#FFD700','#FF9800','#6C5CE7','#66BB6A','#EC407A','#42A5F5'];for(var i=0;i<60;i++){{var d=document.createElement('div');d.className='confetti';d.style.left=Math.random()*100+'%';d.style.top=-(Math.random()*50+10)+'px';d.style.width=(Math.random()*10+6)+'px';d.style.height=(Math.random()*10+6)+'px';d.style.background=colors[Math.floor(Math.random()*colors.length)];d.style.animationDuration=(Math.random()*2+2)+'s';d.style.animationDelay=Math.random()*1.5+'s';d.style.borderRadius=Math.random()>0.5?'50%':'0';document.body.appendChild(d);setTimeout(function(){{d.remove();}},4000);}}}}

function restartGame(){{clearInterval(ti);go=false;sc=[0,0];cr=0;ans=[false,false];
drawState=[null,null];
document.getElementById('s1').textContent='0';document.getElementById('s2').textContent='0';
document.getElementById('fb1').innerHTML='';document.getElementById('fb2').innerHTML='';
document.getElementById('st1').textContent='';document.getElementById('st2').textContent='';
document.getElementById('rn').textContent='1';document.getElementById('tm').textContent='20';
document.getElementById('winOverlay').classList.remove('show');
document.getElementById('btnStart').style.display='inline-block';
document.getElementById('moduleBar').style.display='flex';
document.getElementById('content1').innerHTML='已选：'+modNames[curModule]+'<br>点击开始对战';
document.getElementById('content2').innerHTML='已选：'+modNames[curModule]+'<br>点击开始对战';
Q=sf(Q);var cf=document.querySelectorAll('.confetti');cf.forEach(function(c){{c.remove();}});}}

function backToMenu(){{restartGame();}}
</script>
</body>
</html>'''

# ─── Helper: choice question ───
def pkq(q, opts, ans):
    return {"q":q, "o1":opts, "a1":ans, "o2":opts, "a2":ans}

# ─── Helper: draw question ───
# Canvas: 10x10 grid, spacing 28px, total ~308x308
GS=10; SP=28; W=(GS+1)*SP; H=(GS+1)*SP

def draw_q(task, given_lines, given_points, labels, check_body, hint="", show_answer_body=""):
    """Create a drawing question.
    check_body: JS function body (code between { and }) that takes (lines, gs) and returns true/false
    show_answer_body: JS function body that takes (drawState) and adds correct lines
    """
    w = W; h = H
    return {
        "draw": {
            "task": task,
            "hint": hint,
            "w": w, "h": h,
            "gridSize": GS,
            "given": [{"c1":c1,"r1":r1,"c2":c2,"r2":r2} for c1,r1,c2,r2 in given_lines],
            "points": [{"c":c,"r":r} for c,r in given_points],
            "labels": {k: {"c":c,"r":r} for k,(c,r) in labels.items()},
            "checkBody": check_body,
            "showAnswerBody": show_answer_body,
        },
        "q": "", "o1": [""], "a1": 0, "o2": [""], "a2": 0
    }

# ─── Check functions (operate on grid coords) ───

# Check if a line passes through point (pc,pr)
def on_line(x1,y1,x2,y2,px,py):
    """Check if point (px,py) is on line segment (x1,y1)-(x2,y2)"""
    d = abs((x2-x1)*(y1-py) - (x1-px)*(y2-y1))
    if d > 1e-6: return False
    if min(x1,x2)-0.1 <= px <= max(x1,x2)+0.1 and min(y1,y2)-0.1 <= py <= max(y1,y2)+0.1:
        return True
    return False

# Check perpendicular: two lines defined by (dx1,dy1) and (dx2,dy2)
# Dot product should be ~0
def is_perp(dx1,dy1,dx2,dy2):
    return abs(dx1*dx2 + dy1*dy2) < 0.01

# Check parallel: cross product should be ~0
def is_para(dx1,dy1,dx2,dy2):
    return abs(dx1*dy2 - dx2*dy1) < 0.01

# ============================================================
# MODULE 1: 判断垂线和平行线 (choice only)
# ============================================================
m1 = [
    pkq("两条直线相交成直角时，这两条直线叫做什么？",
        ["互相平行", "互相垂直", "互相交叉", "互相重合"], 1),
    pkq("在同一平面内，永远不相交的两条直线叫做什么？",
        ["垂线", "斜线", "平行线", "曲线"], 2),
    pkq("长方形的长和宽是什么关系？",
        ["平行", "垂直", "重合", "既不平行也不垂直"], 1),
    pkq("长方形的两条长边是什么关系？",
        ["垂直", "平行", "交叉", "不确定"], 1),
    pkq("两条平行线之间的垂直线段长度有什么特点？",
        ["不相等", "处处相等", "越来越大", "越来越小"], 1),
    pkq("黑板的上边沿和下边沿是什么关系？",
        ["垂直", "平行", "相交", "不确定"], 1),
    pkq("正方形相邻的两条边是什么关系？",
        ["平行", "垂直", "重合", "不确定"], 1),
    pkq("同一平面内，过直线外一点可以画几条直线与已知直线平行？",
        ["0条", "1条", "2条", "无数条"], 1),
    pkq("两条直线互相垂直时，会形成几个直角？",
        ["1个", "2个", "3个", "4个"], 3),
    pkq("正方形有几组互相垂直的边？",
        ["1组", "2组", "3组", "4组"], 3),
]

# ============================================================
# MODULE 2: 画垂线 (drawing tasks)
# ============================================================
# Task template: given a horizontal/vertical line through grid, and a point,
# student draws perpendicular line through that point

# Draw Q1: Given horizontal line at row 5, point P at (5,2). Draw perpendicular through P.
m2 = [
    draw_q(
        "过点P画已知直线L的垂线。<br>（点击P点→再点击直线上方或下方格点）",
        [(0,5,10,5)],  # given line L: horizontal at row 5
        [(5,2)],       # point P at (5,2)
        {"L":(9,4.5), "P":(5,1.5)},
        # check: drawn line goes through P(5,2) AND is vertical (perpendicular to horizontal)
        """for(var i=0;i<lines.length;i++){
            var l=lines[i];
            var dx=l.c2-l.c1, dy=l.r2-l.r1;
            var onP=(l.c1===5&&l.r1===2)||(l.c2===5&&l.r2===2);
            var vert=(dx===0 && dy!==0);
            if(onP && vert)return true;
        }
        return false;""",
        "提示：垂线应该与L成直角，即画竖直线通过P点"
    ),
    draw_q(
        "过点P画已知直线L的垂线。",
        [(3,0,3,10)],  # vertical line at col 3
        [(7,5)],       # point P at (7,5)
        {"L":(2.5,9), "P":(7,4.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var dx=l.c2-l.c1, dy=l.r2-l.r1;
                var onP=(l.c1===7&&l.r1===5)||(l.c2===7&&l.r2===5);
                var horz=(dy===0 && dx!==0);
                if(onP && horz)return true;
            }
            return false;""",
        "提示：L是竖直线，垂线应该是水平线通过P点"
    ),
    draw_q(
        "过直线L上的点P，画L的垂线。",
        [(1,5,9,5)],  # horizontal
        [(5,5)],      # P on the line
        {"L":(8.5,4.5), "P":(5,4.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var dx=l.c2-l.c1, dy=l.r2-l.r1;
                var onP=(l.c1===5&&l.r1===5)||(l.c2===5&&l.r2===5);
                var vert=(dx===0 && dy!==0);
                if(onP && vert)return true;
            }
            return false;""",
        "提示：P在L上，过P画L的垂线（竖直线）"
    ),
    draw_q(
        "过点A画直线BC的垂线。",
        [(2,7,8,3)],  # diagonal line BC
        [(6,2)],      # point A
        {"B":(1.5,7.5), "C":(8.5,3.5), "A":(6,1.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var onA=(l.c1===6&&l.r1===2)||(l.c2===6&&l.r2===2);
                if(!onA)continue;
                // given line BC: (2,7)->(8,3), dx=6,dy=-4 → slope=-2/3
                // perpendicular slope=3/2 → dx=2,dy=3 (or dx=-2,dy=-3)
                var dx=l.c2-l.c1, dy=l.r2-l.r1;
                // Check perpendicular: dot product (6)*(dx) + (-4)*(dy) ≈ 0
                if(Math.abs(6*dx + (-4)*dy) < 0.1)return true;
            }
            return false;""",
        "提示：先看BC的方向（右6下4），垂线方向应与之垂直"
    ),
    draw_q(
        "过直线外一点P，画直线L的垂线。",
        [(1,2,1,8)],  # vertical line
        [(7,3)],      # point P
        {"L":(0.5,7), "P":(7,2.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var onP=(l.c1===7&&l.r1===3)||(l.c2===7&&l.r2===3);
                var horz=(l.r2-l.r1===0 && l.c2-l.c1!==0);
                if(onP && horz)return true;
            }
            return false;""",
        "提示：L是竖直的，垂线是水平的"
    ),
    # 5 choice questions mixed in
    pkq("过直线上一点可以画几条垂线？",
        ["0条", "1条", "2条", "无数条"], 1),
    pkq("画垂线最常用的工具是什么？",
        ["直尺", "量角器", "三角板", "圆规"], 2),
    pkq("用三角板画垂线，需要用到三角板的什么角？",
        ["锐角", "直角", "钝角", "任意角"], 1),
    pkq("两条直线垂直时，它们的交点叫做什么？",
        ["交点", "垂足", "顶点", "中点"], 1),
    pkq("验证两条直线是否垂直，最简单的方法是什么？",
        ["用直尺量", "用三角板直角比", "目测", "用圆规"], 1),
]

# ============================================================
# MODULE 3: 点到直线的距离 (drawing + measurement)
# ============================================================
m3 = [
    draw_q(
        "画出点P到直线L的垂线段。<br>（这是点P到L的距离）",
        [(0,4,10,4)],  # horizontal L
        [(5,8)],       # P above L
        {"L":(9,3.5), "P":(5,7.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var onP=(l.c1===5&&l.r1===8)||(l.c2===5&&l.r2===8);
                if(!onP)continue;
                // must end on line L (row 4)
                var onL=(l.r1===4)||(l.r2===4);
                var vert=(l.c2-l.c1===0);
                if(onL && vert)return true;
            }
            return false;""",
        "提示：距离 = 垂线段长度，从P竖直向下连到L"
    ),
    draw_q(
        "画出点A到直线BC的距离（垂线段）。",
        [(1,8,9,8)],  # horizontal BC
        [(5,2)],      # A above
        {"A":(5,1.5), "B":(0.5,8.5), "C":(9.5,8.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var onA=(l.c1===5&&l.r1===2)||(l.c2===5&&l.r2===2);
                if(!onA)continue;
                var onBC=(l.r1===8)||(l.r2===8);
                var vert=(l.c2-l.c1===0);
                if(onBC && vert && l.r1!==l.r2)return true;
            }
            return false;""",
        "提示：从A竖直向下连到BC所在直线"
    ),
    draw_q(
        "画出点P到直线L的垂线段，并测量距离。<br>（每个格点间距=1cm，距离=？cm）",
        [(0,6,10,6)],  # horizontal L
        [(4,3)],       # P above L
        {"L":(9,5.5), "P":(4,2.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var onP=(l.c1===4&&l.r1===3)||(l.c2===4&&l.r2===3);
                if(!onP)continue;
                var onL=(l.r1===6)||(l.r2===6);
                var vert=(l.c2-l.c1===0);
                if(onL && vert)return true;
            }
            return false;""",
        "提示：从P竖直连到L，距离=6-3=3格=3cm"
    ),
    draw_q(
        "点P到直线L的垂线段长3cm。<br>在方格中画出这条垂线段。<br>（提示：L在row=5，P在row=2或row=8）",
        [(0,5,10,5)],  # L
        [(6,2)],       # P, 3 units above L
        {"L":(9,4.5), "P":(6,1.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var onP=(l.c1===6&&l.r1===2)||(l.c2===6&&l.r2===2);
                if(!onP)continue;
                var onL=(l.r1===5)||(l.r2===5);
                var vert=(l.c2-l.c1===0);
                var dist=Math.abs(l.r1-l.r2);
                if(onL && vert && dist===3)return true;
            }
            return false;""",
        "提示：P到L的距离=5-2=3格，垂线段长3格"
    ),
    draw_q(
        "画出点A到直线BC的垂线段。",
        [(1,3,9,3)],  # BC
        [(4,9)],      # A below
        {"A":(4,9.5), "B":(0.5,3.5), "C":(9.5,3.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var onA=(l.c1===4&&l.r1===9)||(l.c2===4&&l.r2===9);
                if(!onA)continue;
                var onBC=(l.r1===3)||(l.r2===3);
                var vert=(l.c2-l.c1===0);
                if(onBC && vert)return true;
            }
            return false;""",
        "提示：从A竖直向上连到BC"
    ),
    # 5 choice questions
    pkq("从直线外一点到直线的距离，是指什么？",
        ["任意线段的长", "垂直线段的长", "斜线段的长", "最长的线段"], 1),
    pkq("点到直线的所有连线中，哪条最短？",
        ["垂线段", "斜线段", "水平线段", "都一样"], 0),
    pkq("测量点到直线的距离，实际是测量什么？",
        ["斜线长度", "垂线段的长度", "任意线段", "曲线长度"], 1),
    pkq("直尺上相邻两个刻度之间的距离是多少？",
        ["1毫米", "1厘米", "1分米", "根据尺子而定"], 0),
    pkq("一条线段长5厘米，等于多少毫米？",
        ["5毫米", "50毫米", "500毫米", "0.5毫米"], 1),
]

# ============================================================
# MODULE 4: 平行线之间的距离 (drawing)
# ============================================================
m4 = [
    draw_q(
        "已知直线L，过点P画L的平行线。<br>（用三角板贴紧直尺平移法）",
        [(0,5,10,5)],  # L horizontal
        [(0,2)],       # P
        {"L":(9,4.5), "P":(0,1.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var onP=(l.c1===0&&l.r1===2)||(l.c2===0&&l.r2===2);
                if(!onP)continue;
                var horz=(l.r2-l.r1===0 && l.c2-l.c1!==0);
                if(horz)return true;
            }
            return false;""",
        "提示：L是水平线，平行线也是水平的，从P向右画水平线"
    ),
    draw_q(
        "画出两条平行线L1和L2之间的一条垂线段。<br>（测量平行线间距离）",
        [(0,3,10,3),(0,7,10,7)],  # two horizontal parallel lines
        [],
        {"L1":(9,2.5),"L2":(9,6.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var vert=(l.c2-l.c1===0);
                var touchesL1=(l.r1===3||l.r2===3);
                var touchesL2=(l.r1===7||l.r2===7);
                if(vert && touchesL1 && touchesL2)return true;
            }
            return false;""",
        "提示：在任意位置画竖直线连接L1和L2，长度=4格"
    ),
    draw_q(
        "已知直线L，过点P画L的平行线。",
        [(2,0,2,10)],  # L vertical
        [(7,4)],       # P
        {"L":(1.5,9), "P":(7,3.5)},
        """            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var onP=(l.c1===7&&l.r1===4)||(l.c2===7&&l.r2===4);
                if(!onP)continue;
                var vert=(l.c2-l.c1===0 && l.r2-l.r1!==0);
                if(vert)return true;
            }
            return false;""",
        "提示：L是竖直线，平行线也是竖直的"
    ),
    draw_q(
        "L1和L2是平行线。在它们之间画2条不同的垂线段。<br>比较它们的长度。",
        [(0,2,10,2),(0,8,10,8)],
        [],
        {"L1":(9,1.5),"L2":(9,7.5)},
        """            var count=0;
            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var vert=(l.c2-l.c1===0);
                var t1=(l.r1===2||l.r2===2);
                var t2=(l.r1===8||l.r2===8);
                if(vert && t1 && t2)count++;
            }
            return count>=2;""",
        "提示：画两条竖直线，每条都连接L1和L2，两条应该一样长"
    ),
    draw_q(
        "过点P画直线L的平行线，再过点Q画L的垂线。",
        [(0,5,10,5)],  # L
        [(0,2)],       # P for parallel
        {"L":(9,4.5), "P":(0,1.5), "Q":(5,8)},
        """            var gotPara=false, gotPerp=false;
            for(var i=0;i<lines.length;i++){
                var l=lines[i];
                var onP=(l.c1===0&&l.r1===2)||(l.c2===0&&l.r2===2);
                var onQ=(l.c1===5&&l.r1===8)||(l.c2===5&&l.r2===8);
                var horz=(l.r2-l.r1===0);
                var vert=(l.c2-l.c1===0);
                if(onP && horz)gotPara=true;
                if(onQ && vert)gotPerp=true;
            }
            return gotPara && gotPerp;""",
        "提示：过P画水平线（平行），过Q画竖直线（垂直）"
    ),
    # 5 choice
    pkq("两条平行线之间的垂线段长度有什么特点？",
        ["左边大右边小", "右边大左边小", "处处相等", "中间最大"], 2),
    pkq("测量平行线之间的距离，应该怎样量？",
        ["斜着量", "垂直于两条平行线量", "平行于其中一条量", "怎么量都行"], 1),
    pkq("平行线之间可以画多少条垂线段？",
        ["1条", "2条", "10条", "无数条"], 3),
    pkq("平行线间距离是3cm，任意位置画垂线段长多少？",
        ["1.5cm", "3cm", "6cm", "位置不同长度不同"], 1),
    pkq("画平行线时，最常用的方法是什么？",
        ["三角板和直尺配合", "只用三角板", "只用直尺", "徒手画"], 0),
]

# ============================================================
# MODULE 5: 长方形和正方形特征 (choice only)
# ============================================================
m5 = [
    pkq("长方形有几条边？",
        ["3条", "4条", "5条", "6条"], 1),
    pkq("长方形有几条对称轴？",
        ["1条", "2条", "3条", "4条"], 1),
    pkq("长方形对边的长度有什么特点？",
        ["一条长一条短", "对边相等", "四条边都相等", "不一定"], 1),
    pkq("长方形有几个角？每个角是多少度？",
        ["4个锐角", "4个直角", "2个直角2个锐角", "4个钝角"], 1),
    pkq("正方形四条边的长度有什么特点？",
        ["对边相等", "四条边都相等", "相邻两边相等", "不一定"], 1),
    pkq("正方形有几条对称轴？",
        ["1条", "2条", "3条", "4条"], 3),
    pkq("正方形是特殊的长方形吗？",
        ["是的", "不是", "长方形是特殊的正方形", "两者无关"], 0),
    pkq("长方形和正方形的共同特点是什么？",
        ["四条边都相等", "四个角都是直角", "都是斜的", "没有共同点"], 1),
    pkq("一个四边形四个角都是直角，四边相等，是什么图形？",
        ["长方形", "正方形", "平行四边形", "梯形"], 1),
    pkq("一个四边形四个角都是直角，对边相等邻边不等，是什么？",
        ["正方形", "长方形", "平行四边形", "菱形"], 1),
]

# ============================================================
# MODULE 6: 画长方形和正方形 (drawing)
# ============================================================
m6 = [
    draw_q(
        "画一个长6格、宽4格的长方形。<br>从点A(2,2)开始，向右画长，向上画宽。",
        [],
        [(2,2)],  # start point A
        {"A":(2,1.5)},
        """            // expect 4 lines forming 6x4 rectangle
            if(lines.length!==4)return false;
            // check: starting at (2,2), right 6 to (8,2), up 4 to (8,6), left 6 to (2,6), down 4 to (2,2)
            var exp=[[2,2,8,2],[8,2,8,6],[8,6,2,6],[2,6,2,2]];
            var found=0;
            for(var e=0;e<4;e++){{
                var ee=exp[e];
                for(var i=0;i<lines.length;i++){{
                    var l=lines[i];
                    if((l.c1===ee[0]&&l.r1===ee[1]&&l.c2===ee[2]&&l.r2===ee[3])||
                       (l.c1===ee[2]&&l.r1===ee[3]&&l.c2===ee[0]&&l.r2===ee[1])){{
                        found++;break;
                    }}
                }}
            }}
            return found===4;""",
        "提示：从A(2,2)开始→右6格到(8,2)→上4格到(8,6)→左6格到(2,6)→下4格回到A"
    ),
    draw_q(
        "画一个边长为5格的正方形。<br>从点A(3,3)开始。",
        [],
        [(3,3)],
        {"A":(3,2.5)},
        """            if(lines.length!==4)return false;
            var exp=[[3,3,8,3],[8,3,8,8],[8,8,3,8],[3,8,3,3]];
            var found=0;
            for(var e=0;e<4;e++){{
                var ee=exp[e];
                for(var i=0;i<lines.length;i++){{
                    var l=lines[i];
                    if((l.c1===ee[0]&&l.r1===ee[1]&&l.c2===ee[2]&&l.r2===ee[3])||
                       (l.c1===ee[2]&&l.r1===ee[3]&&l.c2===ee[0]&&l.r2===ee[1])){{
                        found++;break;
                    }}
                }}
            }}
            return found===4;""",
        "提示：正方形四边相等，每边5格"
    ),
    draw_q(
        "已知长方形的长AB=6格。<br>补全这个长方形（宽4格）。",
        [(2,5,8,5)],  # AB: from (2,5) to (8,5), length 6
        [(2,5),(8,5)],  # A and B
        {"A":(1.5,5.5),"B":(8.5,5.5)},
        """            if(lines.length!==3)return false;
            // need: vertical from A up/down 4, vertical from B up/down 4, horizontal top/bottom
            var exp=[[2,5,2,9],[8,5,8,9],[2,9,8,9]]; // up
            var exp2=[[2,5,2,1],[8,5,8,1],[2,1,8,1]]; // down
            function check(ex){{
                var f=0;
                for(var e=0;e<3;e++){{
                    var ee=ex[e];
                    for(var i=0;i<lines.length;i++){{
                        var l=lines[i];
                        if((l.c1===ee[0]&&l.r1===ee[1]&&l.c2===ee[2]&&l.r2===ee[3])||
                           (l.c1===ee[2]&&l.r1===ee[3]&&l.c2===ee[0]&&l.r2===ee[1])){{f++;break;}}
                    }}
                }}
                return f===3;
            }}
            return check(exp)||check(exp2);""",
        "提示：从A、B分别向上（或向下）画4格竖线，再连起来"
    ),
    draw_q(
        "画一个长7格、宽3格的长方形。",
        [],
        [(1,2)],
        {"起":(1,1.5)},
        """            if(lines.length!==4)return false;
            var exp=[[1,2,8,2],[8,2,8,5],[8,5,1,5],[1,5,1,2]];
            var found=0;
            for(var e=0;e<4;e++){{
                var ee=exp[e];
                for(var i=0;i<lines.length;i++){{
                    var l=lines[i];
                    if((l.c1===ee[0]&&l.r1===ee[1]&&l.c2===ee[2]&&l.r2===ee[3])||
                       (l.c1===ee[2]&&l.r1===ee[3]&&l.c2===ee[0]&&l.r2===ee[1])){{
                        found++;break;
                    }}
                }}
            }}
            return found===4;""",
        "提示：任意起点，按长7宽3画出4条边"
    ),
    draw_q(
        "画一个边长为4格的正方形。",
        [],
        [(2,4)],
        {"起":(2,3.5)},
        """            if(lines.length!==4)return false;
            var exp=[[2,4,6,4],[6,4,6,8],[6,8,2,8],[2,8,2,4]];
            var found=0;
            for(var e=0;e<4;e++){{
                var ee=exp[e];
                for(var i=0;i<lines.length;i++){{
                    var l=lines[i];
                    if((l.c1===ee[0]&&l.r1===ee[1]&&l.c2===ee[2]&&l.r2===ee[3])||
                       (l.c1===ee[2]&&l.r1===ee[3]&&l.c2===ee[0]&&l.r2===ee[1])){{
                        found++;break;
                    }}
                }}
            }}
            return found===4;""",
        "提示：正方形四边相等，每边4格"
    ),
    # 5 choice questions
    pkq("画长方形时，至少需要知道哪两个条件？",
        ["边长和角度", "长和宽", "周长和面积", "对角线的长"], 1),
    pkq("画正方形时，至少需要知道什么？",
        ["长和宽", "对角线的长", "边长", "周长"], 2),
    pkq("画长方形第一步先画什么？",
        ["四条边", "一条长边（或宽）", "对角线", "四个角"], 1),
    pkq("画好一条边后，下一步在两端画什么？",
        ["平行线", "垂线（宽）", "斜线", "随便"], 1),
    pkq("画长方形时用什么工具确保角是直角？",
        ["直尺", "三角板或量角器", "圆规", "目测"], 1),
]

# ============================================================
all_modules = [m1, m2, m3, m4, m5, m6]
for i, m in enumerate(all_modules):
    assert len(m) == 10, f"Module {i+1}: expected 10, got {len(m)}"

def serialize(qlist):
    result = []
    for q in qlist:
        entry = {
            "q": q.get("q",""), "q1": q.get("q1",""), "q2": q.get("q2",""),
            "o1": q.get("o1",[]), "a1": q.get("a1",0),
            "o2": q.get("o2",[]), "a2": q.get("a2",0),
        }
        if "draw" in q:
            entry["draw"] = q["draw"]
        result.append(entry)
    return result

all_json = json.dumps([serialize(m) for m in all_modules], ensure_ascii=False)
html = T.format(title="长方形和正方形", all_questions=all_json)

fp = os.path.join(BASE, "长方形和正方形-交互绘图PK.html")
with open(fp, 'w', encoding='utf-8') as f:
    f.write(html)
print("OK: %s" % fp)
print("Done!")
