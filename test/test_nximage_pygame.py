import os

import pygame

from maplepy.nx.resourcenx import ResourceNx
from maplepy.base.sprite import DataSprite
from nxpy.nxfile import NXFile


def test_nxsprite():
    node = NXFile(os.path.join(os.path.dirname(__file__),  'map.nx')).resolve(
        "Back/grassySoil_new.img/back/0")
    image = node.get_image()
    byte = image.get_data()

    assert node.name == '0'
    assert image.width == 22
    assert image.height == 738
    assert len(byte) == 22 * 738 * 4

    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    sprite = DataSprite()
    sprite.load(node.width, node.height, byte)
    sprite.image = pygame.transform.scale(sprite.image, screen.get_size())

    timer = 0
    while(timer < 180):

        # Test event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                pygame.quit()
                return
        pygame.event.pump()

        # Blit image as normal
        screen.blit(sprite.image, sprite.rect)

        # Update display
        pygame.display.update()
        pygame.time.Clock().tick(60)
        timer += 1


def test_nxsprite2():

    node = NXFile(os.path.join(os.path.dirname(__file__),  'map.nx')).resolve(
        "Tile/grassySoil.img/bsc/0")
    image = node.get_image()
    byte = image.get_data()

    assert node.name == '0'
    assert node.width == 90
    assert node.height == 60
    assert len(byte) == 90 * 60 * 4

    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    sprite = DataSprite()
    sprite.load(node.width, node.height, byte)
    sprite.image = pygame.transform.scale(sprite.image, screen.get_size())

    timer = 0
    while(timer < 180):

        # Test event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                pygame.quit()
                return
        pygame.event.pump()

        # Blit image as normal
        screen.blit(sprite.image, sprite.rect)

        # Update display
        pygame.display.update()
        pygame.time.Clock().tick(60)
        timer += 1


def test_nxspritemanager():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    file = NXFile(os.path.join(os.path.dirname(__file__),  'map.nx'))
    manager = ResourceNx()
    manager.file = file
    sprite = manager.get_sprite(file, 'Back/grassySoil_new.img/back/0')
    sprite2 = manager.get_sprite(file, 'Tile/grassySoil.img/enV0/1')
    sprite3 = manager.get_sprite(file, 'Obj/acc1.img/grassySoil/nature/0/0')
    sprite.image = pygame.transform.scale(sprite.image, screen.get_size())
    sprite2.image = pygame.transform.scale(sprite2.image, screen.get_size())
    sprite3.image = pygame.transform.scale(sprite3.image, screen.get_size())

    timer = 0
    while(timer < 180):

        # Test event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.clear()
                pygame.quit()
                return
        pygame.event.pump()

        # Blit image as normal
        screen.blit(sprite.image, sprite.rect)
        screen.blit(sprite2.image, sprite2.rect)
        screen.blit(sprite3.image, sprite3.rect)

        # Update display
        pygame.display.update()
        pygame.time.Clock().tick(60)
        timer += 1
