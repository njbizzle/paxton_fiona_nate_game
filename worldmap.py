
current_id = 0
def get_id():
    global current_id
    current_id+=1
    return current_id

class Worldmap:
    def __init__(self):
        self.worldmap_dict = {}
    
    def add_sprite(self, sprite, pos):
        self.worldmap_dict[[pos, current_id]] = sprite # create new entry in the dict
    
    def objects_at_pos_id(self, pos_ids):
        return [self.worldmap_dict[pos_id] for pos_id in pos_ids] # get 
            
    def get_object_at_tile_range(self, xmin_max, ymin_max):

        xmin = xmin_max[0]
        xmax = xmin_max[1]

        ymin = ymin_max[0]
        ymax = ymin_max[1]

        all_positions_ids = self.worldmap_dict.keys() # get all the positions of sprites (can optomize later if its a problem)

        poses_to_return = []

        for pos_id in all_positions_ids:
            pos = pos_id[0]
            if not(pos[0] > xmin and pos[0] < xmax): # skip it if its out of x range
                continue
            if not(pos[0] > ymin and pos[0] < ymax): # skip it if its out of y range
                continue
            poses_to_return.append(pos_id)

        return self.objects_at_pos_id(poses_to_return)

worldmap = Worldmap()