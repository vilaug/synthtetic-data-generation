# Modify Library

First I will talk about adding materials, models, skins and finally removing them.

## Models
- All models are stored in a directory called `Models`
- To add a new material, create a new directory inside `Models`. In `configuration.yaml` 
    - Add the material name to `skins` (refer materials already present for syntax)
    - Add to `flask | Materials` in `FLask | Materials` to display on GUI 
    - Add to appropriate number in `change_skin`, ignore if 0 map_Kd lines are in `mtl` file
    - add to `info_json` @Augustus
    - in an edge case, if Crushing complains due to adding a new material, create an empty directory in `Crushed Models` @Abel
    
- New models can be added to existing materials by simply creating directories and updating `configuration.yaml`.
    - update `skins` with array of skins if required
    - update `change_skin.json` with number of occurances of `map_Kd`
    
- To add more skins to the existing library of models and materials, 
    - Add image to `Models` directory
    - Add name of image to `skins` in `configuration.yaml`
  
- To temporarily remove a skin, remove the image from `skins` in `configuration.yaml`.
- To permanently remove it, remove the image from `Models` directory and `skins` in `configuration.yaml`
 