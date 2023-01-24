#version 400

in vec2 textureCoord;
out vec4 color;
uniform sampler2D textureSlot;

void main(void) 
{
    color = texture(textureSlot, vec2(1.0 - textureCoord.x, textureCoord.y));
}
