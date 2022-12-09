#version 130

in vec3 position;
in vec2 textureCoord;
in vec3 normal;
uniform mat4 MVP;
out float intensity;

void main(void) 
{   
    vec3 lightDir = normalize(vec3(10.0,0.0,0.0));
    intensity = dot(lightDir,normalize(normal));
    gl_Position = MVP * vec4(position,1.0);
}