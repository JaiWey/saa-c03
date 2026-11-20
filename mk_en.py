import re
s=open('template.html',encoding='utf-8').read()
def R(old,new,count=1):
    global s
    assert s.count(old)>=1,('missing',old[:70])
    if count==1: assert s.count(old)==1,('multi',old[:70],s.count(old))
    s=s.replace(old,new)

R('<html lang="zh-CN">','<html lang="en">')
R('<title>AWS SAA-C03 刷题</title>','<title>AWS SAA-C03 Practice</title>')
R('"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}','Roboto,"Helvetica Neue",Arial,sans-serif}')
R('.mismatch{','.expl{margin-top:14px;padding:14px 16px;border-radius:12px;background:var(--card);border:1px solid var(--line)}\n.expl b{display:block;margin-bottom:4px;font-size:14px;letter-spacing:.3px;text-transform:uppercase;color:var(--accent)}\n.expl p{margin:0;line-height:1.65}\n.ref{margin-top:10px;font-size:13px;color:var(--muted)}\n.mismatch{')
R('<i></i>SAA-C03 刷题</div>','<i></i>SAA-C03 Practice</div>')
R('id="btnSettings">设置</button>','id="btnSettings">Settings</button>')
R('<b id="drTitle">题目导航</b><span class="spacer"></span><button class="btn ghost" id="drClose">关闭</button>','<b id="drTitle">Navigator</b><span class="spacer"></span><button class="btn ghost" id="drClose">Close</button>')
R("const KEY = 'saa-c03-practice-v1';","const KEY = 'saa-c03-practice-en-v1';")
R("S.set=Object.assign({src:'official',autoSubmit:true,autoNext:false},S.set||{});\nfunction save","S.set=Object.assign({autoSubmit:true,autoNext:false,ref:true},S.set||{});\nfunction save") if "S.set=Object.assign({src:'official',autoSubmit:true,autoNext:false},S.set||{});\nfunction save" in s else None
s=s.replace("S.set=Object.assign({src:'official',autoSubmit:true,autoNext:false},S.set||{});","S.set=Object.assign({autoSubmit:true,autoNext:false,ref:true},S.set||{});")
R("const effAns=q=> (S.set.src==='community' && q.cv) ? q.cv : q.a;","const effAns=q=>q.a;")
R("const isMulti=q=>q.a.length>1 || (q.cv&&q.cv.length>1);\nconst mismatch=q=>!!q.cv && q.cv!==q.a;","const mismatch=q=>!!q.pa && q.pa!==q.a;")
R("toast('这个列表是空的')","toast('This list is empty')")
R("'答对'),","'Correct'),")
R("'答错'),","'Wrong'),")
R("'已作答'):null,","'Answered'):null,")
R("'未做')));","'Not done')));")
R("placeholder:'跳到第几题（1-'+Q.list.length+'）'","placeholder:'Jump to question (1-'+Q.list.length+')'")
R("'跳转')));","'Go')));")
R("title:'题号 #'+n","title:'Question #'+n")
R("openDrawer(Q.exam?'答题卡':'题目导航',box);","openDrawer(Q.exam?'Answer sheet':'Navigator',box);")

# settings block
a=s.index("$('#btnSettings').onclick=()=>{")
b=s.index("$('#brand').onclick=")
new_settings='''$('#btnSettings').onclick=()=>{
  const box=h('div',{class:'set'});
  box.append(h('label',{},h('input',{type:'checkbox',checked:S.set.autoSubmit,onchange:e=>{S.set.autoSubmit=e.target.checked;save();}}),h('div',{},'Grade single-choice questions on click',h('small',{},'When off, press "Submit answer" to grade.'))));
  box.append(h('label',{},h('input',{type:'checkbox',checked:S.set.autoNext,onchange:e=>{S.set.autoNext=e.target.checked;save();}}),h('div',{},'Auto-advance after a correct answer',h('small',{},'Wrong answers stay on screen so you can read the explanation.'))));
  box.append(h('label',{},h('input',{type:'checkbox',checked:S.set.ref,onchange:e=>{S.set.ref=e.target.checked;save();if(V.view==='quiz')render();}}),h('div',{},'Show source PDF key and community vote',h('small',{},'Reference only. Grading always uses this app\\'s own answers.'))));
  box.append(h('hr',{style:'border:none;border-top:1px solid var(--line);width:100%'}));
  const applyImport=o=>{if(!o.prog)throw 0;S=o;S.prog=S.prog||{};S.fav=S.fav||[];S.set=Object.assign({autoSubmit:true,autoNext:false,ref:true},S.set||{});save();toast('Imported');closeDrawer();render();};
  box.append(h('div',{},h('button',{class:'btn',onclick:()=>{
    const ta=h('textarea',{readonly:true,style:'width:100%;height:120px;margin-top:10px;font:12px monospace;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:8px'});
    ta.value=JSON.stringify(S); box.append(ta); ta.select();
    try{navigator.clipboard.writeText(ta.value).then(()=>toast('Copied to clipboard'),()=>toast('Copy the text box manually'));}catch(e){toast('Copy the text box manually');}
  }},'Export progress'),' ',h('button',{class:'btn',onclick:()=>{
    const f=h('input',{type:'file',accept:'application/json'});
    f.onchange=()=>{const r=new FileReader();r.onload=()=>{try{applyImport(JSON.parse(r.result));}catch(e){toast('Invalid file');}};r.readAsText(f.files[0]);};
    f.click();
  }},'Import progress (file)'),' ',h('button',{class:'btn',style:'color:var(--bad)',onclick:()=>{
    if(confirm('Clear all practice history, favorites and progress? This cannot be undone.')){S={prog:{},fav:[],pos:0,set:S.set};save();closeDrawer();V={view:'home'};Q=null;render();}
  }},'Reset progress')));
  box.append(h('div',{class:'sub'},'Progress is stored in this browser only. Before switching devices or clearing browser data, use "Export progress" (copy the text and save it), then restore it later with "Import progress" by choosing the .json file.'));
  openDrawer('Settings',box);
};
'''
s=s[:a]+new_settings+s[b:]
R("confirm('退出将放弃本次模拟考试，确定吗？')","confirm('Leaving will abandon this mock exam. Continue?')")

