// Mobile menu
const toggle = document.querySelector(".nav-toggle");
const nav = document.getElementById("nav");
toggle?.addEventListener("click", () => {
  const open = nav.classList.toggle("is-open");
  toggle.setAttribute("aria-expanded", open);
});

// Home page slideshow
const show = document.querySelector(".slideshow");
if (show) {
  const slides = [...show.querySelectorAll(".slide")];
  let current = 0;
  let timer;
  const go = (n) => {
    slides[current].classList.remove("is-active");
    current = (n + slides.length) % slides.length;
    slides[current].classList.add("is-active");
    restart();
  };
  const restart = () => {
    clearInterval(timer);
    if (!matchMedia("(prefers-reduced-motion: reduce)").matches) timer = setInterval(() => go(current + 1), 4500);
  };
  show.querySelector(".slideshow__nav--prev").addEventListener("click", () => go(current - 1));
  show.querySelector(".slideshow__nav--next").addEventListener("click", () => go(current + 1));
  show.addEventListener("click", (e) => { if (!e.target.closest("button")) go(current + 1); });
  restart();
}

// Lightbox for gallery images
const links = [...document.querySelectorAll("[data-full]")];
if (links.length) {
  const box = document.createElement("div");
  box.className = "lightbox";
  box.hidden = true;
  box.innerHTML =
    '<img alt=""><button class="lb-close" aria-label="Close">&times;</button>' +
    '<button class="lb-prev" aria-label="Previous">&#8249;</button><button class="lb-next" aria-label="Next">&#8250;</button>';
  document.body.append(box);
  const img = box.querySelector("img");
  let index = 0;

  const showImage = (n) => {
    index = (n + links.length) % links.length;
    img.src = links[index].dataset.full;
    img.alt = links[index].querySelector("img").alt;
  };
  const open = (n) => {
    showImage(n);
    box.hidden = false;
    requestAnimationFrame(() => box.classList.add("is-open"));
    document.body.style.overflow = "hidden";
  };
  const close = () => {
    box.classList.remove("is-open");
    document.body.style.overflow = "";
    setTimeout(() => (box.hidden = true), 250);
  };

  links.forEach((a, n) => a.addEventListener("click", (e) => { e.preventDefault(); open(n); }));
  box.querySelector(".lb-close").addEventListener("click", close);
  box.querySelector(".lb-prev").addEventListener("click", () => showImage(index - 1));
  box.querySelector(".lb-next").addEventListener("click", () => showImage(index + 1));
  box.addEventListener("click", (e) => { if (e.target === box) close(); });
  document.addEventListener("keydown", (e) => {
    if (box.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") showImage(index - 1);
    if (e.key === "ArrowRight") showImage(index + 1);
  });
  // Swipe on phones
  let startX = null;
  box.addEventListener("touchstart", (e) => (startX = e.touches[0].clientX), { passive: true });
  box.addEventListener("touchend", (e) => {
    if (startX === null) return;
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) showImage(index + (dx < 0 ? 1 : -1));
    startX = null;
  });
}

// Contact form: until a form service is connected, say so instead of failing silently.
const form = document.querySelector(".contact-form");
if (form?.dataset.connected === "no") {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    form.querySelector(".form-note").textContent =
      "This form isn't connected yet. Please get in touch through Instagram for now.";
  });
}
