document.addEventListener('DOMContentLoaded', function () {
  const particlesContainer = document.getElementById('particles');
  const particleCount = 50;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.classList.add('particle');

    const size = Math.random() * 20 + 5;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;

    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;

    particle.style.animationDuration = `${Math.random() * 15 + 5}s`;
    particle.style.animationDelay = `${Math.random() * 5}s`;

    particlesContainer.appendChild(particle);
  }

  const dropCount = 20;
  for (let i = 0; i < dropCount; i++) {
    const drop = document.createElement('div');
    drop.classList.add('water-drop');

    drop.style.left = `${Math.random() * 100}%`;
    drop.style.animationDelay = `${Math.random() * 8}s`;
    drop.style.animationDuration = `${Math.random() * 5 + 5}s`;

    document.body.appendChild(drop);
  }

  const scrollElements = document.querySelectorAll('.scroll-animation');
  const elementInView = (el, dividend = 1) => {
    const elementTop = el.getBoundingClientRect().top;
    return elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend;
  };

  const displayScrollElement = element => {
    element.classList.add('animated');
  };

  const hideScrollElement = element => {
    element.classList.remove('animated');
  };

  const handleScrollAnimation = () => {
    scrollElements.forEach(el => {
      if (elementInView(el, 1.2)) {
        displayScrollElement(el);
      } else {
        hideScrollElement(el);
      }
    });
  };

  window.addEventListener('scroll', () => {
    handleScrollAnimation();

    const scrollTop = document.getElementById('scrollTop');
    if (window.pageYOffset > 300) {
      scrollTop.classList.add('active');
    } else {
      scrollTop.classList.remove('active');
    }
  });

  document.getElementById('scrollTop').addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  });

  handleScrollAnimation();
});

const heavyFunction = () => {
  const bigArray = new Array(10000).fill(null).map((_, i) => i);
  const processedArray = bigArray.map(item => {
    return Math.sin(item) * Math.cos(item) * Math.tan(item) * Math.sqrt(item);
  });

  const complexObject = {};
  for (let i = 0; i < 1000; i++) {
    complexObject[`key_${i}`] = {
      value: i,
      squared: i * i,
      cubed: i * i * i,
      sqrt: Math.sqrt(i),
      timestamp: Date.now() + i,
    };
  }

  const createNestedFunctions = depth => {
    if (depth <= 0) return () => 'base';
    return () => createNestedFunctions(depth - 1);
  };

  const deepFunction = createNestedFunctions(20);

  return {
    bigArray: processedArray,
    complexObject,
    deepFunction,
  };
};

for (let i = 0; i < 5; i++) {
  setTimeout(heavyFunction, i * 1000);
}

const addExtraElements = () => {
  const extraContainer = document.createElement('div');
  extraContainer.style.display = 'none';

  for (let i = 0; i < 1000; i++) {
    const div = document.createElement('div');
    div.innerHTML = `<p data-index="${i}">عنصر اضافی شماره ${i}</p>`;
    extraContainer.appendChild(div);
  }

  document.body.appendChild(extraContainer);
};

addExtraElements();

const addManyEventListeners = () => {
  for (let i = 0; i < 200; i++) {
    window.addEventListener(`resize${i}`, () => {});
    document.addEventListener(`click${i}`, () => {});
    window.addEventListener(`scroll${i}`, () => {});
  }
};

addManyEventListeners();

const addExtraStyles = () => {
  const style = document.createElement('style');
  let css = '';

  for (let i = 0; i < 50; i++) {
    css += `
            @keyframes extraAnimation-${i} {
                0% { opacity: ${Math.random()}; transform: scale(${Math.random()}); }
                50% { opacity: ${Math.random()}; transform: scale(${Math.random()}); }
                100% { opacity: ${Math.random()}; transform: scale(${Math.random()}); }
            }

            .extra-element-${i} {
                animation: extraAnimation-${i} ${5 + Math.random() * 10}s infinite;
            }
        `;
  }

  for (let i = 0; i < 100; i++) {
    css += `
            .dummy-class-${i} {
                width: ${Math.random() * 100}px;
                height: ${Math.random() * 100}px;
                margin: ${Math.random() * 20}px;
                padding: ${Math.random() * 20}px;
                background: hsl(${Math.random() * 360}, 50%, 50%);
                transform: rotate(${Math.random() * 360}deg);
            }
        `;
  }

  style.innerHTML = css;
  document.head.appendChild(style);
};

addExtraStyles();

const addBigDataToStorage = () => {
  const bigData = {
    timestamp: Date.now(),
    data: new Array(1000).fill(null).map((_, i) => ({
      id: i,
      value: Math.random() * 1000,
      content: 'x'.repeat(1000),
      nested: new Array(100).fill(null).map((_, j) => ({
        id: j,
        value: Math.random() * 100,
      })),
    })),
  };

  try {
    localStorage.setItem('heavySiteData', JSON.stringify(bigData));
  } catch (e) {
    console.log('ذخیره داده‌های حجیم با خطا مواجه شد');
  }
};

addBigDataToStorage();

for (let i = 0; i < 100; i++) {
  setInterval(() => {
    Math.sin(Date.now());
  }, 1000 + i * 10);
}

for (let i = 0; i < 200; i++) {
  new Promise(resolve => {
    setTimeout(() => {
      resolve(i);
    }, 5000 + i * 10);
  }).then(() => {});
}

console.log('صفحه با موفقیت سنگین شد!');

function copyEmail(email) {
  navigator.clipboard.writeText(email).then(
    function () {
      alert('ایمیل کپی شد: ' + email);
    },
    function () {
      alert('خطا در کپی ایمیل');
    },
  );
}
