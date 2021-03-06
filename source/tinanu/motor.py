# -*- coding: utf-8 -*-
# @author: Charles Tim Batista Garrocho
# @contact: ccharles.garrocho@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável por toda interação dos atores no jogo.
"""

import copy
import media
import pygame
import random
import settings
from atores import *
from pygame.locals import *


class JogadorXPStatus:
    """
    Esta classe representa a experiência do usuário
    """
    fonte   = None
    last_xp = -1
    fgcolor = None
    bgcolor = None
    imagem  = None
    
    def __init__( self, jogador, posicao=None, fonte=None, ptsize=30, fgcolor="0xffff00", bgcolor=None ):
        self.jogador = jogador
        self.fgcolor = pygame.color.Color( fgcolor )
        if bgcolor:
            self.bgcolor = pygame.color.Color( bgcolor )
        self.posicao = posicao or [ 0, 0 ]
        self.fonte   = pygame.font.Font( fonte, ptsize )

    def update( self, dt ):
        pass

    def draw( self, screen ):
        xp = self.jogador.get_XP()
        if self.last_xp != xp:
            self.last_xp = xp
            texto = "XP: % 4d" % xp
            if self.bgcolor:
                self.imagem = self.fonte.render( texto, True, self.fgcolor, self.bgcolor )
            else:                
                self.imagem = self.fonte.render( texto, True, self.fgcolor )
        screen.blit( self.imagem, self.posicao )


class JogadorVidaStatus:
    """
    Esta classe representa o contador de vidas do jogador
    """
    jogador    = None
    posicao    = None
    imagem     = None
    size_image = None
    spacing    = 5

    def __init__( self, jogador, image, posicao=None ):
        self.imagem     = image
        self.jogador    = jogador
        self.posicao    = posicao or [ 5, 5 ]
        self.size_image = self.imagem.get_size()

    def update( self, dt ):
        pass

    def draw( self, screen ):
        posicao = copy.copy( self.posicao )
        for i in range( self.jogador.get_vidas() ):
            posicao[ 0 ] += self.size_image[ 0 ] + self.spacing
            screen.blit( self.imagem, posicao )


class Game:
    screen      = None
    screen_size = None
    run         = True
    intervalo   = 0
    level       = 0
    lista       = None
    jogador     = None
    background  = None 
    
    def __init__( self, screen ):
        """
        Esta é a função que inicializa o pygame, define a resolução da tela,
        caption, e disabilitamos o mouse dentro desta.
        """
        atores = {}
        media.executar_musica("musica.ogg", 0.75)
        self.screen      = screen
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible( 0 )
        pygame.display.set_caption( 'TiNaNu - Tiro nas Nuvens' )
        self.carrega_dados()

    def carrega_dados( self ):
        """
        Lê as imagens e sons necessarios pelo jogo.
        """
        # imagens
        self.imagem_jogador      = pygame.image.load( media.carrega_imagem(settings.IMG_NAVE_JOGADOR) )
        self.imagem_inimigo      = pygame.image.load( media.carrega_imagem(settings.IMG_NAVE_INIMIGO) )
        self.imagem_tiro         = pygame.image.load( media.carrega_imagem(settings.IMG_TIRO_JOGADOR) )
        self.imagem_tiro_inimigo = pygame.image.load( media.carrega_imagem(settings.IMG_TIRO_INIMIGO) )
        self.imagem_fase_1       = pygame.image.load( media.carrega_imagem(settings.IMG_TILE_1) )
        self.imagem_fase_2       = pygame.image.load( media.carrega_imagem(settings.IMG_TILE_2) )
        self.imagem_fase_3       = pygame.image.load( media.carrega_imagem(settings.IMG_TILE_3) )
        self.imagem_fase_4       = pygame.image.load( media.carrega_imagem(settings.IMG_TILE_4) )
        self.imagem_fase_5       = pygame.image.load( media.carrega_imagem(settings.IMG_TILE_5) )
        self.imagem_vida         = pygame.image.load( media.carrega_imagem(settings.IMG_NAVE_STATUS) )

        # sons
        self.som_tiro     = media.obter_som('tiro.wav')
        self.som_explosao = media.obter_som('explosao.wav')

    def handle_events( self ):
        """
        Trata o evento e toma a ação necessária.
        """
        jogador = self.jogador

        for event in pygame.event.get():
            t = event.type
            if t in ( KEYDOWN, KEYUP ):
                k = event.key
        
            if t == QUIT:
                self.run = False

            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
                elif k == K_LCTRL or k == K_RCTRL:
                    self.intervalo = 0
                    self.som_tiro.play()
                    jogador.tiro( lista_tiros = self.lista[ "tiros" ], imagem = self.imagem_tiro )
                elif k == K_UP:
                    jogador.accel_top()
                elif k == K_DOWN:
                    jogador.accel_bottom()
                elif k == K_RIGHT:
                    jogador.accel_right()
                elif k == K_LEFT:
                    jogador.accel_left()
        
            elif t == KEYUP:
                if   k == K_DOWN:
                    jogador.accel_top()
                elif k == K_UP:
                    jogador.accel_bottom()
                elif k == K_LEFT:
                    jogador.accel_right()
                elif k == K_RIGHT:
                    jogador.accel_left()
        
            keys = pygame.key.get_pressed()
            if self.intervalo > 10:
                self.intervalo = 0
                if keys[ K_RCTRL ] or keys[ K_LCTRL ]:
                    self.som_tiro.play()
                    jogador.tiro( self.lista[ "tiros" ], self.imagem_tiro )        

    def atores_update( self, dt ):
        self.background.update( dt )
        for ator in self.lista.values():
            ator.update( dt )
        self.jogador_vida.update( dt )
        self.jogador_xp.update( dt )

    def atores_draw( self ):
        self.background.draw( self.screen )
        for ator in self.lista.values():
            ator.draw( self.screen )
        self.jogador_vida.draw( self.screen )
        self.jogador_xp.draw( self.screen )

    def ator_check_hit( self, ator, lista, acao ):
        if isinstance( ator, pygame.sprite.RenderPlain ):
            hitted = pygame.sprite.groupcollide( ator, lista, 1, 0 )
            for v in hitted.values():
                for o in v:
                    acao( o )
            return hitted

        elif isinstance( ator, pygame.sprite.Sprite ):
            if pygame.sprite.spritecollide( ator, lista, 1 ):
                acao()
            return ator.is_dead()

    def atores_act( self ):
        # Verifica se personagem foi atingido por um tiro
        self.ator_check_hit( self.jogador, self.lista[ "tiro_inimigo" ], self.jogador.do_hit )
        if self.jogador.is_dead():
            self.run = False
            return

        # Verifica se o personagem trombou em algum inimigo
        self.ator_check_hit( self.jogador, self.lista[ "inimigos" ], self.jogador.do_collision )
        if self.jogador.is_dead():
            self.run = False
            return

        # Verifica se o personagem atingiu algum alvo.
        hitted = self.ator_check_hit( self.lista[ "tiros" ], self.lista[ "inimigos" ], Inimigo.do_hit )
        
        # Aumenta a experiência baseado no número de acertos:
        self.jogador.set_XP( self.jogador.get_XP() + len( hitted ) )

    def modifica_level( self ):
        xp = self.jogador.get_XP()
        if xp > 5  and self.level == 0:
            self.background = Background( self.imagem_fase_2 )
            self.level = 1
            self.jogador.set_vidas( self.jogador.get_vidas() + 2 )
        elif xp > 10  and self.level == 1:
            self.background = Background( self.imagem_fase_3 )
            self.level = 2        
            self.jogador.set_vidas( self.jogador.get_vidas() + 4 )
        elif xp > 20  and self.level == 2:
            self.background = Background( self.imagem_fase_4 )
            self.level = 3      
            self.jogador.set_vidas( self.jogador.get_vidas() + 6 )
        elif xp > 30  and self.level == 3:
            self.background = Background( self.imagem_fase_5 )
            self.level = 4
            self.jogador.set_vidas( self.jogador.get_vidas() + 8 )

    def manage( self ):
        self.ticks += 1
        # Faz os inimigos atirarem aleatóriamente
        if self.ticks > random.randint( 20, 30 ):
            for inimigo in self.lista[ "inimigos" ].sprites():
                if random.randint( 0, 10 ) > 5:
                    inimigo.tiro( self.lista[ "tiro_inimigo" ], imagem = self.imagem_tiro_inimigo )
                    self.ticks = 0
        
        # criamos mais inimigos randomicamente para o jogo não ficar chato
        r = random.randint( 0, (self.level + 1) * 100 )
        bhvr = random.randint( 0, 2 )
        x = random.randint( 1, self.screen_size[ 0 ] / 20 )
        if ( r > ( 40 * len( self.lista[ "inimigos" ] ) ) ):
            inimigo = Inimigo( posicao = [ 0, 0 ], explosao = self.som_explosao, behaviour = bhvr, imagem = self.imagem_inimigo )
            size    = inimigo.get_size()
            inimigo.set_posicao( [ x * size[ 0 ], - size[ 1 ] ] )
            self.lista[ "inimigos" ].add( inimigo )

        # Verifica se modificou o level
        self.modifica_level()

    def loop( self ):
        """
        Laço principal
        """
        # Criamos o fundo
        self.background = Background( self.imagem_fase_1 )

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock          = pygame.time.Clock()
        dt             = 16
        self.ticks     = 0
        self.intervalo = 1

        posicao      = [ self.screen_size[ 0 ] / 2, self.screen_size[ 1 ] ]
        self.jogador = Jogador( posicao = posicao, explosao = self.som_explosao, vidas=10, imagem = self.imagem_jogador )

        self.lista = {
            "jogador"       : pygame.sprite.RenderPlain( self.jogador ),
            "inimigos"      : pygame.sprite.RenderPlain( Inimigo( posicao = [ 120, 0 ], explosao = self.som_explosao, imagem = self.imagem_inimigo ) ),
            "tiros"         : pygame.sprite.RenderPlain(),
            "tiro_inimigo"  : pygame.sprite.RenderPlain()
            }

        self.jogador_vida = JogadorVidaStatus( jogador = self.jogador, image = self.imagem_vida, posicao = [ 5, 5 ] )
        self.jogador_xp   = JogadorXPStatus( self.jogador, [ self.screen_size[ 0 ] - 100, 5 ], fgcolor="0xff0000" )

        # Loop principal do programa
        while self.run:
            clock.tick( 1000 / dt )
            self.intervalo += 1

            # Handle Input Events
            self.handle_events()

            # Atualiza Elementos
            self.atores_update( dt )

            # Faça os atores atuarem
            self.atores_act()

            # Faça a manutenção do jogo, como criar inimigos, etc.
            self.manage()
            
            # Desenhe os elementos do jogo.
            self.atores_draw()
            
            # Por fim atualize o screen do jogo.
            pygame.display.flip()