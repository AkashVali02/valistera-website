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

function getValiSteraEnquiryContext(search) {
  const services = new Map([
    ["qualification-validation", "Qualification & Validation"],
    ["gmp-compliance", "GMP Compliance"],
    ["inspection-readiness", "Inspection Readiness"],
    ["regulatory-services", "Regulatory Services / CMC"],
    ["sterile-manufacturing", "Sterile Manufacturing"],
    ["digital-quality", "Digital Quality & CSV"],
    ["training", "Training / ValiStera Academy"],
  ]);
  const courses = new Map([
    ["qualification-validation-fundamentals", "Qualification & Validation Fundamentals"],
    ["sterile-manufacturing-annex-1", "Sterile Manufacturing & Annex 1"],
    ["gmp-documentation-data-integrity", "GMP Documentation & Data Integrity"],
    ["csv-gxp-digital-systems", "CSV & GxP Digital Systems"],
  ]);
  const params = new URLSearchParams(search);
  const course = courses.get(params.get("course"));

  return {
    service: course
      ? services.get("training")
      : services.get(params.get("service")) || "",
    message: course
      ? "I would like to register my interest in " + course + ".\n\n"
      : "",
  };
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("consultancy-enquiry-form");

  if (!form) return;

  const status = document.getElementById("form-status");
  const submitButton = form.querySelector('button[type="submit"]');
  const serviceField = form.querySelector('[name="service"]');
  const messageField = form.querySelector('[name="message"]');
  const enquiryContext = getValiSteraEnquiryContext(window.location.search);

  function prefillEnquiry() {
    if (enquiryContext.service && !serviceField.value) {
      serviceField.value = enquiryContext.service;
    }
    if (
      enquiryContext.message &&
      !messageField.value &&
      serviceField.value === "Training / ValiStera Academy"
    ) {
      messageField.value = enquiryContext.message;
    }
  }

  prefillEnquiry();

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
    /* GA4 lead event — only after confirmed submission and analytics consent */
    try {
      if (
        localStorage.getItem("valistera_analytics_consent") === "accepted" &&
        typeof window.gtag === "function"
      ) {
        window.gtag("event", "generate_lead", {
          lead_source: "website_consultancy_enquiry"
        });
      }
    } catch (_) {}


      form.reset();
      prefillEnquiry();

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
