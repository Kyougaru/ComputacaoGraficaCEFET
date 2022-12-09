function setup() {
	createCanvas(600,600);
}  

function combina(A,B,t) {
	return {x:(1-t)*A.x+t*B.x,y:(1-t)*A.y+t*B.y};
}

function draw() {
	let p0, p1, p2, p3;
	background(200);
	p0 = {x:width/4 - 80,y:height/2};
	p1 = {x:2*width/4 - 80,y:height/4};
	p2 = {x:3*width/4 - 80,y:3*height/4};
	p3 = {x:4*width/4 - 80,y:height/2};
	noFill();
	beginShape();
	for(let t=0; t<=1; t+=0.01)
	{
		r1 = combina(p0,p1,t);
		r2 = combina(p1,p2,t);
		c1 = combina(r1,r2,t);

		r3 = combina(p1,p2,t);
		r4 = combina(p2,p3,t);
		c2 = combina(r3,r4,t);

		c3 = combina(c1,c2,t);

		vertex(c3.x,c3.y);
	}
	endShape();
}
