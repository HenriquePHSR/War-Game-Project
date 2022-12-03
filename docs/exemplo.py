import pip
import pygame
import time

from PPlay.window import *
from PPlay.sprite import *
from PPlay.collision import *
from PPlay.mouse import *
from PPlay.keyboard import *
from PPlay.character import *

# System_variables
local = 0
fps_per_sec = 0
fps = 0
sec = 0
aux = 1.0
janela = Window(800, 600)
teclado = Window.get_keyboard()
mouse = Mouse()
colisao = Collision()
# Load_Assets
if True:
    print("Loading ")
    # Assets without collision
    pivo = Sprite("_assets\pont.png")
    play = Sprite("_assets\menu\play.jpg")
    exit = Sprite("_assets\menu\exit.jpg")
    sky = Sprite(
        "_assets\Background\country-platform-files\country-platform-files\layers\country-platform-back(01).png")
    ground = Sprite(
        "_assets\Background\country-platform-files\country-platform-files\layers\country-platform-tiles-example(01).png")
    floor = Sprite("_assets\Background\Full_floor.png")
    floor_2 = Sprite("_assets\Background\Full_floor.png")
    stage_1_layer = Sprite("_assets\Background\city_stage.png")
    stage_1_layer_2 = Sprite("_assets\Background\stage_1_layer_2.png")
    wall_brick = Sprite("_assets/Background/wall_brick.png")
    wall_brick_2 = Sprite("_assets/Background/wall_brick.png")
    castle_wall = Sprite("_assets/Background/castle_wall.png")
    castle_interior = Sprite("_assets/Background/castle_interior.png")
    castle_wall_2 = Sprite("_assets/Background/castle_wall.png")
    timer_2 = 100

    # Position
    pivo.set_position(0, 0)
    floor.set_position(pivo.x, pivo.y + 515)
    floor_2.set_position(pivo.x + -3500, pivo.y + 515)
    ground.set_position(pivo.x, pivo.x)
    sky.set_position(pivo.x, pivo.x)
    play.set_position(pivo.x + 330, pivo.y + 300)
    exit.set_position(pivo.x + 330, pivo.y + 200)
    play.set_position(pivo.x + 330, pivo.y + 200)
    exit.set_position(pivo.x + 330, pivo.y + 300)
    stage_1_layer.set_position(pivo.x + -50, pivo.y + 150)
    stage_1_layer_2.set_position(pivo.x + -50, pivo.y + 40)
    wall_brick.set_position(pivo.x + -3000, pivo.y + 440)
    wall_brick_2.set_position(pivo.x + -3500, pivo.y + 440)
    castle_wall.set_position(pivo.x + -3500, pivo.y + 200)
    castle_interior.set_position(pivo.x + -3500, pivo.y + 200)
    castle_wall_2.set_position(pivo.x + -3500, pivo.y + 200)
    # characters_construct
    # Inicializa o personagem principal
    HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_100.png")
    HP.set_position(50,50)
    test_character = controlable_char(
    "test",
    Sprite("_assets\protagonista\point.png"),
    100,
    440,
    Sprite("_assets\protagonista\main_Idle.png", 4),
    Sprite("_assets\protagonista\main_Idle_left.png", 4),
    Sprite("_assets\protagonista\main_Running.png", 6),
    Sprite("_assets\protagonista\main_Running_left.png", 6),
    Sprite("_assets\protagonista\jumping_right_01.png", 7),
    Sprite("_assets\protagonista\jumping_left_01.png", 7),
    Sprite("_assets\protagonista\jumping_right_static.png", 4),
    Sprite("_assets\protagonista\jumping_left_static.png", 4),
    Sprite("_assets\protagonista\_falling_right.png", 2),
    Sprite("_assets\protagonista\_falling_left.png", 2),
    Sprite("_assets\protagonista\_full_atk_sequence_right.png", 15),
    Sprite("_assets\protagonista\_full_atk_sequence_left.png", 15),
    Sprite("_assets/protagonista/dying_right.png", 4),
    Sprite("_assets/protagonista/dying_left.png", 4),
    Sprite("_assets/protagonista/dead_right.png"),
    Sprite("_assets/protagonista/dead_left.png"),
    pivo,
    200
    )
    print(".")
    # Lista dos inimigos
    enemies = [NPC(
        "test_npc_1",
        Sprite("_assets\protagonista\point.png"),
        200,
        442,
        Sprite("_assets/inimigos/enemy_blue_idle_right.png", 4),
        Sprite("_assets/inimigos/enemy_blue_idle_left.png", 4),
        Sprite("_assets/inimigos/enemy_blue_running_right.png", 8),
        Sprite("_assets/inimigos/enemy_blue_running_left.png", 8),
        Sprite("_assets/inimigos/enemy_blue_atk_sequence_right.png", 8),
        Sprite("_assets/inimigos/enemy_blue_atk_sequence_left.png", 8),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        pivo,
        test_character.player_pos(),
        100,
        Sprite("_assets/inimigos/die_sequence.png", 8),
        Sprite("_assets/inimigos/die_sequence_right.png", 8),
        Sprite("_assets/inimigos/dead.png"),
        Sprite("_assets/inimigos/dead_right.png"),
        45
    ), NPC(
        "test_npc_2",
        Sprite("_assets\protagonista\point.png"),
        1300,
        442,
        Sprite("_assets/inimigos/enemy_blue_idle_right.png", 4),
        Sprite("_assets/inimigos/enemy_blue_idle_left.png", 4),
        Sprite("_assets/inimigos/enemy_blue_running_right.png", 8),
        Sprite("_assets/inimigos/enemy_blue_running_left.png", 8),
        Sprite("_assets/inimigos/enemy_blue_atk_sequence_right.png", 8),
        Sprite("_assets/inimigos/enemy_blue_atk_sequence_left.png", 8),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        pivo,
        test_character.player_pos(),
        100,
        Sprite("_assets/inimigos/die_sequence.png", 8),
        Sprite("_assets/inimigos/die_sequence_right.png", 8),
        Sprite("_assets/inimigos/dead.png"),
        Sprite("_assets/inimigos/dead_right.png"),
        45
    ), NPC(
        "test_npc_3",
        Sprite("_assets\protagonista\point.png"),
        1800,
        442,
        Sprite("_assets/inimigos/enemy_blue_idle_right.png", 4),
        Sprite("_assets/inimigos/enemy_blue_idle_left.png", 4),
        Sprite("_assets/inimigos/enemy_blue_running_right.png", 8),
        Sprite("_assets/inimigos/enemy_blue_running_left.png", 8),
        Sprite("_assets/inimigos/enemy_blue_atk_sequence_right.png", 8),
        Sprite("_assets/inimigos/enemy_blue_atk_sequence_left.png", 8),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        pivo,
        test_character.player_pos(),
        100,
        Sprite("_assets/inimigos/die_sequence.png", 8),
        Sprite("_assets/inimigos/die_sequence_right.png", 8),
        Sprite("_assets/inimigos/dead.png"),
        Sprite("_assets/inimigos/dead_right.png"),
        45
    ), NPC(
        "test_npc_4",
        Sprite("_assets\protagonista\point.png"),
        1870,
        442,
        Sprite("_assets/inimigos/enemy_blue_idle_right.png", 4),
        Sprite("_assets/inimigos/enemy_blue_idle_left.png", 4),
        Sprite("_assets/inimigos/enemy_blue_running_right.png", 8),
        Sprite("_assets/inimigos/enemy_blue_running_left.png", 8),
        Sprite("_assets/inimigos/enemy_blue_atk_sequence_right.png", 8),
        Sprite("_assets/inimigos/enemy_blue_atk_sequence_left.png", 8),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        pivo,
        test_character.player_pos(),
        100,
        Sprite("_assets/inimigos/die_sequence.png", 8),
        Sprite("_assets/inimigos/die_sequence_right.png", 8),
        Sprite("_assets/inimigos/dead.png"),
        Sprite("_assets/inimigos/dead_right.png"),
        45
    ), NPC(
        "test_npc_5",
        Sprite("_assets\protagonista\point.png"),
        2000,
        442,
        Sprite("_assets/inimigos/enemy_blue_idle_right.png", 4),
        Sprite("_assets/inimigos/enemy_blue_idle_left.png", 4),
        Sprite("_assets/inimigos/enemy_blue_running_right.png", 8),
        Sprite("_assets/inimigos/enemy_blue_running_left.png", 8),
        Sprite("_assets/inimigos/enemy_blue_atk_sequence_right.png", 8),
        Sprite("_assets/inimigos/enemy_blue_atk_sequence_left.png", 8),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        pivo,
        test_character.player_pos(),
        100,
        Sprite("_assets/inimigos/die_sequence.png", 8),
        Sprite("_assets/inimigos/die_sequence_right.png", 8),
        Sprite("_assets/inimigos/dead.png"),
        Sprite("_assets/inimigos/dead_right.png"),
        45
    ),NPC(
        "King",
        Sprite("_assets\protagonista\point.png"),
        3400,
        442,
        Sprite("_assets/NPC/4 directional character/king_idle.png",4),
        Sprite("_assets/NPC/4 directional character/king_idle.png",4),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        pivo,
        [-1000,-1000],
        100,
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        Sprite("_assets\protagonista\point.png"),
        45
    )
    ]
    print(".")
    # A lista props armazena todos os objetos do cenario
    props = [
        obstaculos(
        'test_prop',
        Sprite("_assets\protagonista\point.png"),
        100,
        440,
        Sprite(
            "_assets\Background\GothicVania-town-files\GothicVania-town-files\PNG\environment\props-sliced\wagon.png"),
        pivo,
        test_character.player_pos(),
        1
    ), obstaculos(
        'test_prop',
        Sprite("_assets\protagonista\point.png"),
        200,
        410,
        Sprite(
            "_assets\Background\GothicVania-town-files\GothicVania-town-files\PNG\environment\props-sliced\street-lamp.png"),
        pivo,
        test_character.player_pos(),
        1
    ), obstaculos(
        'test_prop',
        Sprite("_assets\protagonista\point.png"),
        400,
        410,
        Sprite(
            "_assets\Background\GothicVania-town-files\GothicVania-town-files\PNG\environment\props-sliced\street-lamp.png"),
        pivo,
        test_character.player_pos(),
        1
    ), obstaculos(
        'test_prop',
        Sprite("_assets\protagonista\point.png"),
        600,
        410,
        Sprite(
            "_assets\Background\GothicVania-town-files\GothicVania-town-files\PNG\environment\props-sliced\street-lamp.png"),
        pivo,
        test_character.player_pos(),
        1
    ), obstaculos(
        'test_prop',
        Sprite("_assets\protagonista\point.png"),
        800,
        410,
        Sprite(
            "_assets\Background\GothicVania-town-files\GothicVania-town-files\PNG\environment\props-sliced\street-lamp.png"),
        pivo,
        test_character.player_pos(),
        1
    ), obstaculos(
        'test_prop',
        Sprite("_assets\protagonista\point.png"),
        1000,
        410,
        Sprite(
            "_assets\Background\GothicVania-town-files\GothicVania-town-files\PNG\environment\props-sliced\street-lamp.png"),
        pivo,
        test_character.player_pos(),
        1
    ),obstaculos(
        'test_prop',
        Sprite("_assets\protagonista\point.png"),
        1200,
        440,
        Sprite(
            "_assets\Background\GothicVania-town-files\GothicVania-town-files\PNG\environment\props-sliced\wagon.png"),
        pivo,
        test_character.player_pos(),
        1),
        obstaculos(
            'test_prop',
            Sprite("_assets\protagonista\point.png"),
            1500,
            440,
            Sprite(
                "_assets\Background\GothicVania-town-files\GothicVania-town-files\PNG\environment\props-sliced\wagon.png"),
            pivo,
            test_character.player_pos(),
            1),
        obstaculos(
            'test_prop',
            Sprite("_assets\protagonista\point.png"),
            1800,
            455,
            Sprite(
                "_assets\Background\GothicVania-town-files\GothicVania-town-files\PNG\environment\props-sliced\crate-stack.png"),
            pivo,
            test_character.player_pos(),
            1),
        obstaculos(
            'test_prop',
            Sprite("_assets\protagonista\point.png"),
            2500,
            460,
            Sprite(
                "_assets\Background\GothicVania-town-files\GothicVania-town-files\PNG\environment\props-sliced\well.png"),
            pivo,
            test_character.player_pos(),
            1),
        obstaculos(
        'test_prop',
        Sprite("_assets\protagonista\point.png"),
        3150,
        200,
        Sprite("_assets/Background/castle_interior.png"),
        pivo,
        test_character.player_pos(),
        1
    ),
        obstaculos(
            'test_prop',
            Sprite("_assets\protagonista\point.png"),
            3150,
            420,
            Sprite("_assets/Background/door.png"),
            pivo,
            test_character.player_pos(),
            1
        ),
        obstaculos(
            'test_prop',
            Sprite("_assets\protagonista\point.png"),
            3400,
            410,
            Sprite("_assets/Background/door_2.png"),
            pivo,
            test_character.player_pos(),
            1
        ),
        obstaculos(
            'test_prop',
            Sprite("_assets\protagonista\point.png"),
            3500,
            200,
            Sprite("_assets/Background/castle_interior.png"),
            pivo,
            test_character.player_pos(),
            1
        ),
        obstaculos(
            'test_prop',
            Sprite("_assets\protagonista\point.png"),
            3900,
            200,
            Sprite("_assets/Background/castle_interior.png"),
            pivo,
            test_character.player_pos(),
            1
        )

    ]
    print(".")
    # Assets with collision
