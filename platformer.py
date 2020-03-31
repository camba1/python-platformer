import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Awesome Game"

# SPRITE SCALING
CHARACTER_SCALING = 1
TILE_SCALIING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALIING)

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

PLAYER_START_X = 64
PLAYER_START_Y = 225

#Margin between charactddr and edge of screen
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 250
TOP_VIEWPORT_MARGIN = 250

class MyGame(arcade.Window):
    """
    Main awesome app class
    """

    def __init__(self):

        # Call parent class and init the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # LISTS TO TRACK SPRITES
        self.coin_list = None
        self.wall_list = None
        self.foreground_list = None
        self.background_list = None
        self.dont_touch_list = None
        self.player_list = None

        # Player Sprite
        self.player_sprite = None

        # Physics Engine
        self.physics_engine = None

        # Scroll trakcking
        self.view_bottom = 0
        self.view_left = 0

        # track score
        self.score = 0

        self.end_of_map = 0

        # Level
        self.level = 1

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self, level):
        # Game setup
        # create sprite lists

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.foreground_list = arcade.sprite_list
        self.background_list = arcade.sprite_list

        # setup player
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # load map from tiled editor

        map_name = ":resources:tmx_maps/map2_level_{0}.tmx".format(level)
        # name of layer in the file
        platforms_layer_name = 'Platforms'
        # Name of layer with items for pick up
        coins_layer_name = "Coins"
        foreground_layer_name = "Foreground"
        background_layer_name = "Background"
        dont_touch_layer_name = "Don't Touch"

        my_map = arcade.tilemap.read_tmx(map_name)
        # Calc right side of map
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE
        self.background_list = arcade.tilemap.process_layer(my_map,
                                                            background_layer_name,
                                                            TILE_SCALIING)
        self.foreground_list = arcade.tilemap.process_layer(my_map,
                                                             foreground_layer_name,
                                                             TILE_SCALIING)

        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALIING)
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name, TILE_SCALIING)
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            dont_touch_layer_name,
                                                            TILE_SCALIING)

        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)


        # # Setup ground
        # for x in range(0, 1250, 64):
        #     wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALIING)
        #     wall.center_x = x
        #     wall.center_y = 32
        #     self.wall_list.append(wall)
        #
        # # Setup crates
        # coordinate_list = [[512, 96],
        #                    [256, 96],
        #                    [768, 96]]
        # for coordinate in coordinate_list:
        #     wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALIING)
        #     wall.position = coordinate
        #     self.wall_list.append(wall)
        #
        # # Add Coins
        # for x in range(120, 1250, 256):
        #     coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
        #     coin.center_x = x
        #     coin.center_y = 96
        #     self.coin_list.append(coin)

        # Add physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,self.wall_list, GRAVITY)

    def on_draw(self):
        # Render Screen

        arcade.start_render()

        # code to draw screen
        self.wall_list.draw()
        self.background_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.dont_touch_list.draw()
        self.player_list.draw()
        self.foreground_list.draw()

        # Draw score, scroll with viewport
        score_text = "Score: {0}".format(self.score)
        arcade.draw_text(score_text, 10 + self.view_left,
                         10 + self.view_bottom, arcade.csscolor.BLACK, 20)

    def on_key_press(self,key,modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        # elif key == arcade.key.DOWN or key == arcade.key.S:
        #     self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self,key,modifiers):
        # if key == arcade.key.UP or key == arcade.key.W:
        #     self.player_sprite.change_y = 0
        # elif key == arcade.key.DOWN or key == arcade.key.S:
        #     self.player_sprite.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)
        for coin in coin_hit_list:
            #remove coin
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score +=1

        changed_viewport = False

        # Did player fall off the wall?
        if self.player_sprite.center_y == -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # adjust cameera
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

        # Did the palyer touch a forbiden item?
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # adjust cameera
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

        # Check if user beat level
        if self.player_sprite.center_x > self.end_of_map:
            # Advance to next map
            self.level += 1
            self.setup(self.level)
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True


        # Scrolling
        changed = False

        # left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # UP
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

def main():
    window = MyGame()
    window.setup(window.level)
    arcade.run()


if __name__ == '__main__':
    main()
