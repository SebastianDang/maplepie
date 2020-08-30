import os
import nx.nxfile as nxfile
from nx.nxfileset import NXFileSet


class MapNx:

    """ Helper class to get values from a map nx file. """

    def __init__(self):
        self.file = NXFileSet()

    def open(self, file):
        # Check if file exists
        if not os.path.exists(file):
            print('{} does not exist'.format(file))
            return
        try:
            # Open nx file
            self.file.load(file)
        except:
            print('Unable to open {}'.format(file))

    def get_map_nodes(self, map_root):
        map_nodes = {}
        for i in range(0, 9):
            map_digit = map_root.getChild('Map{}'.format(i))
            if not map_digit:
                continue
            for map_id in map_digit.listChildren():
                node = map_digit.getChild(map_id)
                if not node:
                    continue
                map_nodes[map_id] = node
        return map_nodes

    def get_map_node(self, map_id):
        img = "Map/Map{}/{}.img".format(map_id[0:1], map_id)
        return self.file.resolve(img)

    def get_info_data(self, map_id):
        info = {}
        img = "Map/Map{}/{}.img".format(map_id[0:1], map_id)
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        info_node = map_node.getChild('info')
        for child in info_node.getChildren():
            info[child.name] = child.value
        return info

    def get_minimap_data(self, map_id):
        minimap = {}
        img = "Map/Map{}/{}.img".format(map_id[0:1], map_id)
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        # Get the current minimap node
        minimap_node = map_node.getChild('miniMap')
        if not minimap_node:
            return None
        for child in minimap_node.getChildren():
            minimap[child.name] = child.value
        return minimap

    def get_background_data(self, map_id):
        back = []
        img = "Map/Map{}/{}.img".format(map_id[0:1], map_id)
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        # Get the current back node
        back_node = map_node.getChild('back')
        if not back_node:
            return None
        # Get values
        for index in back_node.listChildren():
            array_node = back_node.getChild(index)
            data = {'name': index}
            for child in array_node.getChildren():
                data[child.name] = child.value
            back.append(data)
        return back

    def get_layer_data(self, map_id, index):
        layer = {}
        img = "Map/Map{}/{}.img".format(map_id[0:1], map_id)
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        # Get the current layer
        layer_node = map_node.getChild(str(index))
        if not layer_node:
            return None
        # Get info for this layer
        info = {}
        info_node = layer_node.getChild('info')
        for name in info_node.listChildren():
            info[name] = info_node.getChild(name).value
        # Get tiles for this layer
        tiles = []
        tile_node = layer_node.getChild('tile')
        for array_node in tile_node.getChildren():
            data = {'name': array_node.name}
            for child in array_node.getChildren():
                data[child.name] = child.value
            tiles.append(data)
        # Get objects for this layer
        objects = []
        object_node = layer_node.getChild('obj')
        for array_node in object_node.getChildren():
            data = {'name': array_node.name}
            for child in array_node.getChildren():
                data[child.name] = child.value
            objects.append(data)
        # Add layer
        layer = {'info': info, 'tile': tiles, 'obj': objects}
        return layer

    def get_portal_data(self, map_id):
        portal = []
        img = "Map/Map{}/{}.img".format(map_id[0:1], map_id)
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        # Get the current back node
        back_node = map_node.getChild('portal')
        if not back_node:
            return None
        # Get values
        for index in back_node.listChildren():
            array_node = back_node.getChild(index)
            data = {'name': index}
            for child in array_node.getChildren():
                data[child.name] = child.value
            portal.append(data)
        return portal

    def get_data(self, path):
        data = {}
        node = self.file.resolve(path)
        for child in node.getChildren():
            data[child.name] = child.value
        return data
