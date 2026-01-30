// search.js 

/**
 * یک رشته را برای جستجوی دقیق نرمال‌سازی می‌کند.
 * - فاصله‌ها را حذف می‌کند.
 * - اعداد فارسی را به انگلیسی تبدیل می‌کند.
 * - به حروف کوچک تبدیل می‌کند.
 * @param {string} str - رشته ورودی.
 * @returns {string} رشته نرمال‌شده.
 */
function normalizeString(str) {
  if (!str) return "";
  return str
    .toString()
    .toLowerCase()
    .replace(/\s+/g, '')
    .replace(/[۱-۹]/g, d => "۱۲۳۴۵۶۷۸۹".indexOf(d))
    .replace(/[۰]/g, '0');
}

/**
 * سیستم جستجو را با داده‌های مشخص شده راه‌اندازی می‌کند.
 * @param {object} aliasesData - آبجکتی شامل نام‌های مستعار برای هر عنصر.
 */
function initSearch(aliasesData) {
  const searchInput = document.getElementById("searchInput");
  const clearBtn = document.getElementById("clearSearch");

  if (!searchInput || !clearBtn) {
    console.error("Error: HTML elements for search (searchInput or clearSearch) not found.");
    return;
  }

  const allCells = Array.from(document.querySelectorAll(".element-cell"));
  if (allCells.length === 0) {
    console.error("Error: No element cell found to search on the page.");
    return;
  }

  searchInput.addEventListener("input", (event) => {
    const query = event.target.value;
    performSmartSearch(query, aliasesData, allCells);
  });

  clearBtn.addEventListener("click", (event) => {
    event.preventDefault();
    searchInput.value = "";
    resetSearch(allCells);
  });

  console.log("✅ The search system was successfully launched.");
}

/**
 * جستجوی هوشمند را بر اساس ورودی کاربر انجام می‌دهد.
 * @param {string} query - عبارت جستجو شده.
 * @param {object} aliasesData - داده‌های نام‌های مستعار.
 * @param {HTMLElement[]} cells - آرایه‌ای از تمام سلول‌های عناصر.
 */
function performSmartSearch(query, aliasesData, cells) {
  // ۱. عبارت جستجو را نرمال‌سازی کن
  const normalizedQuery = normalizeString(query);

  // اگر ورودی خالی است، جدول را به حالت اولیه برگردان
  if (!normalizedQuery) {
    resetSearch(cells);
    return;
  }

  cells.forEach(cell => {
    const symbol = cell.dataset.symbol;
    if (!symbol) return;

    const aliases = aliasesData[symbol] || [];

    const isMatch = aliases.some(alias => {
      const normalizedAlias = normalizeString(alias);
      return normalizedAlias.startsWith(normalizedQuery);
    });

    if (isMatch) {
      cell.classList.remove("search-no-match");
    } else {
      cell.classList.add("search-no-match");
    }
  });
}

/**
 * تمام فیلترهای جستجو را پاک کرده و جدول را به حالت اولیه برمی‌گرداند.
 * @param {HTMLElement[]} cells - آرایه‌ای از تمام سلول‌های عناصر.
 */
function resetSearch(cells) {
  cells.forEach(cell => {
    cell.classList.remove("search-no-match");
  });
}