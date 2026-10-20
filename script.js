document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    const setMenuOpen = (open) => {
      nav.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      toggle.textContent = open ? '×' : '☰';
    };
    const isInsideNavigation = (target) => nav.contains(target) || toggle.contains(target);
    toggle.addEventListener('click', () => setMenuOpen(!nav.classList.contains('open')));
    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setMenuOpen(false));
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && nav.classList.contains('open')) {
        event.preventDefault();
        setMenuOpen(false);
        toggle.focus();
      }
    });
    document.addEventListener('pointerdown', (event) => {
      if (!isInsideNavigation(event.target)) setMenuOpen(false);
    });
    document.addEventListener('focusin', (event) => {
      if (!isInsideNavigation(event.target)) setMenuOpen(false);
    });
    const mobile = window.matchMedia('(max-width: 820px)');
    mobile.addEventListener('change', () => {
      const focusWasInNav = nav.contains(document.activeElement);
      setMenuOpen(false);
      if (mobile.matches && focusWasInNav) toggle.focus();
    });
  }
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
});
/* ValiStera performance counters — respect reduced-motion preferences. */
(function(){
  const counters=document.querySelectorAll('.count-up');
  if(!counters.length)return;
  const motionPreference=typeof window.matchMedia==='function'
    ? window.matchMedia('(prefers-reduced-motion: reduce)')
    : null;
  const showFinalValue=(counter)=>{
    counter.textContent=(parseInt(counter.dataset.target,10)||0)+(counter.dataset.suffix||'');
  };
  if(!motionPreference || motionPreference.matches || !('IntersectionObserver' in window)){
    counters.forEach(showFinalValue);
    return;
  }
  const animateCounter=(counter)=>{
    const target=parseInt(counter.dataset.target,10)||0;
    const suffix=counter.dataset.suffix||'';
    const duration=1800;
    const startTime=performance.now();
    const step=(now)=>{
      if(motionPreference.matches){showFinalValue(counter);return;}
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
  motionPreference.addEventListener?.('change',(event)=>{
    if(event.matches){
      observer.disconnect();
      counters.forEach(showFinalValue);
    }
  });
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
  let submitting = false;

  function prefillEnquiry() {
    if (enquiryContext.service && !serviceField.value) serviceField.value = enquiryContext.service;
    if (enquiryContext.message && !messageField.value && serviceField.value === "Training / ValiStera Academy") {
      messageField.value = enquiryContext.message;
    }
  }

  function setStatus(message, state, focus = false) {
    status.textContent = message;
    status.className = "form-status" + (state ? " form-status-" + state : "");
    if (focus) status.focus();
  }

  function resetVerification() {
    // A third-party widget error must not turn a confirmed submission into a failure.
    try { window.turnstile?.reset(); } catch (_) {}
  }

  prefillEnquiry();
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (submitting) return;
    setStatus("", "");

    for (const name of ["name", "organization", "email", "phone", "country", "message"]) {
      const field = form.elements.namedItem(name);
      if (field) field.value = field.value.trim();
    }
    if (!form.reportValidity()) {
      setStatus("Please complete all required fields.", "error");
      return;
    }

    const turnstileToken = form.querySelector('[name="cf-turnstile-response"]')?.value || "";
    if (!turnstileToken) {
      setStatus("Please complete the security verification. If it does not appear, use the email link below.", "error", true);
      return;
    }
    const endpoint = form.dataset.endpoint;
    if (!endpoint) {
      setStatus("The enquiry service is temporarily unavailable. Please email contact@valistera.com.", "error", true);
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

    submitting = true;
    submitButton.disabled = true;
    submitButton.textContent = "Submitting…";
    form.setAttribute("aria-busy", "true");
    setStatus("Submitting your enquiry…", "");
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 30000);

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
      let result = {};
      try { result = await response.json(); } catch (_) {}
      if (!response.ok) {
        throw new Error(typeof result?.error === "string" ? result.error : "We could not submit your enquiry. Please email contact@valistera.com if the problem continues.");
      }
      if (!result?.ok) {
        throw new Error(typeof result?.error === "string" && result.error ? result.error : "We could not confirm the server response. Please email contact@valistera.com before sending again.");
      }

      // Only a confirmed successful submission with current consent records a lead.
      try {
        if (window.valisteraHasAnalyticsConsent?.() && typeof window.gtag === "function") {
          window.gtag("event", "generate_lead", { lead_source: "website_consultancy_enquiry" });
        }
      } catch (_) {}

      form.reset();
      prefillEnquiry();
      resetVerification();
      setStatus(typeof result.message === "string" && result.message ? result.message : "Thank you. Your enquiry has been submitted successfully.", "success", true);
    } catch (error) {
      const message = error.name === "AbortError"
        ? "The request timed out and delivery could not be confirmed. Your details are still here. Please email contact@valistera.com before sending again."
        : error instanceof TypeError
          ? "The connection was interrupted and delivery could not be confirmed. Your details are still here. Please email contact@valistera.com before sending again."
          : error.message || "We could not submit your enquiry. Please email contact@valistera.com.";
      setStatus(message, "error", true);
      resetVerification();
    } finally {
      window.clearTimeout(timeout);
      submitting = false;
      form.setAttribute("aria-busy", "false");
      submitButton.disabled = false;
      submitButton.textContent = "Submit enquiry";
    }
  });
  // Keep the HTML button disabled until its secure submit handler is attached.
  submitButton.disabled = false;
});
