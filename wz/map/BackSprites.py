import os
import pygame

from wz.xml.BaseXml import Layer, BaseXml
from wz.info.Instance import Instance
from wz.info.Canvas import Canvas


class BackSprites():
    def __init__(self):
        self.xml = {}
        self.images = {}
        self.sprites = pygame.sprite.Group()

    def load_xml(self, name, path):

        # Check if xml has already been loaded before
        if name in self.xml:
            print('{} was already loaded.'.format(name))
            return

        # Load and parse the xml
        file = "{}/map.wz/Back/{}.img.xml".format(path, name)
        self.xml[name] = BaseXml()
        self.xml[name].open(file)
        self.xml[name].parse_root(Layer.CANVAS_ARRAY)

    def load_sprites(self, name, path):

        # Check if xml has finished loading
        if name not in self.xml or not self.xml[name].objects:
            print('{} was not loaded yet.'.format(name))
            return

        # Get current xml file
        xml = self.xml[name]

        # Load sprites for a given xml file
        sprites = []
        for index in range(0, 100):  # Num images
            file = "{}/map.wz/Back/{}/back.{}.png".format(
                path, xml.name, str(index))
            if os.path.isfile(file):
                image = pygame.image.load(file).convert_alpha()
                sprites.append(image)
            else:
                break

        # Set images
        self.images[name] = sprites

    def load_objects(self, name, object_instances):

        # Check if xml has finished loading
        if name not in self.xml or not self.xml[name].objects:
            print('{} was not loaded yet.'.format(name))
            return

        # Go through instances list and add
        for instance in object_instances:
            try:

                # Build object
                obj = Instance()

                # Required properties
                obj.x = int(instance['x'])
                obj.y = int(instance['y'])
                obj.cx = int(instance['cx'])
                obj.cy = int(instance['cy'])
                obj.rx = int(instance['rx'])
                obj.ry = int(instance['ry'])
                obj.f = int(instance['f'])
                obj.a = int(instance['a'])
                obj.type = int(instance['type'])
                obj.front = int(instance['front'])
                obj.ani = int(instance['ani'])
                obj.bS = instance['bS']
                obj.no = int(instance['no'])

                # Get sprite by key and index
                sprites = self.images[obj.bS]
                sprite = sprites[obj.no]
                w, h = sprite.get_size()

                # Get additional properties
                object_data = self.xml[name].objects
                back_data = object_data['back']
                data = back_data[obj.no]
                x = int(data['x'])
                y = int(data['y'])
                z = int(data['z'])

                # Create a canvas object
                canvas = Canvas(sprite, w, h, x, y, z)

                # Flip
                if obj.f > 0:
                    canvas.flip()

                # Add to object
                obj.add_canvas(canvas)

                # Add to list
                self.sprites.add(obj)

            except:
                print('Error while loading backs')
                continue

    def calculate_x(self, rx, dx, z):
        return float(rx * (dx + z) / 100) + z

    def calculate_y(self, ry, dy, z):
        return float(ry * (dy + z) / 100) + z

    def update(self):
        pass
        # horizontal = [4, 6]
        # vertical = [5, 7]
        # frame_ticks = 1
        # for obj in self.objects:
        #     if obj.type in horizontal and obj.width > 0:
        #         obj.frame_offset += obj.rx / frame_ticks
        #         obj.frame_offset %= obj.width
        #     if obj.type in vertical and obj.height > 0:
        #         obj.frame_offset += obj.ry / frame_ticks
        #         obj.frame_offset %= obj.height

    def blit(self, surface, offset=None):
        if not self.sprites:
            return

        # Get surface properties
        w, h = surface.get_size()

        # For all objects
        for obj in self.sprites:
            try:

                # Camera offset
                dx = offset.x if offset else 0
                dy = offset.y if offset else 0
                x = self.calculate_x(obj.rx, dx, 0.5 * w)
                y = self.calculate_y(obj.ry, dy, 0.5 * h)
                rect = obj.rect.move(x, y)

                # 0 - Simple image (eg. the hill with the tree in the background of Henesys)
                # 1 - Image is copied horizontally (eg. the sea in Lith Harbor)
                # 2 - Image is copied vertically (eg. trees in maps near Ellinia)
                # 3 - Image is copied in both directions (eg. the background sky color square in many maps)
                # 4 - Image scrolls and is copied horizontally (eg. clouds)
                # 5 - Image scrolls and is copied vertically (eg. background in the Helios Tower elevator)
                # 6 - Image scrolls horizontally, and is copied in both directions (eg. the train in Kerning City subway JQ)
                # 7 - Image scrolls vertically, and is copied in both directions (eg. rain drops in Ellin PQ maps)

                if obj.type == 0:
                    surface.blit(obj.image, rect)
                elif obj.type == 1:
                    delta = obj.cx if obj.cx > 0 else obj.rect.width
                    if delta > 0:
                        tile = rect.copy()
                        while tile.x < w:
                            surface.blit(obj.image, tile)
                            tile = tile.move(delta, 0)
                        tile = rect.copy()
                        while tile.x > -obj.rect.width:
                            surface.blit(obj.image, tile)
                            tile = tile.move(-delta, 0)
                elif obj.type == 2:
                    pass
                elif obj.type == 3:
                    pass
                elif obj.type == 4:
                    pass
                elif obj.type == 5:
                    pass
                elif obj.type == 6:
                    pass
                elif obj.type == 7:
                    pass

            except:
                continue