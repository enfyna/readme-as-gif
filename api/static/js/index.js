let current_form;
let base_form_data;
let game_form_data;

window.addEventListener('DOMContentLoaded',()=>{
	document.getElementById('generate').onclick = generateBase;
	document.getElementById('next').onclick = get_game_form;

	current_form = document.getElementById('baseForm');
});


function generateBase() {
	if(current_form == null){
		return;
	}
	base_form_data = new FormData(current_form);

	const keysToDelete = [];

	base_form_data.forEach((val, key) => {
		if (key.endsWith('color')) {
			base_form_data.set(key, rgb2bgr(base_form_data.get(key).slice(1)));
		} else if (val.trim().length === 0) {
			keysToDelete.push(key);
		}
	});

	keysToDelete.forEach(key => base_form_data.delete(key));

	const url = '/api/base?' + new URLSearchParams(base_form_data).toString();
	const gifImage = document.getElementById('gifImage');
	gifImage.src = url;
}

function get_game_form() {
	if(base_form_data == null){
		return;
	}
	current_form.hidden = true;
	current_form = document.getElementById(base_form_data.get('game'));
	document.getElementById('generate_'+base_form_data.get('game')).onclick = generateGame;
	current_form.hidden = false;
}

function generateGame(){
	game_form_data = new FormData(current_form);

	const keysToDelete = [];

	game_form_data.forEach((val, key)=>{
		if(key.endsWith('color')){
			game_form_data.set(key, rgb2bgr(game_form_data.get(key).slice(1)));
		}
		else if (val.trim().length === 0) {
			keysToDelete.push(key);
		}
	});

	keysToDelete.forEach(key => base_form_data.delete(key));

	const url = '/api/' + base_form_data.get('game') + '?' + new URLSearchParams(game_form_data).toString() + '&' +new URLSearchParams(base_form_data).toString();
	const gifImage = document.getElementById('gifImage');
	gifImage.src = url;
}

function rgb2bgr(rgb){
	const r = rgb.slice(0,2)
	const g = rgb.slice(2,4)
	const b = rgb.slice(4,6)
	return b + g + r
}
