document.body.style.zoom = "90%"

let canvas = document.getElementById("wordcloud")
let generate = document.getElementById("generate");
let download = document.getElementById("download");

download.addEventListener('click', downloadImg);
generate.addEventListener('click', generateCloud);

let input_text = document.getElementById('words-input');
//let length = document.getElementById("length");
//let width = document.getElementById("width");
let cloud_mask = "usa";
let color_map = "plasma"
let img_url = "";

document.getElementById("shapes").querySelectorAll('li').forEach( function(el) {
  el.addEventListener('click', function() {
    document.getElementById("cloud-shape").innerText = el.textContent;
    cloud_mask = el.textContent;
    console.log(cloud_mask)
  });
});

document.getElementById("colors").querySelectorAll('li').forEach( function(el) {
  el.addEventListener('click', function() {
    document.getElementById("color-map").innerText = el.textContent;
    color_map = el.textContent;
    console.log(color_map)
  });
});


function generateCloud() {
  console.log("generate request sent")
  var pre_text = input_text.value
  var processed = pre_text.replace(/[.,\/#!$%\^&\*;:{}=\-_`~\'()]/g,"")
  generate_request = {
    text: processed,
    mask: cloud_mask,
    cmap: color_map
  }

  $.post( "/generate",
   JSON.stringify(generate_request))
  .done(function(result) {
    img_url = result
    canvas.innerHTML = img_url
  })
  .fail(function() {
    alert( "error" );
  })
}

function downloadImg() {
  var link = document.createElement('a');
  var img = document.images[0];
  link.download = `word_cloud.png`;
  link.href = img.src.replace(/^data:image\/[^;]+/, 'data:application/octet-stream');
  link.click();
}

VANTA.CLOUDS({
  el: "body",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight:1500.00,
  backgroundColor: 0xe8c7c7,
  skyColor: 0x90afc2,
  cloudColor: 0xd7dde8
})


