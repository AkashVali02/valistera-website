/* ValiStera Solutions — GA4 privacy consent */
(() => {
  'use strict';

  const MEASUREMENT_ID = 'G-0EQ98P2EPW';
  const CONSENT_KEY = 'valistera_analytics_consent';

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
    if (analyticsLoaded) return;

    analyticsLoaded = true;

    gtag('consent', 'update', {
      analytics_storage: 'granted',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });

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

      #vs-consent-reject {
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

  function showSettingsButton() {
    const existingButton = document.getElementById('vs-cookie-settings');

    if (existingButton) {
      existingButton.style.display = '';
      return;
    }

    const button = document.createElement('button');
    button.id = 'vs-cookie-settings';
    button.type = 'button';
    button.textContent = 'Cookie settings';
    button.setAttribute('aria-label', 'Change analytics cookie settings');

    button.addEventListener('click', () => {
      showConsentBanner();
    });

    document.body.appendChild(button);
  }

  function showConsentBanner() {
    addStyles();
    removeBanner();

    const settingsButton = document.getElementById('vs-cookie-settings');
    if (settingsButton) settingsButton.style.display = 'none';

    const banner = document.createElement('section');
    banner.id = 'vs-consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Analytics cookie preferences');

    banner.innerHTML = `
      <strong>Your privacy choices</strong>
      <p>
        We use optional Google Analytics to understand how visitors use
        ValiStera.com and improve our services. Analytics is not loaded unless
        you accept it. Advertising storage and ad personalization remain
        disabled.
        <a href="/privacy.html">Privacy Policy</a>
      </p>
      <div class="vs-consent-actions">
        <button id="vs-consent-reject" type="button">
          Reject non-essential
        </button>
        <button id="vs-consent-accept" type="button">
          Accept analytics
        </button>
      </div>
    `;

    document.body.appendChild(banner);

    banner.querySelector('#vs-consent-accept').addEventListener('click', () => {
      saveConsent('accepted');
      removeBanner();
      loadAnalytics();
      showSettingsButton();
    });

    banner.querySelector('#vs-consent-reject').addEventListener('click', () => {
      const wasLoaded = analyticsLoaded;

      saveConsent('rejected');
      denyAnalytics();
      deleteAnalyticsCookies();
      removeBanner();

      if (wasLoaded) {
        location.reload();
        return;
      }

      showSettingsButton();
    });
  }

  function initialise() {
    addStyles();

    const consent = getConsent();

    if (consent === 'accepted') {
      loadAnalytics();
      showSettingsButton();
      return;
    }

    if (consent === 'rejected') {
      denyAnalytics();
      showSettingsButton();
      return;
    }

    showConsentBanner();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialise);
  } else {
    initialise();
  }
})();
