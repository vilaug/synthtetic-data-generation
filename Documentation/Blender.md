# General Instructions
I will explain some common steps/actions/process over here so that I can simply refer to the contents in this document and assume you know what I'm talking about.

## General
- The terms Model and Object have been used interchangably, they refer to eg: Can, PizzaBox etc. 
- I'm using a keyboard with `Ctrl` instead of keyboards with `Cmd`, please adjust accordingly.
- I highly recommend using a mouse, the trackpad of a laptop can be used, but it would significantly simplify things with a mouse. 
- Material refers to Aluminium, Cardboard, etc respectively
- `LMB` refers to Left Mouse Button
- `RMB` refer to Right Mouse Button
- To use x-ray view, press `Ctrl` + `Z`
- To go closer or futher away from an object use the wheel of your mouse
- To move left, right, top or bottom, press `shift` and use `LMB`

## Blender
- We will mostly work in `Shading` and sometimes `Layout` and `UV Editing`. You can change between modes using the horizontal panel at the top called `Topbar`. Refer [this](https://docs.blender.org/manual/en/latest/interface/window_system/tabs_panels.html).
- It if often very convenient to change various properties and settings from the vertical panel on the right side called `Properties Panel` instead of using a [node editor](https://docs.blender.org/manual/en/2.79/editors/node_editor/index.html). 
When I say something like "Object Properties" (note the upper case letters and last word is Properties), you can find the icon on right side (Properties Panel). The icons are arranged vertically, hover over them to see their name.
- I'll briefly explain how to use node editor as well, they are equivalent in functionality. For complicated things, use node editor, for simple operations I prefer Properties Panel but it is up to yoo.
- For scaling, rotating and moving an object, there are many ways. In Layout, there is a vertical panel on the left side, click on an icon, click on object to select and you should see arrows appear. Drag the arrows to perform the action. Alternatively, in Layout click `r` to rotate, `s` to scale and `m` to move.
- The other, more elegant way is through Object Properties, you can enter a number in the box or click on the arrows near right/left side of the box. You can also enter operators like `*` followed by a number to make things easy. This can also be done through Node Editor.

# Import/Export
- We are using [Wavefront](https://en.wikipedia.org/wiki/Wavefront_.obj_file) because it's human readable and very space efficient compared to other formats.
- You can import your models in any format, however to use with our code, export in Wavefront or alternatively, change the code in `main.py` to support other formats.

## Node Editor
- In Shading there should be a default Principled Bsdf Shader open already. It is important you know how to use that and what means what, refer [doc](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html) and [2 min video](https://www.youtube.com/watch?v=_IjSYLt9k2A).
- We will refer to the some of the actions performed here later in `Properties`.
- To create an image texture, click on an empty spot of the editor, open pop-up with `Ctrl` + `A`, `s` to search and start typing ("Ima" should do here as we want an Image Texture).
- Place Image Texture to left side of Principled Shader, click open to open your file mamager and find your image. 
- Connect the yellow ball to right side of Colour to the yellow ball to left side of Base Colour. 
- All balls can't be connected to each other, the ones on right side can only be connected to other balls on right side. 
- While it is possible to link differently coloured balls, maximum effect is received with same coloured balls being connected and only through particular connections.

## Properties
Click on Material Properties in the Properties panel. You can do this through all editors while Node Editors is mostly through Shading.
- When using Material Properties, the shader is often not present by default, simply click `new` and give it a name.
- Instead of opening the pop-up and searching and etc, as in Node Editor, here you'll notice a ring next to every box/option of the Principled Shader. Click this and simply find what you want.
- Not all nodes can be connected to other nodes, here the ring only shows connectable nodes.
- To add an Image Texture, click on the ring next to Base Colour, open to open your file manager. If using Layout, you will not see any noticeable difference, use Shading for this. You should instantly see the texture being applied. In some edge cases, moving closer or further from the object/changing the angle is required.
- Another interesting Property is Modifiers, I'll use Shrinkwrap over here. Select the object to be attached, navigate to Modifier Properties | Add Modifier | Shrinkwrap Modifier. Excellent but slightly long [video](https://www.youtube.com/watch?v=kNLCJGtsU7M).
- In target, click on the knife at the right side and choose your target. Click on the surface you are attaching to. I recommend adding a little offset (right under it) so that the texture being attached is a little above the surface. Choose `Apply`, `Apply as Shape` is for animating and not needed. Move/Scale texture to the exact spot on the surface. Blender for unknown reasons doesn't like rendering the textures as seperate objects, therefore select the texture and object, or use `a` and then `Ctrl` + `j` to join.