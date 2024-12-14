const sleep = ms => new Promise(r => setTimeout(r, ms));

let Images = ['Image-Display/image1.png', 'Image-Display/image2.png', 'Image-Display/image3.png', 'Image-Display/image4.png'];
let imageIndex = 0;
function moveImage(proportional_index) {
    imageIndex += proportional_index;
    imageIndex %= Images.length;
    if (imageIndex < 0) {
        while (imageIndex < 0) {
            imageIndex += Images.length
        }
    }
    let img = document.getElementById('displayed-image');
    img.src = Images[imageIndex];
}

async function autoSlide() {
    while (true) {
        await sleep(10 * 1000);
        moveImage(1);
    }
}

addEventListener("DOMContentLoaded", () => {
    autoSlide();
});