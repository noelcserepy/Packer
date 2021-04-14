from tex_import import *
import tex_import

def test_detect_changes_no_data(mocker):
    mocker.patch.object(tex_import.detect_changes, dir, )
    assert 1 == 1