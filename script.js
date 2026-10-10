const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('.main-nav');
if (menuToggle && mainNav) {
  menuToggle.addEventListener('click', () => {
    const open = mainNav.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    menuToggle.textContent = open ? '×' : '☰';
  });
  mainNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    mainNav.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.textContent = '☰';
  }));
}
document.getElementById('year').textContent = new Date().getFullYear();
const form = document.getElementById('contactForm');
if (form) form.addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(form);
  const subject = encodeURIComponent(`ValiStera enquiry: ${data.get('topic')}`);
  const body = encodeURIComponent(
    `Name: ${data.get('name')}\nBusiness email: ${data.get('email')}\nOrganisation: ${data.get('organisation') || 'Not provided'}\nArea of interest: ${data.get('topic')}\n\nRequirement:\n${data.get('message')}`
  );
  window.location.href = `mailto:contact@valistera.com?subject=${subject}&body=${body}`;
});
