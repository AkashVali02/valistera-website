/* ValiStera Solutions — GA4 privacy consent */
(() => {
  'use strict';

  const MEASUREMENT_ID = 'G-0EQ98P2EPW';
  const CONSENT_KEY = 'valistera_analytics_consent';
  let currentConsent = getConsent();
  window['ga-disable-' + MEASUREMENT_ID] = true;
  window.valisteraHasAnalyticsConsent = () => currentConsent === 'accepted';

  window.dataLayer = window.dataLayer || [];

  function gtag() {
    window.dataLayer.push(arguments);
  }

  window.gtag = window.gtag || gtag;

  /* Consent Mode defaults — no analytics or advertising storage */
  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });

  let analyticsLoaded = false;

  function loadAnalytics() {
    window['ga-disable-' + MEASUREMENT_ID] = false;
    gtag('consent', 'update', {
      analytics_storage: 'granted',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });

    if (analyticsLoaded) return;
    analyticsLoaded = true;

    gtag('js', new Date());
    gtag('config', MEASUREMENT_ID);

    const script = document.createElement('script');
    script.async = true;
    script.src =
      'https://www.googletagmanager.com/gtag/js?id=' +
      encodeURIComponent(MEASUREMENT_ID);

    document.head.appendChild(script);
  }

  function denyAnalytics() {
    window['ga-disable-' + MEASUREMENT_ID] = true;
    gtag('consent', 'update', {
      analytics_storage: 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
  }

  function deleteAnalyticsCookies() {
    document.cookie.split(';').forEach(cookie => {
      const name = cookie.split('=')[0].trim();

      if (name === '_ga' || name.startsWith('_ga_')) {
        document.cookie =
          name + '=; Max-Age=0; path=/; SameSite=Lax';
        document.cookie =
          name + '=; Max-Age=0; path=/; domain=.valistera.com; SameSite=Lax';
        document.cookie =
          name + '=; Max-Age=0; path=/; domain=valistera.com; SameSite=Lax';
      }
    });
  }

  function getConsent() {
    try {
      return localStorage.getItem(CONSENT_KEY);
    } catch (_) {
      return null;
    }
  }

  function saveConsent(value) {
    currentConsent = value;
    try {
      localStorage.setItem(CONSENT_KEY, value);
    } catch (_) {}
  }

  function addStyles() {
    if (document.getElementById('vs-consent-style')) return;

    const style = document.createElement('style');
    style.id = 'vs-consent-style';

    style.textContent = `
      #vs-consent-banner {
        position: fixed;
        left: 50%;
        bottom: 18px;
        transform: translateX(-50%);
        width: min(920px, calc(100% - 28px));
        box-sizing: border-box;
        padding: 18px 20px;
        background: #111827;
        color: #f8fafc;
        border: 1px solid rgba(255,255,255,.14);
        border-radius: 14px;
        box-shadow: 0 18px 50px rgba(0,0,0,.32);
        z-index: 99999;
        font: inherit;
        max-height: calc(100vh - 32px);
        max-height: calc(100dvh - 32px);
        overflow-y: auto;
        overscroll-behavior: contain;
      }

      #vs-consent-banner strong {
        display: block;
        margin-bottom: 6px;
        font-size: 1rem;
      }

      #vs-consent-banner p {
        margin: 0;
        line-height: 1.55;
        font-size: .92rem;
        color: #dbe3ee;
      }

      #vs-consent-banner a {
        color: #8ec5ff;
      }

      .vs-consent-actions {
        display: flex;
        gap: 10px;
        margin-top: 14px;
        flex-wrap: wrap;
      }

      .vs-consent-actions button,
      #vs-cookie-settings {
        font: inherit;
        cursor: pointer;
      }

      .vs-consent-actions button {
        border-radius: 9px;
        padding: 10px 15px;
        font-weight: 600;
      }

      #vs-consent-accept {
        border: 1px solid #60a5fa;
        background: #2563eb;
        color: #fff;
      }

      #vs-consent-reject,
      #vs-consent-close {
        border: 1px solid #64748b;
        background: transparent;
        color: #f8fafc;
      }

      #vs-cookie-settings {
        position: fixed;
        left: 14px;
        bottom: 14px;
        z-index: 99998;
        padding: 7px 10px;
        border-radius: 8px;
        border: 1px solid rgba(100,116,139,.55);
        background: rgba(17,24,39,.94);
        color: #e5e7eb;
        font-size: .78rem;
      }

      #vs-consent-accept:focus-visible,
      #vs-consent-reject:focus-visible,
      #vs-consent-close:focus-visible,
      #vs-cookie-settings:focus-visible {
        outline: 3px solid #93c5fd;
        outline-offset: 2px;
      }

      @media (max-width: 600px) {
        #vs-consent-banner {
          padding: 16px;
          bottom: 12px;
        }

        .vs-consent-actions {
          flex-direction: column-reverse;
        }

        .vs-consent-actions button {
          width: 100%;
        }
      }
    `;

    document.head.appendChild(style);
  }

  function removeBanner() {
    document.getElementById('vs-consent-banner')?.remove();
  }

  function showSettingsButton(focus = false) {
    const existingButton = document.getElementById('vs-cookie-settings');

    if (existingButton) {
      existingButton.style.display = '';
      if (focus) existingButton.focus();
      return;
    }

    const button = document.createElement('button');
    button.id = 'vs-cookie-settings';
    button.type = 'button';
    button.textContent = 'Cookie settings';
    button.setAttribute('aria-label', 'Change analytics cookie settings');

    button.addEventListener('click', () => {
      showConsentBanner(true);
    });

    document.body.appendChild(button);
    if (focus) button.focus();
  }

  function showConsentBanner(fromSettings = false) {
    addStyles();
    removeBanner();

    const settingsButton = document.getElementById('vs-cookie-settings');
    if (settingsButton) settingsButton.style.display = 'none';

    const banner = document.createElement('section');
    banner.id = 'vs-consent-banner';
    banner.setAttribute('role', 'region');
    banner.setAttribute('aria-labelledby', 'vs-consent-title');

    banner.innerHTML = `
      <strong id="vs-consent-title">Your privacy choices</strong>
      <p>
        We use optional Google Analytics to understand how visitors use
        ValiStera.com and improve our services. Analytics is not loaded unless
        you accept it. Advertising storage and ad personalization remain
        disabled.
        <a href="/privacy">Privacy Policy</a>
      </p>
      <div class="vs-consent-actions">
        <button id="vs-consent-reject" type="button">
          Reject non-essential
        </button>
        <button id="vs-consent-accept" type="button">
          Accept analytics
        </button>
        ${fromSettings ? '<button id="vs-consent-close" type="button">Keep current choice</button>' : ''}
      </div>
    `;

    document.body.appendChild(banner);

    banner.querySelector('#vs-consent-accept').addEventListener('click', () => {
      saveConsent('accepted');
      removeBanner();
      loadAnalytics();
      showSettingsButton(true);
    });

    banner.querySelector('#vs-consent-reject').addEventListener('click', () => {
      saveConsent('rejected');
      denyAnalytics();
      deleteAnalyticsCookies();
      removeBanner();

      showSettingsButton(true);
    });

    if (fromSettings) {
      const close = () => { removeBanner(); showSettingsButton(true); };
      banner.querySelector('#vs-consent-close').addEventListener('click', close);
      banner.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') { event.preventDefault(); close(); }
      });
      banner.querySelector('#vs-consent-reject').focus();
    }
  }

  function initialise() {
    addStyles();

    const consent = currentConsent;

    if (consent === 'accepted') {
      loadAnalytics();
      showSettingsButton();
      return;
    }

    if (consent === 'rejected') {
      denyAnalytics();
      deleteAnalyticsCookies();
      showSettingsButton();
      return;
    }

    showConsentBanner();
  }

  // Respect preference changes from another open tab without discarding form data.
  window.addEventListener('storage', (event) => {
    if (event.key !== CONSENT_KEY && event.key !== null) return;
    currentConsent = getConsent();
    if (currentConsent !== 'accepted') { denyAnalytics(); deleteAnalyticsCookies(); }
    removeBanner();
    initialise();
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialise);
  } else {
    initialise();
  }
})();
