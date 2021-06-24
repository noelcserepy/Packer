from packer.texture_match import TextureMatch
import json

test_settings = json.load(open("tests/test_settings.json"))
test_path = "C:/Users/noelc/OneDrive/Desktop/syncdir/Game/EF_Edie/Textures/Chair_r.PNG"

def test_filename_full():
    tm = TextureMatch(test_settings, test_path)
    assert tm.filename_full == "Chair_r.PNG"

def test_filename():
    tm = TextureMatch(test_settings, test_path)
    assert tm.filename == "Chair_r"

def test_extension():
    tm = TextureMatch(test_settings, test_path)
    assert tm.extension == "PNG"

def test_directory():
    tm = TextureMatch(test_settings, test_path)
    assert tm.directory == "C:/Users/noelc/OneDrive/Desktop/syncdir/Game/EF_Edie/Textures/"

def test_asset_name():
    tm = TextureMatch(test_settings, test_path)
    assert tm.asset_name == "Chair"

def test_preferred_filename():
    tm = TextureMatch(test_settings, test_path)
    assert tm.preferred_filename == "R_Chair.PNG"

def test_texture_type():
    tm = TextureMatch(test_settings, test_path)
    assert tm.texture_type == "Roughness"

def test_preferred_identifier():
    tm = TextureMatch(test_settings, test_path)
    assert tm.preferred_identifier == ["R_", "start"]




