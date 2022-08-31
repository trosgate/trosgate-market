
const imageBox = document.getElementById('image-box');
const thumbinput = document.getElementById('id_thumbnail');

let image = document.getElementById('image');
thumbinput.addEventListener('change', ()=>{
  const image_data = thumbinput.files[0]
  const url = URL.createObjectURL(image_data)
  imageBox.innerHTML = `<img id="image" src="${url}" width:"60px"'>`
})






























