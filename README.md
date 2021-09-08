# What is Packer?
Packer is an optimization tool for real-time 3D rendering. It automates the process of "texture packing". It locates image files of user-defined types and merges them into RGBA channels on a per-asset basis. This saves costly texture lookups in the 3D engine. 


## What problem does Packer solve?
### Reducing iteration time
Texture packing, while being important for optimization, is a pain to implement into the development process. The 3D artists responsible for designing these textures will have to create the textures, then import them to photoshop, then make sure all the textures are on the right channels, then save the new file, then import them into the engine to see the final result. If the artists want to change the texture, they have to go through that same process. You can see how this can kill valuable time, as well as the artists' inspiration. 

Packer automates all that. The artist saves a texture file, Packer detects and re-packs it automatically, ready for import into the engine. No wasted time, no errors. This can also be used to integrate externally sourced assets into the pipeline without friction.

### Flexible packing strategy for studios
Traditionally, studios have to decide early on, which textures/channels configuration to use, so that all future textures are compatible with existing shaders. This decision locks developers into one path, which can only be changed through painstaking re-packing of thousands of assets. 

With Packer, all you need to do is to define new packing groups, run it on the asset directory and voilà!


## What is texture packing?
In real-time 3D, frames per second (fps) is one of the most important values to track. If a game runs with 2 fps, you can't play it. If a VR simulation doesn't run smoothly, it can cause nausea. One technique to optimize fps is called "texture packing". It merges texture files of different types into one image file by using RGBA channels. So instead of using separate files for base colour and roughness, base colour can use channels R, G and B, while roughness uses channel A. That means that the shader (a program that runs on the graphics card, responsible for rendering graphics) has to look up one less texture file every time it is run. And it is run A LOT! In fact it runs once for every frame, for every pixel on your screen. 


## How does it work?
Luckily, all of the actual packing is done for you. All that is required from you is the setup. Setup includes two main sections.

### General
- Search directory: where Packer should look for texture files.
- Output directory: The output directory can be specified but the default is to save the output file in the same location as the asset textures. 
- Overwrite old: overwrites old files that have been packed by Packer. This prevents unneccessary cluttering of the directory when Packer is run again.
- Auto rename: renames all identified texture files to match your preferred pre/postfix naming convention.

### Texture types setup
Here you define what textures Packer should look for. 
- Texture type: the type of texture e.g. base colour, roughness, normal etc.
- Prefix/Postfix: what pre/postfixes are used to identify this texture type e.g. N_assetName for normal maps.
- File Type: what file extensions Packer should look for e.g. .PNG, .TIF, .JPG.
- Preferred Prefix/Postfix: what is your preferred pre/postfix for this texture type. This will be used for a future renaming option.

### Packing group setup
Here you define how these textures should be packed.
- Name: the name of your new combined texture type. This is for you to identify these new files.
- Preferred Prefix/Postfix: what is your preferred pre/postfix for this texture type e.g. DR_assetName for a diffuse + roughness texture.
- File Type: what file extension the output file should be e.g. .PNG, .TIF, .JPG.
- Channels R G B A: what texture type should be packed into which channel of the output image. 

With this information, Packer will find all of the files of your specified texture types. It then groups these by asset name. If all of the texture types of any of your defined packing groups are found, it will group them and let you know that these packing groups are ready to pack. Then just press "Pack" and Packer merges the images of each packing groups. With live-packing, Packer can identify any changes to the search directory and pack new or updated textures in the background. 