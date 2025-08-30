const images = ['./img/lab.jpg', './img/member.jpg', './img/baseball.jpg', './img/semiroom.jpg', './img/bbq.jpg']
let current = 0

function changeImage() {
    const imgElement = document.getElementById('slideshow-image')
    current = (current + 1) % images.length
    imgElement.src = images[current]
}

setInterval(changeImage, 3000) // xxxxmsごとに画像を切り替える