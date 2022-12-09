function setup() {
	createCanvas(600,600);
}

function estrela(x, y, raio1, raio2) {
	let angulo, meioAngulo;
	angulo = TWO_PI/5; //Uma estrela
	meioAngulo = angulo/2;

	beginShape();
	for (let i = 0; i<= TWO_PI; i+=angulo){
		let nx = x + raio1 * cos(i);
		let ny = y + raio1 * sin(i);
		vertex(nx, ny);

		nx = x + raio2 * cos(i+meioAngulo);
		ny = y + raio2 * sin(i+meioAngulo);
		vertex(nx,ny);
	}
	endShape();
}

function draw() {
	let angulo, meioAngulo;
	background(200);

	estrela(width/2, height/2, 20, 80);
}