# home
a=s.index("  app.append(h('h1',{},'AWS SAA-C03 刷题')")
b=s.index("function startExam(){")
home='''  app.append(h('h1',{},'AWS SAA-C03 Practice'),h('div',{class:'sub'},`${total} questions · answers and explanations written independently`));
  app.append(h('div',{class:'stats'},
    stat(done,'Attempted',`/ ${total}`),stat(right,'Last try correct'),stat(wrong,'Review list'),stat(att?acc+'%':'–','Overall accuracy')));
  app.append(h('div',{class:'bar',title:'Progress'},
    h('i',{style:`width:${right/total*100}%;background:var(--ok)`}),
    h('i',{style:`width:${wrong/total*100}%;background:var(--bad)`})));
  const pos=Math.min(S.pos||0,total-1);
  const modes=[
    ['Continue in order',`Resume at question ${pos+1} (#${BANK[pos].n})`,null,()=>startSession('seq',BANK.map(q=>q.n),{i:pos})],
    ['Random practice','Shuffle the whole bank',null,()=>startSession('rand',shuffle(BANK.map(q=>q.n)))],
    ['Random · unseen only','Cover questions you have not tried',unseenList().length,()=>startSession('unseen',shuffle(unseenList()))],
    ['Review list','Questions you last got wrong; removed once answered correctly',wrong,()=>startSession('wrong',shuffle(wrongList()))],
    ['Favorites','Questions you starred',S.fav.length,()=>startSession('fav',S.fav.slice().sort((a,b)=>a-b))],
    ['Mock exam','65 random questions · 130 minutes · graded at the end',null,()=>startExam()],
  ];
  const grid=h('div',{class:'modes'});
  for(const [t,d,n,fn] of modes){
    grid.append(h('button',{class:'card mode',onclick:fn},h('div',{class:'row'},h('b',{},t),n!=null?h('span',{class:'n'},n):null),h('small',{},d)));
  }
  app.append(h('h2',{},'Start practicing'),grid);

  app.append(h('h2',{},'Find by number or keyword'));
  const inp=h('input',{type:'search',placeholder:'Enter a number (e.g. 305) or keyword (e.g. Transfer Acceleration)'});
  const res=h('div',{class:'results'});
  const doSearch=()=>{
    res.replaceChildren(); const v=inp.value.trim(); if(!v)return;
    let hits=[];
    if(/^#?\\d+$/.test(v)){ const q=BY.get(+v.replace('#','')); if(q)hits=[q]; }
    else { const kw=v.toLowerCase().split(/\\s+/); hits=BANK.filter(q=>{const t=(q.q+' '+q.o.join(' ')).toLowerCase();return kw.every(k=>t.includes(k));}); }
    if(!hits.length){res.append(h('div',{class:'sub'},'No matching questions'));return;}
    res.append(h('div',{class:'sub'},`${hits.length} found${hits.length>40?', showing the first 40':''}`));
    const ids=hits.map(q=>q.n);
    hits.slice(0,40).forEach(q=>res.append(h('button',{class:'card res',onclick:()=>startSession('search',ids,{i:ids.indexOf(q.n)})},h('span',{class:'no'},'#'+q.n),h('span',{class:'t'},q.q))));
  };
  inp.addEventListener('input',doSearch);
  app.append(h('div',{class:'search'},inp),res);

  const mm=BANK.filter(mismatch).length;
  app.append(h('div',{class:'note'},`Note: every answer and explanation here was worked out independently, without using the source PDF's "Correct Answer" or the community votes. ${mm} questions differ from the PDF's listed answer; they are flagged after you answer. A few questions are ambiguous or have outdated wording, so check the AWS documentation when in doubt.`));
  function stat(v,l,s){return h('div',{class:'card stat'},h('b',{},String(v)),h('span',{},l+(s?' '+s:'')));}
}

'''
s=s[:a]+home+s[b:]
R("toast('时间到，已自动交卷')","toast('Time is up. Exam submitted.')")
R("labelMap={seq:'顺序练习',rand:'随机练习',unseen:'未做题',wrong:'错题本',fav:'收藏夹',search:'搜索结果',exam:'模拟考试'}","labelMap={seq:'In order',rand:'Random',unseen:'Unseen',wrong:'Review list',fav:'Favorites',search:'Search results',exam:'Mock exam'}")
R("'题号 #'+n),","'Question #'+n),")
R("`多选 · 选 ${ans.length} 项`):h('span',{class:'chip'},'单选'),","`Multiple choice · pick ${ans.length}`):h('span',{class:'chip'},'Single choice'),")
R("(!Q.exam&&mismatch(q))?h('span',{class:'chip warn',title:'题库答案与社区投票不一致'},'⚠ 答案有争议'):null,","(reveal&&mismatch(q))?h('span',{class:'chip warn',title:'Differs from the source PDF key'},'⚠ Differs from PDF key'):null,")
R("title:'收藏 (S)'","title:'Favorite (S)'")
R("alt:'题目附图'","alt:'Question exhibit'")
R("alt:'选项 '+L","alt:'Option '+L")
R("'提交答案'));","'Submit answer'));")
R("`已选 ${sel.size} / ${need}`","`Selected ${sel.size} / ${need}`")
R("'直接看答案'));","'Show answer'));")

