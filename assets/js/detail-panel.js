// detail-panel.js
function renderProperAtomicModel(element) {
  const container = document.getElementById("atomicModel");
  if (!container) return;
  
  container.innerHTML = "";

  const nucleus = document.createElement("div");
  nucleus.className = "nucleus";
  nucleus.textContent = element.symbol;
  container.appendChild(nucleus);

  const electronsPerShell = element.electronsPerShell || [];
  
  electronsPerShell.forEach((electronCount, shellIndex) => {
    if (electronCount === 0) return;
    
    const shell = document.createElement("div");
    shell.className = "shell";
    
    const shellSize = 50 + shellIndex * 45;
    shell.style.width = `${shellSize}px`;
    shell.style.height = `${shellSize}px`;
    
    const duration = 20 + shellIndex * 8;
    shell.style.animationDuration = `${duration}s`;

    for (let i = 0; i < electronCount; i++) {
      const electronOrbit = document.createElement("div");
      electronOrbit.className = "electron-orbit";
      
      const angle = (360 / electronCount) * i;
      electronOrbit.style.transform = `rotate(${angle}deg)`;
      
      const electron = document.createElement("div");
      electron.className = "electron";
      
      electronOrbit.appendChild(electron);
      shell.appendChild(electronOrbit);
    }
    
    container.appendChild(shell);
  });
}

window.openDetailPanel = function(element) {
  const detailPanel = document.getElementById("detailPanel");
  if (!detailPanel) return;

  const detailContent = detailPanel.querySelector(".detail-content");
  if (!detailContent) return;

  const isMobile = window.innerWidth <= 768;
  
  // پر کردن محتوای پنل
  detailContent.innerHTML = `
    <button id="closeDetail" title="بستن">✖</button>
    <h2>${element.faName} (${element.symbol})</h2>
    <div class="element-info">
      <p><strong>عدد اتمی:</strong> ${element.atomicNumber}</p>
      <p><strong>جرم اتمی:</strong> ${element.atomicMass}</p>
      <p><strong>پروتون‌ها:</strong> ${element.protons}</p>
      <p><strong>نوترون‌ها:</strong> ${element.neutrons}</p>
      <p><strong>الکترون‌ها:</strong> ${element.electrons}</p>
      <p><strong>کشف‌کننده:</strong> ${element.discovered}</p>
      <p><strong>دسته:</strong> ${element.category}</p>
      <p><strong>فاز:</strong> ${element.phase}</p>
      <p><strong>کاربردها:</strong></p>
      <ul>${element.uses.map(use => `<li>${use}</li>`).join("")}</ul>
    </div>
    ${!isMobile ? `
      <div id="atomicModel" class="atomic-model"></div>
    ` : ''}
  `;
  
  // فقط در دسکتاپ مدل اتمی رو بساز
  if (!isMobile) {
    renderProperAtomicModel(element);
  }
  
  detailPanel.classList.remove("hidden");
}

function closeDetailPanel() {
  const detailPanel = document.getElementById("detailPanel");
  if (!detailPanel) return;
  detailPanel.classList.add("hidden");
}

document.addEventListener('DOMContentLoaded', function() {
  const detailPanel = document.getElementById("detailPanel");
  
  if (!detailPanel) return;

  detailPanel.addEventListener("click", (event) => {
    if (event.target.closest("#closeDetail")) {
      closeDetailPanel();
    }
  });
  
  detailPanel.addEventListener("click", (event) => {
    if (event.target === detailPanel) {
      closeDetailPanel();
    }
  });
  
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !detailPanel.classList.contains('hidden')) {
      closeDetailPanel();
    }
  });
});