const bar = document.getElementById("bar")
const close = document.getElementById("close")
const nav = document.getElementById("navbar")

// check if nav bar is already opened or not
// check if nav bar is opened already

if(bar) {
  bar.addEventListener('click', () => {
    nav.classList.add('active')
  })
} 

if(close) {
  close.addEventListener('click', () => {
    nav.classList.remove('active')
  })
}

// video controls
// function toggle() {
//   var trailer = document.querySelector(".trailer");
//   var video = document.querySelector("video");
//   trailer.classList.toggle("active");
//   video.pause();
//   video.currentTime = 0;
// }