a=s.index("    const ok=sub.ok;\n    const v=h('div'")
b=s.index("    box.append(v);\n  }\n  app.append(box);")
verdict='''    const ok=sub.ok;
    const v=h('div',{class:'verdict '+(ok?'ok':'bad')},
      h('b',{class:'t'},ok?'✓ Correct':(sub.peek?'Answer revealed':'✗ Incorrect')),
      h('div',{class:'ans'},
        h('span',{},h('em',{},'Correct answer'),h('span',{class:'kv'},ans.split('').join(' '))),
        h('span',{},h('em',{},'Your answer'),h('span',{class:'kv'},sub.sel.length?[...sub.sel].sort().join(' '):'—'))));
    v.append(h('div',{class:'expl'},h('b',{},'Explanation'),h('p',{},q.e||'')));
    if(S.set.ref&&(q.pa||q.v)) v.append(h('div',{class:'ref'},'Reference: '+(q.pa?'source PDF key '+q.pa.split('').join(' '):'')+(q.pa&&q.v?' · ':'')+(q.v?'community vote '+q.v:'')));
    if(mismatch(q)) v.append(h('div',{class:'mismatch'},`ⓘ The source PDF lists ${q.pa.split('').join('')}, but the answer here is ${q.a.split('').join('')}. See the explanation and confirm against the AWS documentation if unsure.`));
'''
s=s[:a]+verdict+s[b:]
R("'← 上一题'","'← Previous'")
R("Q.exam?'答题卡':'题目导航'},","Q.exam?'Answer sheet':'Navigator'},") if "Q.exam?'答题卡':'题目导航'}," in s else None
s=s.replace("Q.exam?'答题卡':'题目导航'","Q.exam?'Answer sheet':'Navigator'")
s=s.replace("'下一题 →'","'Next →'")
R("`还有 ${un} 题未作答，确定交卷吗？`:'确定交卷吗？'","`${un} question(s) unanswered. Submit the exam?`:'Submit the exam?'")
R("'交卷')]","'Submit exam')]")
R("toast('已取消收藏')","toast('Removed from favorites')")
R("toast('已收藏')","toast('Added to favorites')")
R("'模拟考试结果'","'Mock exam results'")
R("`答对 ${r.right} / ${r.total} 题 · 用时 ${fmtTime(r.used)}`","`${r.right} / ${r.total} correct · time used ${fmtTime(r.used)}`")
R("(pass?'达到':'未达到')+' 约 72% 的参考及格线（真实考试为 100–1000 分制、720 分及格，且含不计分题，仅供参考）'","(pass?'Above':'Below')+' the ~72% reference pass mark (the real exam is scored 100–1000 with 720 to pass and includes unscored questions, so treat this as a rough guide).'")
R("`复习错题（${wrong.length}）`","`Review wrong answers (${wrong.length})`")
R("'再考一次'","'Retake'")
R("'返回首页'","'Back home'")
R("'答题情况（点击进入复习）'","'Results (click to review)'")
R("title:'#'+d.n","title:'#'+d.n")
open('template_en.html','w',encoding='utf-8').write(s)
left=sorted(set(re.findall(r'[一-鿿]+',s)))
print('remaining CJK:',left)
