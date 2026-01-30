// responsive.js 
document.addEventListener('DOMContentLoaded', function() {
  // فقط برای موارد خاص استفاده شود
  console.log('صفحه آماده است');
});
document.addEventListener('DOMContentLoaded', function() {
  const logoImage = document.querySelector('.logo-image');
  
  if (logoImage) {
    logoImage.addEventListener('load', function() {
      this.classList.add('loaded');
    });
    
    if (logoImage.complete) {
      logoImage.classList.add('loaded');
    }
  }
});