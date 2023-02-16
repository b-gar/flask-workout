var slider = document.getElementById("time-input");
var output = document.getElementById("time-val");
                
output.innerHTML = slider.value;

slider.oninput = function() {
	output.innerHTML = this.value;
}