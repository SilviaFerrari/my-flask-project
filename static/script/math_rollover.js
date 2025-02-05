window.onload = function() {
    let f = document.getElementById('calculator');
    f.op1.value = Math.floor(Math.random()*11);
    f.op2.value = Math.floor(Math.random()*11);
}

function compute_string(f) {
    let r = f.op1.value + f.op2.value;
    if ( r === f.sum.value ) {
        f.string_out.value = "corretto!";
    }
    else {
        f.string_out.value = "sbagliato! Fa " + r + " :) !!";
    }
}

function compute_int(f) {
    let r = parseInt(f.op1.value) + parseInt(f.op2.value);
    if ( r === parseInt(f.sum.value) ) {
        f.int_out.value = "corretto!";
    }
    else {
        f.int_out.value = "sbagliato! Fa " + r + " :) !!";
    }
}

function rollImageById(img_id, img_file) {
   let image = document.getElementById(img_id);
   image.src = img_file;
}

function rollImageByName( img_name, img_file) {
    alert(img_name);
    CANCELLAMIdocument[img_name].src = img_file;
}