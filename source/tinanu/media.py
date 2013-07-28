# -*- coding: utf-8 -*-
# @author: Charles Tim Batista Garrocho
# @contact: ccharles.garrocho@gmail.com
# @copyright: (C) 2013 - 2013 Python Software Open Source

"""
Este é o módulo responsável por realizar o carregamento dos endereços de fontes, imagens e sons do jogo.
"""


import os
import pygame
from os.path import join as join_path


dados_py  = os.path.abspath(os.path.dirname(__file__))
dados_dir = os.path.normpath(join_path(dados_py, '..', 'media'))


endereco_arquivos = dict(
    fontes  = join_path(dados_dir, 'fontes'),
    imagens = join_path(dados_dir, 'imagens'),
    sons = join_path(dados_dir, 'sons'),
)


def endereco_arquivo(tipo, nome_arquivo):
    return join_path(endereco_arquivos[tipo], nome_arquivo)


def carrega(tipo, nome_arquivo, modo='rb'):
	return open(endereco_arquivo(tipo, nome_arquivo), modo)


def carrega_fonte(nome_arquivo):
    return endereco_arquivo('fontes', nome_arquivo)


def carrega_imagem(nome_arquivo):
	return endereco_arquivo('imagens', nome_arquivo)


def carrega_imagem_menu(nome_arquivo):
    nome_arquivo = carrega('imagens', nome_arquivo)
    try:
        image = pygame.image.load(nome_arquivo)
    except pygame.error:
        raise SystemExit, "Unable to load: " + nome_arquivo
    return image


def carrega_son(nome_arquivo):
    return carrega('sons', nome_arquivo)


def executar_musica(nome_arquivo, volume=0.5, loop=-1):
    nome_arquivo = carrega_son(nome_arquivo)
    try:
        pygame.mixer.music.load(nome_arquivo)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)
    except:
        raise SystemExit, "Unable to load: " + nome_arquivo


def parar_musica():
    pygame.mixer.music.stop()


def obter_som(nome_arquivo, volume=1.0):
    nome_arquivo = carrega_son(nome_arquivo)
    try:
        som = pygame.mixer.Sound(nome_arquivo)
        som.set_volume(volume)
    except:
        raise SystemExit, "Unable to load: " + nome_arquivo
    return som


def carregar_sprites_fatias(w, h, nome_arquivo):
    imagens = []
    nome_arquivo = carrega('imagens', nome_arquivo)
    mestre_w, mestre_h = master_image.get_size()
    colunas = mestre_w / w
    linhas = mestre_h / h
    for i in xrange (linhas):
        for j in xrange (colunas):
            pequeno_sprite = master_image.subsurface((j*w,i*h,w,h))
            imagens.append(pequeno_sprite)
    return imagens
