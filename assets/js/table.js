function buildPeriodicTable(elementsData) {
  console.log("🏗️ Building the periodic table...");
  
  const mainTable = document.getElementById("periodicTable");
  const seriesContainer = document.getElementById("seriesContainer");

  if (!mainTable || !seriesContainer) {
    console.error("❌ Table elements not found!");
    return;
  }

  mainTable.innerHTML = '';
  seriesContainer.innerHTML = '';

  // ایجاد ردیف‌های لانتانید و آکتینید
  const lanthanidesRow = document.createElement("div");
  lanthanidesRow.className = "element-row";
  const actinidesRow = document.createElement("div");
  actinidesRow.className = "element-row";

  const elementsArray = Object.values(elementsData);
  elementsArray.sort((a, b) => a.atomicNumber - b.atomicNumber);

  console.log(`📊 تعداد عناصر: ${elementsArray.length}`);

  elementsArray.forEach((element) => {
    const cell = createCell(element);
    
    // لانتانیدها (۵۷ تا ۷۱)
    if (element.atomicNumber >= 57 && element.atomicNumber <= 71) {
      lanthanidesRow.appendChild(cell);
    } 
    // آکتینیدها (۸۹ تا ۱۰۳)  
    else if (element.atomicNumber >= 89 && element.atomicNumber <= 103) {
      actinidesRow.appendChild(cell);
    } 
    // عناصر اصلی
    else {
      if (element.group && element.period) {
        cell.style.gridColumn = element.group;
        cell.style.gridRow = element.period;
        mainTable.appendChild(cell);
      }
    }
  });

  if (lanthanidesRow.children.length > 0) {
    seriesContainer.appendChild(lanthanidesRow);
  }
  if (actinidesRow.children.length > 0) {
    seriesContainer.appendChild(actinidesRow);
  }

  console.log("✅ The periodic table was created");
}

function createCell(element) {
  const cell = document.createElement("div");
  cell.className = `element-cell ${element.category?.replace(/\s+/g, "-") || 'unknown'}`;
  cell.dataset.symbol = element.symbol;
  cell.dataset.atomicNumber = element.atomicNumber;
  
  cell.innerHTML = `
    <div class="atomic-number">${element.atomicNumber}</div>
    <div class="symbol">${element.symbol}</div>
    <div class="fa-name">${element.faName}</div>
  `;
  
  cell.addEventListener("click", () => {
    console.log(`🎯 کلیک روی عنصر: ${element.faName}`);
    
    if (typeof window.openDetailPanel === 'function') {
      window.openDetailPanel(element);
    } else {
      console.error('❌ Function openDetailPanel not found!');
    }
  });
  
  return cell;
}

console.log("🔧 table.js loaded");