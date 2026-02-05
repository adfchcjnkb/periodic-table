document.addEventListener('DOMContentLoaded', function () {
  // Particles 
  const particlesContainer = document.getElementById('particles');
  if (particlesContainer) {
    for (let i = 0; i < 20; i++) {
      const particle = document.createElement('div');
      particle.classList.add('particle');
      const size = Math.random() * 10 + 3;
      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.left = `${Math.random() * 100}%`;
      particle.style.top = `${Math.random() * 100}%`;
      particle.style.animationDuration = `${Math.random() * 8 + 3}s`;
      particlesContainer.appendChild(particle);
    }
  }

  // Water drops 
  for (let i = 0; i < 8; i++) {
    const drop = document.createElement('div');
    drop.classList.add('water-drop');
    drop.style.left = `${Math.random() * 100}%`;
    drop.style.animationDelay = `${Math.random() * 3}s`;
    document.body.appendChild(drop);
  }

  // Scroll animations
  const scrollElements = document.querySelectorAll('.scroll-animation');
  
  const checkScroll = () => {
    scrollElements.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.8) {
        el.classList.add('animated');
      }
    });

    const scrollTop = document.getElementById('scrollTop');
    if (window.pageYOffset > 300) {
      scrollTop?.classList.add('active');
    } else {
      scrollTop?.classList.remove('active');
    }
  };

  window.addEventListener('scroll', checkScroll);
  checkScroll();

  // Scroll to top
  document.getElementById('scrollTop')?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});

// Email copy function
function copyEmail(email) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(email)
      .then(() => alert('ایمیل کپی شد: ' + email))
      .catch(() => alert('خطا در کپی ایمیل'));
  } else {
    const textArea = document.createElement('textarea');
    textArea.value = email;
    document.body.appendChild(textArea);
    textArea.select();
    try {
      document.execCommand('copy');
      alert('ایمیل کپی شد: ' + email);
    } catch (err) {
      alert('خطا در کپی ایمیل');
    }
    document.body.removeChild(textArea);
  }
}


setTimeout(() => {
  const data = { items: [] };
  for (let i = 0; i < 500; i++) {
    data.items.push({
      id: i,
      value: Math.random(),
      timestamp: Date.now()
    });
  }
  try {
    localStorage.setItem('siteData', JSON.stringify(data));
  } catch (e) {
    console.log('Storage full');
  }
}, 2000);


setInterval(() => {
  Math.sin(Date.now());
}, 5000);

console.log('صفحه آماده است');
