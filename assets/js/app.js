// app.js 
document.addEventListener("DOMContentLoaded", async () => {
  try {
    console.log("🚀 شروع لود برنامه در حالت استاتیک...");

    const [elementsResponse, aliasesResponse] = await Promise.all([
      fetch("assets/data/elements.json"), 
      fetch("assets/data/aliases.json")
    ]);

    if (!elementsResponse.ok || !aliasesResponse.ok) {
        throw new Error(`Error reading local JSON files`);
    }

    const elementsData = await elementsResponse.json();
    const aliasesData = await aliasesResponse.json();

    window.elementsData = elementsData;
    window.aliasesData = aliasesData;

    console.log("✅ Element and search data successfully loaded from local files");

    buildPeriodicTable(elementsData);
    console.log("✅ The periodic table was created.");

    initSearch(aliasesData);
    console.log("✅ Search system activated.");

  } catch (err) {
    console.error("❌ Error loading data or creating table:", err);
    document.body.innerHTML = '<h1 style="color: red; text-align: center; margin-top: 50px;">خطا در بارگذاری اطلاعات. لطفاً صفحه را رفرش کنید.</h1>';
  }
});