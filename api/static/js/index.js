let current_form;
let base_form_data;
let game_form_data = '';
let selected_game = 'base';

let fetching = false;

const result = document.getElementById('result');

window.addEventListener('DOMContentLoaded',()=>{
	current_form = document.getElementById('baseForm');

	const btns = document.querySelectorAll('button')
	btns.forEach(btn => {
		btn.addEventListener('click', event => {
			clicked(event.target)
		})
	})
});

function clicked(btn) {
	switch (btn.id) {
		case 'generate':
		case 'generate_'.concat(selected_game):
			generate();
			break;
		case 'download':
		case 'download_'.concat(selected_game):
			download();
			break;
		case 'next':
			get_game_form();
			break;
		case 'cancel_'.concat(selected_game):
			cancel();
			break;
		default:
			break;
	}
}

function generate(){
	if(current_form == null || fetching){
		return;
	}
	fetching = true;
	if(selected_game == 'base'){
		base_form_data = get_form_as_url_params(current_form);
	}
	else{
		game_form_data = get_form_as_url_params(current_form);
	}

	const url = '/api/'.concat(selected_game,'?',base_form_data,'&',game_form_data);
	fetchGIF(url);
}

function get_game_form() {
	if(base_form_data == null || selected_game != 'base'){
		return;
	}
	current_form.hidden = true;
	selected_game = get_selected_game(current_form);
	current_form = document.getElementById(selected_game);
	current_form.hidden = false;
}

function fetchGIF(url){
	const progress_bar = document.getElementById('progress');
	progress_bar.style.width = '5%';

	let req = new XMLHttpRequest();
	req.onreadystatechange = () => {
		if(req.readyState == 4){
			if(req.status == 200){
				result.onload = () => {fetching = false;}
				result.src = req.responseURL;
			}
			else{
				fetching = false;
				alert('There was a problem generating the GIF. Reload the page and try lowering the width and height.');
			}
		}
	}
	req.onprogress = (e) => {
		if(e.lengthComputable){
			progress_bar.style.width =	(e.loaded / e.total * 100).toString()+'%'
		}
	}
	req.open('GET',url);
	req.send();
}

function get_form_as_url_params(form) {
	const formData = new FormData(form);

	const keysToDelete = [];

	formData.forEach((val, key) => {
		if (key.endsWith('color')) {
			formData.set(key, rgb2bgr(formData.get(key).slice(1)));
		}
		else if(key == 'game'){
			keysToDelete.push(key);
		}
		else if (val.trim().length === 0) {
			keysToDelete.push(key);
		}
	});

	keysToDelete.forEach(key => formData.delete(key));

	return new URLSearchParams(formData).toString();
}

function get_selected_game(form) {
	const formData = new FormData(form);
	return formData.get('game');
}

function cancel(){
	current_form.hidden = true;
	selected_game = 'base';
	current_form = document.getElementById('baseForm');
	document.getElementById('generate').onclick = generate;
	current_form.hidden = false;
}

function download() {
	if(result.src == null){
		return;
	}
	const a = document.createElement('a');
	a.href = result.src;
	a.download = result.src;
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
}

function rgb2bgr(rgb){
	const r = rgb.slice(0,2);
	const g = rgb.slice(2,4);
	const b = rgb.slice(4,6);
	return b + g + r;
}