new_run = 1







#Game loop
while (True):
    test_dmg = 0

    posicao = pivo
    janela.set_background_color((0, 0, 0))

    # condição do menu
    if local == 0:
        ground.x = 0
        sky.draw()
        ground.draw()
        play.draw()
        exit.draw()
        janela.draw_text(str(fps_per_sec), 50, 50, 14)
        if mouse.is_button_pressed(1):
            if mouse.is_over_object(play):
                local = 1
        if mouse.is_button_pressed(1):
            if mouse.is_over_object(exit):
                janela.close()
        new_run = 1
    # se iniciar o jogo
    if local == 1:
        if test_character.get_coord()[0] >= 3335.5:
            test_character.set_HP(0)
        if new_run == 1:
            test_character.set_coord(100, 440)
            test_character.set_HP(2000)
            enemies[0].set_coord(200,442)
            enemies[1].set_coord(1500,442)
            enemies[2].set_coord(1800,442)
            enemies[3].set_coord(1870,442)
            enemies[4].set_coord(2000,442)
            for x in enemies:
                x.set_HP(100)
            new_run = 0
        # Stage_Draw_static  (Desenha o cenario mas nao seus objetos)
        if True:
            # Stage_POS (As posiçoes seguem o padrão: posição do pivo + posição desejada)
            floor.x = pivo.x
            floor_2.x = pivo.x + 2750
            stage_1_layer.x = pivo.x - 50
            stage_1_layer_2.x = pivo.x - 50
            wall_brick.x = pivo.x + 2200
            wall_brick_2.x = pivo.x + 2500
            ground.x = pivo.x + 2000
            castle_wall.x = pivo.x + 2750
            castle_wall_2.x = pivo.x + 3520
            castle_interior.x = pivo.x + 2750
            # Stage_DRAW
            sky.draw()
            stage_1_layer_2.draw()
            ground.draw()
            stage_1_layer.draw()
            wall_brick.draw()
            wall_brick_2.draw()
            castle_interior.draw()


            janela.draw_text(str(fps_per_sec), 50, 50, 14)
            #condiçoes de colisão
            if controlable_char.x==props[1].x:
                controlable_char.x = controlable_char.x-50


            # HUD
            if (True):
                 if (1800 <= test_character.get_HP() < 2000):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_90.png")
                 if (1500 <= test_character.get_HP() < 1800):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_83.png")
                 if (1300 <= test_character.get_HP() < 1500):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_75.png")
                 if (1140 <= test_character.get_HP() < 1300):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_65.png")
                 if (1000 <= test_character.get_HP() < 1140):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_57.png")
                 if (800 <= test_character.get_HP() < 1000):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_50.png")
                 if (660 <= test_character.get_HP() < 800):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_40.png")
                 if (500 <= test_character.get_HP() < 660):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_33.png")
                 if (340 <= test_character.get_HP() < 500):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_25.png")
                 if (180 <= test_character.get_HP() < 340):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_17.png")
                 if (40 <= test_character.get_HP() < 180):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_9.png")
                 if (2 <= test_character.get_HP() < 40):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_2.png")
                 if (test_character.get_HP() <= 0):
                     HP = Sprite("_assets/Hearts/Hearts/PNG/health_bar/health_bar_decoration_0.png")


        # Pivo_mov    (pivo move todo o cenario)
        if test_character.get_HP() >= 0:
            pivo.move_key_x(-1.5)
        if test_character.get_HP() <= 0:
            if timer_2 == 0:
                local = 0
            timer_2 -= 1
        #para o personagem não sair do cenário
        if test_character.get_coord()[0] <= 122.5:
            test_character.set_coord(122.5, test_character.get_coord()[1])
            pivo.x = -22.5
        # Animation Part

        # Props draw (Desenha os objetos)
        for n in range(len(props)):
            props[n].actual_coord()
            props[n].draw_assets()
        # Damage and animation for enemies and player
        # O metodo movements tambem executa .draw do seu respectivo objeto
        test_character.movements(teclado)
        for n in range(len(enemies)):
            enemies[n].interactions(test_character.get_interactions())
            enemies[n].movements(teclado)
            enemies[n].actual_coord()
            test_character.get_dmg_from(enemies[n].turn_dmg)
        # Damage in player
        HP.draw()
        floor.draw()
        floor_2.draw()
        castle_wall.draw()
        castle_wall_2.draw()
        print(test_character.get_coord())

       # Assets with collision

    #Update
    janela.update()

    # Fps_count
    fps_per_sec = int(1 / janela.delta_time())