import game

class ExampleComponent(object):
    
    def add(self, entity):
        entity.register_handler('update', self.handle_update)
        game.get_game().register_for_updates(entity)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        print '%f seconds have elapsed!' % (dt,)

class MovementComponent(object):
    
    def add(self, entity):
        entity.register_handler('update', self.handle_update)
        game.get_game().register_for_updates(entity)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        entity.props.x += entity.props.dx
        entity.props.y += entity.props.dy
        
        
class InputMovementComponent(object):
    
    def add(self, entity):
        entity.register_handler('move', self.handle_update)
        game.get_game().register_for_updates(entity)
    
    def remove(self, entity):
        entity.unregister_handler('move', self.handle_update)
    
    def handle_update(self, entity, event):
        print 'You moved %s' % (event,)