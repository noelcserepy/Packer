class TextureSearch():
    def __init__(self, settings):
        self.dir = settings["sync_asset_dir"]
        self.textures = settings["textures"]

    def _identify_texture(self, file):
        """ 
        Takes in full file path. If file is a texture specified by settings, return a dict of information about that texture.
        """
        filename_full = file.split("/")[-1]
        filename, extension = filename_full.split(".")
        directory = file[:-len(filename_full)]

        for tex in self.textures:
            if extension.upper() not in tex["extensions"]:
                continue
            pref_id = tex["preferred_identifier"]
            for id in tex["identifiers"]:
                if id[1] == "end":
                    if filename.endswith(id[0]):
                        asset_name = filename[:-len(id[0])]
                        if pref_id[1] == "start":
                            new_filename = f"{pref_id[0]}{asset_name}"
                        if pref_id[1] == "end":
                            new_filename = f"{asset_name}{pref_id[0]}"
                        new_full_filename = f"{new_filename}.{extension}"
                        texture = {
                            "asset_name": asset_name,
                            "path": file,
                            "dir": directory,
                            "current_filename": filename_full,
                            "preferred_filename": new_full_filename,
                            "texture_type": tex["name"]
                        }
                        return texture

                if id[1] == "start":
                    if filename.startswith(id[0]):
                        asset_name =filename[len(id[0]):]
                        if pref_id[1] == "start":
                            new_filename = f"{pref_id[0]}{asset_name}"
                        if pref_id[1] == "end":
                            new_filename = f"{asset_name}{pref_id[0]}"
                        new_full_filename = f"{new_filename}.{extension}"
                        texture = {
                            "asset_name": asset_name,
                            "path": file,
                            "dir": directory,
                            "current_filename": filename_full,
                            "preferred_filename": new_full_filename,
                            "texture_type": tex["name"]
                        }
                        return texture

    def get_files_by_asset(self, files):
        """ 
        Takes a list of files.
        Returns dictionary of assets, each with a list of textures belonging to that asset e.g. {asset_name: [available textures]}.
        """
        asset_files = {}
        for file in files:
            try:
                texture = self._identify_texture(file)
                if not texture:
                    raise Exception("Texture does not exist")
                
                asset_name = texture["asset_name"]
                if asset_name not in asset_files.keys():
                    asset_files[asset_name] = []

                asset_files[asset_name].append(texture)
            except:
                continue
        return asset_files


    


