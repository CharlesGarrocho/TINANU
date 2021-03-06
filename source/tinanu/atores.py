# -*- coding: utf-8 -*-
# @author: Charles Tim Batista Garrocho
# @contact: ccharles.garrocho@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável pelos atores do jogo, como background, jogador, inimigos, etc.
"""

import pygame
import settings
from math import ceil
from pygame.locals import *


class Background:
    """
    Esta classe representa o ator "Fundo" do jogo.
    """
    image = None

    def __init__( self, image ):
        self.isize  = image.get_size()
        self.pos    = [ 0, -1 * self.isize[ 1 ] ]
        screen      = pygame.display.get_surface()
        screen_size = screen.get_size()

        largura = ( ceil( float( screen_size[ 0 ] ) / self.isize[ 0 ] ) + 1 ) * self.isize[ 0 ]
        altura  = ( ceil( float( screen_size[ 1 ] ) / self.isize[ 1 ] ) + 1 ) * self.isize[ 1 ]

        back = pygame.Surface( ( largura, altura ) )
        
        for i in range( ( back.get_size()[ 0 ] / self.isize[ 0 ] ) ):
            for j in range( ( back.get_size()[ 1 ] / self.isize[ 1 ] ) ):
                back.blit( image, ( i * self.isize[ 0 ], j * self.isize[ 1 ] ) )

        self.image = back

    def update( self, dt ):
        self.pos[ 1 ] += 1
        if ( self.pos[ 1 ] > 0 ):
            self.pos[ 1 ] -= self.isize[ 1 ]

    def draw( self, screen ):
        screen.blit( self.image, self.pos )


class GameObject( pygame.sprite.Sprite ):
    """
    Esta é a classe básica de todos os objetos do jogo.
    """

    def __init__( self, imagem, posicao, velocidade=None ):
        pygame.sprite.Sprite.__init__( self )
        self.image = imagem

        self.rect  = self.image.get_rect()
        screen     = pygame.display.get_surface()
        self.area  = screen.get_rect()
        
        self.set_posicao( posicao )
        self.set_velocidade( velocidade or ( 0, 2 ) )

    def update( self, dt ):
        velocidade_mov = ( self.velocidade[ 0 ] * dt / 16, self.velocidade[ 1 ] * dt / 16 )
        self.rect  = self.rect.move( velocidade_mov )
        if self.rect.left > self.area.right or self.rect.top > self.area.bottom or self.rect.right < 0:
            self.kill()
        if self.rect.bottom < -40:
            self.kill()

    def get_velocidade( self ):
        return self.velocidade

    def set_velocidade( self, velocidade ):
        self.velocidade = velocidade

    def get_posicao( self ):
        return ( self.rect.center[ 0 ], self.rect.bottom )

    def set_posicao( self, posicao ):
        self.rect.center = ( posicao[ 0 ], posicao[ 1 ] )

    def get_size( self ):
        return self.image.get_size()


class Tiro( GameObject ):
    def __init__( self, posicao, velocidade=None, imagem=None, lista=None ):
        GameObject.__init__( self, imagem, posicao, velocidade )
        if lista != None:
            self.add( lista )


class Nave( GameObject ):

    vidas = None

    def __init__( self, posicao, explosao, vidas=0, velocidade=[ 0, 0 ], imagem=None ):
        self.acceleration = [ 3, 3 ]
        GameObject.__init__( self, imagem, posicao, velocidade )
        self.set_vidas( vidas )
        self.explosao = explosao

    def get_vidas( self ):
        return self.vidas

    def set_vidas( self, vidas ):
        self.vidas = vidas

    def tiro( self, lista_tiros, imagem=None ):
        s = list( self.get_velocidade() )
        s[ 1 ] *= 2
        Tiro( self.get_posicao(), s, imagem, lista_tiros )

    def do_hit( self ):
        if self.get_vidas() == 0:
            self.kill()
            self.explosao.play()
        else:
            self.set_vidas( self.get_vidas() - 1 )

    def do_collision( self ):
        if self.get_vidas() == 0:
            self.kill()
        else:
            self.set_vidas( self.get_vidas() - 1 )

    def is_dead( self ):
        return self.get_vidas() == 0

    def accel_top( self ):
        velocidade = self.get_velocidade()
        self.set_velocidade( ( velocidade[ 0 ], velocidade[ 1 ] - self.acceleration[ 1 ] ) )

    def accel_bottom( self ):
        velocidade = self.get_velocidade()
        self.set_velocidade( ( velocidade[ 0 ], velocidade[ 1 ] + self.acceleration[ 1 ] ) )

    def accel_left( self ):        
        velocidade = self.get_velocidade()
        self.set_velocidade( ( velocidade[ 0 ] - self.acceleration[ 0 ], velocidade[ 1 ] ) )

    def accel_right( self ):
        velocidade = self.get_velocidade()
        self.set_velocidade( ( velocidade[ 0 ] + self.acceleration[ 0 ], velocidade[ 1 ] ) )


class Inimigo( Nave ):
    def __init__( self, posicao, explosao, vidas=0, velocidade=None, behaviour=0, imagem=None):
        if   behaviour == 0: # Inimigo normal, desce reto
            velocidade = (  0, 3 )
        elif behaviour == 1: # Inimigo que desce da esquerda pra direita
            velocidade = (  2, 3 )
        elif behaviour == 2: # Inimigo que desce da direita pra esquerda
            velocidade = ( -2, 3 )
        Nave.__init__( self, posicao, explosao, vidas, velocidade, imagem )


class Jogador( Nave ):
    """
    A classe Jogador é uma classe derivada da classe GameObject.
    """

    def __init__( self, posicao, explosao, vidas=10, imagem=None ):
        Nave.__init__( self, posicao, explosao, vidas, [ 0, 0 ], imagem )
        self.set_XP( 0 )

    def update( self, dt ):
        velocidade_mov = ( self.velocidade[ 0 ] * dt / 16, self.velocidade[ 1 ] * dt / 16)
        self.rect  = self.rect.move( velocidade_mov )
        
        if ( self.rect.right > self.area.right ):
            self.rect.right = self.area.right
            
        elif ( self.rect.left < 0 ):
            self.rect.left = 0
            
        if ( self.rect.bottom > self.area.bottom ):
            self.rect.bottom = self.area.bottom
            
        elif ( self.rect.top < 0 ):
            self.rect.top = 0
    
    def get_posicao( self ):
        return ( self.rect.center[ 0 ], self.rect.top )
    
    def get_XP( self ):
        return self.XP

    def set_XP( self, XP ):
        self.XP = XP

    def tiro( self, lista_tiros, imagem=None ):
        l = 1
        if self.XP > 10: l = 3
        if self.XP > 50: l = 5
        
        posicao     = self.get_posicao()
        velocidades = self.get_velocidade_tiro( l )
        for velocidade in velocidades:
            Tiro( posicao, velocidade, imagem, lista_tiros )

    def get_velocidade_tiro( self, municao ):
        velocidades = []
        if municao <= 0:
            return velocidades
        
        if municao == 1:
            velocidades += [ (  0, -5 ) ]
            
        if municao > 1 and municao <= 3:
            velocidades += [ (  0, -5 ) ]
            velocidades += [ ( -2, -3 ) ]
            velocidades += [ (  2, -3 ) ]
            
        if municao > 3 and municao <= 5:
            velocidades += [ (  0, -5 ) ]
            velocidades += [ ( -2, -3 ) ]
            velocidades += [ (  2, -3 ) ]
            velocidades += [ ( -4, -2 ) ]
            velocidades += [ (  4, -2 ) ]

        return velocidades