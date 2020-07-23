# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# 6

import re

from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress  #, VSlog, xbmc
 
SITE_IDENTIFIER = 'ocs'
SITE_NAME = 'TESTE OCS'
SITE_DESC = 'programmes OCS'

URL_MAIN='https://www.ocs.fr/'

MOVIE_MOVIES = (URL_MAIN + 'ajax/programs/search?categories[]=movie&keyword=&order=null&refresh=false&offset=0&limit=30', 'showMovies')

MOVIE_GENRES=(True, 'showMovieGenre')
MOVIE_NEWS=(URL_MAIN + 'ajax/programs/search?categories[]=movie&keyword=&order=desc-date&refresh=false&offset=0&limit=30', 'showMovies')
 
SERIE_SERIES=(URL_MAIN + 'ajax/programs/search?categories[]=serie&keyword=&order=null&refresh=false&offset=0&limit=30', 'showMovies')
SERIE_GENRES=(True, 'showSerieGenre')
SERIE_NEWS=(URL_MAIN + 'ajax/programs/search?categories[]=serie&keyword=&order=desc-date&refresh=false&offset=0&limit=30', 'showMovies')

URL_SEARCH = (URL_MAIN+ 'ajax/programs/search?keyword=', 'showMovies')#m000
SEARCH_ADD='&order=null&refresh=false&offset=0&limit=30'

def load():
    oGui = cGui()
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSerie', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIES[1], 'Films ( récement ajoutés )', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films ( Année de sortie )', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMenuSerie():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], ' Series ( récement ajoutés )', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries ( Année de sortie )', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMovieGenre():
    showGenres('movie') 

def showSerieGenre():
    showGenres('serie')

def showGenres(cat):
    oGui = cGui()

    #ex : https://www.ocs.fr/ajax/programs/search?categories[]=movie&genres[]=18&keyword=&order=null&refresh=false&offset=0&limit=30
    # &genres[]= id
    url1='https://www.ocs.fr/ajax/programs/search?categories[]='+cat
    url2='&keyword=&order=desc-date&refresh=false&offset=0&limit=30'

    liste = []
    liste.append(['Animation', url1 + '&genres[]=17]' + url2])
    liste.append(['Aventure', url1 + '&genres[]=19]' + url2])
    liste.append(['Classique', url1 + '&genres[]=18]' + url2])
    liste.append(['Comédie', url1 + '&genres[]=21]' + url2])
    liste.append(['Documentaire', url1 + '&genres[]=12]' + url2])
    liste.append(['Drame', url1 + '&genres[]=10]' + url2])
    liste.append(['Fantastique', url1 + '&genres[]=14]' + url2])
    liste.append(['Film documentaire', url1 + '&genres[]=13]' + url2])
    liste.append(['Horreur', url1 + '&genres[]=15]' + url2])
    liste.append(['Jeunesse', url1 + '&genres[]=16]' + url2])
    liste.append(['Policier', url1 + '&genres[]=20]' + url2])
    
    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch(): 
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText + SEARCH_ADD
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch = ''):
    oGui = cGui()
    # bGlobal_Search = False
    oInputParameterHandler = cInputParameterHandler()
    if sSearch:
        sUrl = sSearch 
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
    # if URL_SEARCH[0] in sSearch:
        # bGlobal_Search = True

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    
    #g1 url  g2  imag  g3 title   g4 desc
    sPattern = 'about=".([^"]*).+?background-image.+?url.([^)]*).+?<h3><span>([^<]*).+?description">([^<]*)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        #total = len(aResult[1])
        #progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            #progress_.VSupdate(progress_, total)
            #if progress_.iscanceled():
                #break
            
            siteUrl = URL_MAIN+str(aEntry[0])
            sTitle = str(aEntry[2])
            sDesc = str(aEntry[3])
            sThumb = str(aEntry[1])
            if  not 'https' in str(sThumb):
                sThumb=URL_MAIN[:-1]  +sThumb

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb )
            oGui.addMovie(SITE_IDENTIFIER, 'showDesc', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        #progress_.VSclose(progress_)

        if (len(aResult[1]) == 30 ):
            sNextPage,numberpage= Request_ForNextPage(sUrl)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant' + numberpage +'>>>[/COLOR]', oOutputParameterHandler)
    
    if not sSearch:
        oGui.setEndOfDirectory()

def Request_ForNextPage(url):
    addoffset=30
    data=url.split("&")
    newrequest=''
    for element in data:    
        selement=element #?
        if 'offset' in element :
            number = re.search('([0-9]+)$', element).group(1)
            inumber=int(number)+addoffset
            page=inumber/addoffset
            selement='offset='+ str(inumber)
        newrequest=newrequest+selement+'&' 
    return newrequest[:-1],str(page)

def showDesc():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    typems=''
    if '<div class="serie-category">' in sHtmlContent :
        #sdec  +Saison 1 - 2019
        sPattern = 'synopsis.*?<p>([^<]*).+?<h4>([^<]*)'
        typems='serie'

    if '<div class="film-category">' in sHtmlContent :
        sPattern = 'Synopsis.*?<p>([^<]*).+?Année<.span>([^<]*).+?Durée<.span>([^<]*)'
        typems='film'

    oParser = cParser() 
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):

        for aEntry in aResult[1]:
            sYear='----'
            sDesc=aEntry[0].replace('  ','')
            if typems=='serie':
                sYear= re.search('([0-9]+)$', aEntry[1]).group(1)
                
            if typems=='film':
                sYear= aEntry[1].replace(' ','')

            sDesc = ('[COLOR skyblue]%s[/COLOR][COLOR coral]%s[/COLOR] %s') % (sYear+'\r\n\r\n ' ,'SYNOPSIS : \r\n', sDesc)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'none')
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('searchtext', sTitle)
        oGui.addMovie('globalSearch', 'showSearch', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
    
    
