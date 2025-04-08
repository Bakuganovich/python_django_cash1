let index = 0;

function showSlide(i) {
    const slides = document.querySelectorAll('.slide');
    if (i >= slides.length) index = 0;
    if (i < 0) index = slides.length - 1;
    document.querySelector('.slides').style.transform = `translateX(${-index * 100}%)`;
}

document.querySelector('.next').addEventListener('click', () => {
    index++;
    showSlide(index);
});

document.querySelector('.prev').addEventListener('click', () => {
    index--;
    showSlide(index);
});

// Автоматическая прокрутка каждые 10 секунд
setInterval(() => {
    index++;
    showSlide(index);
}, 6000);


document.getElementById('hamburger').addEventListener('click', function() {
  document.getElementById('navigation').classList.toggle('active');
});
