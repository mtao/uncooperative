'''
Created on May 2, 2013

@author: jonathan
'''

import os
import sys

import pygame

import componentmanager
from entitymanager import EntityManager
from entity import Entity
from component import MovementComponent, ExampleComponent, InputMovementComponent, TileDraw
from resourcemanager import ResourceManager, LoadEntityDefinition, LoadImage

from render import Render
from input import InputEvent, InputManager

from random import randint

_game = None
from gridgen import GridGenerator
from grid import Grid,Vec2


class Game(object):
    
    def __init__(self):
        self.screen_size = (500,500)
        self.map_size = (128,128)
        self.tile_size = (5,5)
        self.world_size = (self.tile_size[0] * self.map_size[0], self.tile_size[1] * self.map_size[1])
        
        self.grid = Grid(self.world_size[0],self.world_size[1])
        GridGenerator(self.grid,Vec2(self.tile_size[0],self.tile_size[1]))
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500,500))
        
        self.component_manager = componentmanager.ComponentManager()
        self.component_manager.register_component('MovementComponent', MovementComponent())
        self.component_manager.register_component('ExampleComponent', ExampleComponent())
        self.component_manager.register_component('TileDraw', TileDraw())
        self.component_manager.register_component('InputMovementComponent', InputMovementComponent())

        self.entity_manager = EntityManager()
        
        self.resource_manager = ResourceManager(os.path.join(sys.path[0], 'res'))
        self.resource_manager.register_loader('definition', LoadEntityDefinition)
        self.resource_manager.register_loader('sprite', LoadImage)

        self.input_manager = InputManager()
        self.input_manager.init_joysticks()

        self.entities_to_update = []
        self.entities_to_input = []
        self.entities_to_draw_tiles = []
        
        
    def register_for_updates(self, entity):
        self.entities_to_update.append(entity)
        
    def register_for_input(self, entity):
        self.entities_to_input.append(entity)
    
    def register_for_draw_tiles(self,entity):
        self.entities_to_draw_tiles.append(entity)
        
    def run(self):
        
        
        #test_entity = Entity('test-include')
        character = Entity('character')
        self.characters = [character for m in xrange(4)]
        self.renderer = Render(self)

        
        
        self.current_camera = 0
        while True:
            dt = self.clock.tick() / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT: sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_TAB:
                        self.current_camera = (self.current_camera +1)%4
                    if e.key == pygame.K_a:
                        #self.cameras[self.current_camera].props.dx = 1
                        pass
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_a:
                        #self.cameras[self.current_camera].props.dx = 0
                        pass
                if e.type == pygame.JOYAXISMOTION or \
                        e.type == pygame.JOYBALLMOTION or \
                        e.type == pygame.JOYBUTTONDOWN or \
                        e.type == pygame.JOYBUTTONUP or \
                        e.type == pygame.JOYHATMOTION or \
                        e.type == pygame.KEYDOWN or \
                        e.type == pygame.KEYUP:
                    event = InputEvent(e)

                    for entity in self.entities_to_update:
                        if e.type == pygame.JOYAXISMOTION:
                            entity.handle('move', event)
                        else:
                            entity.handle('input', event)

            for entity in self.entities_to_draw_tiles:
                entity.handle('draw-tiles',self.world_surface)
            
            for entity in self.entities_to_update:
                entity.handle('update', dt)
            self.renderer.render()

def get_game():
    global _game
    if not _game:
        _game = Game()
    return _game
