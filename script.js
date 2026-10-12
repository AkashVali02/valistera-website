document.addEventListener('DOMContentLoaded',()=>{const toggle=document.querySelector('.menu-toggle');const nav=document.querySelector('.main-nav');if(toggle&&nav){toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));toggle.textContent=open?'×':'☰';});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.textContent='☰';}));}const year=document.getElementById('year');if(year)year.textContent=new Date().getFullYear();const form=document.getElementById('contact-form');if(form){const params=new URLSearchParams(location.search);const wanted=params.get('resource')||params.get('course')||params.get('topic');if(wanted){const msg=form.querySelector('[name="message"]');if(msg)msg.value='I would like to enquire about: '+wanted.replaceAll('-',' ')+'\n\n';}form.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(form);const subject='ValiStera website enquiry - '+d.get('interest');const body='Name: '+d.get('name')+'\nEmail: '+d.get('email')+'\nArea of interest: '+d.get('interest')+'\n\nMessage:\n'+d.get('message');location.href='mailto:contact@valistera.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);});}});
/* ValiStera About Page — Count-up animation */
(function(){
  const counters=document.querySelectorAll('.count-up');
  if(!counters.length)return;
  const animateCounter=(counter)=>{
    const target=parseInt(counter.dataset.target,10)||0;
    const suffix=counter.dataset.suffix||'';
    const duration=1800;
    const startTime=performance.now();
    const step=(now)=>{
      const progress=Math.min((now-startTime)/duration,1);
      const eased=1-Math.pow(1-progress,3);
      counter.textContent=Math.floor(target*eased)+suffix;
      if(progress<1){requestAnimationFrame(step);}else{counter.textContent=target+suffix;}
    };
    requestAnimationFrame(step);
  };
  const observer=new IntersectionObserver((entries,obs)=>{
    entries.forEach((entry)=>{
      if(entry.isIntersecting){animateCounter(entry.target);obs.unobserve(entry.target);}
    });
  },{threshold:0.35});
  counters.forEach((counter)=>observer.observe(counter));
})();
