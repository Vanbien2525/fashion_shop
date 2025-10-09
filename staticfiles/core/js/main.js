document.addEventListener("DOMContentLoaded", () => {
  const images = document.querySelectorAll(".image-item");

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, { threshold: 0.3 });

  images.forEach(img => observer.observe(img));
});
