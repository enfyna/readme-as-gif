
function generateGif() {
	const form = document.getElementById('baseForm');
	const formData = new FormData(form);

	formData.set('bg_color', rgb2bgr(formData.get('bg_color').slice(1)))
	formData.set('font_color', rgb2bgr(formData.get('font_color').slice(1)))

	const string_params = ['name','country','job','project','learning','askme','funfact','icon1','icon2','icon3']

	for (const i in string_params) {
		var value = (formData.get(string_params[i]) ?? '').trim();
		if(value.length == 0){
			formData.delete(string_params[i])
		}
		else{
			formData.set(string_params[i], value)
		}
	}

	const url = '/api/base?' + new URLSearchParams(formData).toString();
	const gifImage = document.getElementById('gifImage');
	gifImage.src = url;
}

function rgb2bgr(rgb){
	const r = rgb.slice(0,2)
	const g = rgb.slice(2,4)
	const b = rgb.slice(4,6)
	return b + g + r
}
