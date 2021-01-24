# Setup
Here I'll describe some certain steps I expect have been done before colouring any model.

1. Import object, scale it appropriately. The camera is set at `(0, 0, 3`, if changed, check `configuration.yaml`.
2. An easy way to check scaling, import another object (already been scaled) and compare.
3. In layout, go to edit mode through the `Mode` drop down menu on top left or press tab and check that `Edit Mode` appears on top left or `Ctrl` + `Tab` and choose Edit Mode. 
4. click on object, `a` to select all, `u` to show UV Mapping menu | Smart UV Project
5. Set Island Margin to 0.03 by entering or using the arrow key that appears when your pointer goes close to the box and Ok at the bottom.
This will unwrap triangles and quadrilaterals from your 3d object and show them on a 2d plane with padding 0.03. This helps Blender map a triangle to a texture when we later apply them.
The Smart UV Unwrap can be an expensive operation depending on number of triangles of an object. It is normal for Blender to become un-useable at this stage based on number of triangles.
I recommend using `top` command, or an equivalent (if using non-Unix like OS) in terminal to check CPU usage and verify that Blender is indeed doing the computations (laptop hasn't frozen for other reasons).

6. Have a rough sketch on paper or an image in your mind about what you want the final object to look like.
7. Prepare the textures(images) accordingly. 
8. If your model has any base colours such as a pizza box is light brown coloured except for the logo, click on the object go to Material Properties and fill in Base Colour. This shader is usually called Default by default by Blender. Rename appropriately.