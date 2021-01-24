# Aluminium Can

I will assume you have followed the steps in Setup.md and read through General.md
 
1. Set base colour to a shade of silver (for top and bottom parts of the can).
2. Give other Principled attributes values such as Metallic = 1, lower roughness and add other you want your model to have.
3. Enter x-ray view (`Ctlr + Z`) in edit mode. Align your object by clicking on an axis near top right corner.
4. Click and drag to select the curved parts of the can with `LSB` (be careful to not select the inside parts of top and bottom parts of the can as x-ray view selects all triangles behind the box you make). If you don't use x-ray view, you will only select the triangles visible on your screen i.e. one side. In that case, after making the box, hold `Shift` and release `LSB`, release `Shift`. Re-position your object, hold `Shift` and click `LSB` and drag again.
5. In Material Properties, make a new Principled Bsdf Shader if not present and create an Image Texture as explained in General.md.
6. Mirror the Principled attributes or change as you would like on the image texture as well (the image texture will be applied on top of the surface created earlier).