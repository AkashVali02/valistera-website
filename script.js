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


/* =========================================================
   VALISTERA — SECURE CONSULTANCY ENQUIRY FORM
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("consultancy-enquiry-form");

  if (!form) return;

  const status = document.getElementById("form-status");
  const submitButton = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    status.textContent = "";
    status.className = "form-status";

    if (!form.reportValidity()) {
      status.textContent = "Please complete all required fields.";
      status.classList.add("form-status-error");
      return;
    }

    const turnstileToken =
      form.querySelector('[name="cf-turnstile-response"]')?.value || "";

    if (!turnstileToken) {
      status.textContent = "Please complete the security verification.";
      status.classList.add("form-status-error");
      return;
    }

    const endpoint = form.dataset.endpoint;

    if (!endpoint) {
      status.textContent =
        "The enquiry service is temporarily unavailable. Please email contact@valistera.com.";
      status.classList.add("form-status-error");
      return;
    }

    const data = new FormData(form);

    const payload = {
      name: data.get("name"),
      organization: data.get("organization"),
      email: data.get("email"),
      phone: data.get("phone"),
      country: data.get("country"),
      service: data.get("service"),
      projectStage: data.get("project_stage"),
      preferredContact: data.get("preferred_contact"),
      message: data.get("message"),
      privacyConsent: data.get("privacy_consent") === "on",
      website: data.get("website"),
      turnstileToken,
    };

    submitButton.disabled = true;
    submitButton.textContent = "Submitting…";

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      let result = {};

      try {
        result = await response.json();
      } catch {
        result = {};
      }

      if (!response.ok || !result.ok) {
        throw new Error(
          result.error ||
          "We could not submit your enquiry. Please try again."
        );
      }

      form.reset();

      if (window.turnstile) {
        window.turnstile.reset();
      }

      status.textContent =
        result.message ||
        "Thank you. Your enquiry has been submitted successfully.";

      status.classList.add("form-status-success");

    } catch (error) {
      status.textContent =
        error.message ||
        "We could not submit your enquiry. Please email contact@valistera.com.";

      status.classList.add("form-status-error");

      if (window.turnstile) {
        window.turnstile.reset();
      }

    } finally {
      submitButton.disabled = false;
      submitButton.textContent = "Submit enquiry";
    }
  });
});
