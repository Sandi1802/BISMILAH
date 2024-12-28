
const carousel = document.getElementById("carouselImages");
const prevSlide = document.getElementById("prevSlide");
const nextSlide = document.getElementById("nextSlide");

let currentIndex = 0;
const totalSlides = carousel.children.length;
const displayDuration = 2000; // Waktu tampilan per gambar (5 detik)
let slideTimeout;

// Fungsi untuk memperbarui posisi carousel
function updateCarousel() {
  const offset = -currentIndex * 100;
  carousel.style.transform = `translateX(${offset}%)`;
}

// Fungsi untuk berpindah ke slide berikutnya
function goToNextSlide() {
  currentIndex = (currentIndex + 1) % totalSlides;
  updateCarousel();
  restartAutoSlide(); // Restart auto-slide setiap berpindah slide
}

// Fungsi untuk berpindah ke slide sebelumnya
function goToPrevSlide() {
  currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
  updateCarousel();
  restartAutoSlide(); // Restart auto-slide setiap berpindah slide
}

// Fungsi untuk memulai perpindahan otomatis
function startAutoSlide() {
  slideTimeout = setTimeout(() => {
    goToNextSlide();
  }, displayDuration);
}

// Fungsi untuk menghentikan perpindahan otomatis
function stopAutoSlide() {
  clearTimeout(slideTimeout);
}

// Fungsi untuk restart perpindahan otomatis
function restartAutoSlide() {
  stopAutoSlide();
  startAutoSlide();
}

// Event listener tombol panah
prevSlide.addEventListener("click", goToPrevSlide);
nextSlide.addEventListener("click", goToNextSlide);

// Mulai perpindahan otomatis saat halaman dimuat
startAutoSlide();

