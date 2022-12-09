#version 130

in float intensity;

void main(void) 
{   
    gl_FragColor = max(intensity,0.2) * vec4(1.0,0.0,0.0,1.0);
}