/* Progressive enhancement: reading and transcript remain available without JS. */
(() => {
  'use strict';
  const load = document.getElementById('load-media');
  const video = document.getElementById('video');
  const mediaStatus = document.getElementById('media-status');
  if (load && video) {
    load.addEventListener('click', () => {
      const source = video.dataset.src;
      if (!source) return;
      load.hidden = true;
      video.hidden = false;
      video.src = source;
      video.preload = 'metadata';
      video.load();
      mediaStatus.textContent = 'Starting lesson…';
      video.focus();
      // Request playback in the user's click/keyboard activation, including on mobile.
      video.play().catch(() => {
        if (!video.error) mediaStatus.textContent = 'Use the player’s play button to continue.';
      });
    });
    video.addEventListener('playing', () => {
      mediaStatus.textContent = '';
      const resume = document.getElementById('resumeLesson');
      if (resume) resume.hidden = true;
    });
    video.addEventListener('error', () => {
      mediaStatus.textContent = 'Video unavailable. Try again, or read the transcript below.';
      load.querySelector('.academy-play-label').textContent = 'Retry lesson';
      load.setAttribute('aria-label', 'Retry lesson video');
      load.hidden = false;
      video.hidden = true;
      if (document.activeElement === video) load.focus();
    });
  }

  const clear = document.getElementById('clear-academy-progress');
  clear?.addEventListener('click', () => {
    const status = document.getElementById('storage-status');
    try {
      // Restrict removal to this module; preserve unrelated site/application data.
      Object.keys(localStorage).filter(k => /^valistera_gmp_(1(?:[1-9]|10)_(?:position|watched|quiz)|module1_assessment_(?:draft|result))$/.test(k)).forEach(k => localStorage.removeItem(k));
      status.textContent = 'Saved Module 1 progress cleared. Reload this page to refresh displayed progress; further learning activity can save new progress.';
    } catch (_) {
      status.textContent = 'Browser storage is unavailable. Learning remains available; you can also manage site data in your browser settings.';
    }
  });
})();
