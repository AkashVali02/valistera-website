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
      video.src = source;
      video.preload = 'metadata';
      video.load();
      load.hidden = true;
      mediaStatus.textContent = 'Loading video. Use the player controls to start playback.';
      video.focus();
    });
    video.addEventListener('loadedmetadata', () => {
      mediaStatus.textContent = 'Video loaded. Captions are available in English; playback speed can be changed in the player controls.';
    });
    video.addEventListener('error', () => {
      mediaStatus.textContent = 'The video could not be loaded. You can read the transcript and companion material below, or retry loading.';
      load.hidden = false;
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
