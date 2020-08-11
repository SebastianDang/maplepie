import os
from nx.nxfile import NXFile

path = 'P:/Downloads/Resources'  # TODO: Change this to use your nx path


def test_nximage():
    node = NXFile(os.path.join(path, 'map.nx')).resolve(
        "Tile/grassySoil.img/bsc/0")
    byte = node.getImage()
    assert node.name == '0'
    assert node.width == 90
    assert node.height == 60
    assert len(byte) == 90 * 60 * 4


def test_nximage2():
    node = NXFile(os.path.join(path, 'map.nx')).resolve(
        "Obj/acc1.img/grassySoil/nature/0/0")
    byte = node.getImage()
    assert node.name == '0'
    assert node.width == 131
    assert node.height == 39
    assert len(byte) == 131 * 39 * 4