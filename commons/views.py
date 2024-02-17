

from django.shortcuts import render
from django.apps import apps

from django.utils.safestring import mark_safe

from main.models import topics
from main.models import yakks
from main.models import accounts


import json
import re

import numpy as np
import cv2
import base64

import os
os.environ['path']                      += r';C:\Program Files\UniConvertor-2.0rc5\dlls'
#MACOS os.environ['DYLD_LIBRARY_PATH']  = "/opt/homebrew/lib" + ":" + os.environ.get('DYLD_LIBRARY_PATH', '')
import cairo
import cairosvg

ImgPath1 = 'A:\\_\\triptych\\virtual\\triptych\\commons\\static\\vAccessories\\'
ImgPath2 = 'A:\\_\\triptych\\virtual\\triptych\\commons\\static\\vDB\\'
#ImgPathMAC = ''



def createTopic ( Request ):

    Python      = json.loads( Request.body )

    XTopicCategory  = Python['NewTopicCategory']
    XTopicTitle     = Python['NewTopicTitle']
    XTopicStatus    = Python['NewTopicStatus']
    XFirstYakk      = Python['FirstYakk']
    TopicImage = getTopicImage( '', XTopicCategory, XTopicStatus )
    return render(Request, 'dummy.html', {"dummy": 'dummy'} )




def getTopics ( Request ):
    Python      = json.loads(Request.body)
    XTopicNr    = int( Python['TopicNr'] )
    QS          = topics.objects.filter( TopicChosenCategory = XTopicNr)
    print('QS is ', QS)
    Context = {
            'TopicsByCategory'     : list( QS )
    }
    return render(Request, 'topics.html', Context )

def createYakk ( Request ):

    Python      = json.loads( Request.body )
    yakkdict = {
            'YakkNr'            : 999,
            'Yakk'              : Python['Yakk'],
            'YakkChosenCategory': Python['Category'],
            'YakkTopicNr'       : Python['TopicNr'],
            'YakkedBy'          : Python['YakkedBy']
    }
    NewYakk  = yakks( **yakkdict )
    NewYakk.save()
    return render(Request, 'dummy.html', {"dummy": 'dummy'} )


def getYakks( Request ):
    Python      = json.loads(Request.body)
    XTopicNr    = int( Python['TopicNr'] )
    QS          = yakks.objects.filter( YakkTopicNr = XTopicNr)
    #Filters                 = {}
    #Filters['YakkTopicNr']  = XTopicNr
    #QS                      = Table.objects.filter(**Filters)

    HTML     = ''
    Likes    = '<img width="3.0%" style="opacity:0.4" src=' + mark_safe( 'data:image/png;base64,' + str( convert2Base64( cv2.imread( ImgPath1 + 'like.png',    -1) ) )[2:-1]) + '>'
    Dislikes = '<img width="3.0%" style="opacity:0.4" src=' + mark_safe( 'data:image/png;base64,' + str( convert2Base64( cv2.imread( ImgPath1 + 'dislike.png', -1) ) )[2:-1]) + '>'

    from datetime import datetime
    for Yakk in QS:
        TimeStamp = Yakk.YakkedOnAt.strftime( '<span class="time">&nbsp; &nbsp; &nbsp; %H:%M &nbsp; <font size=-2>%D</font></span>') + '<br>'
        YakkText  = '<font style="line-height:0.8" size=+3>' + Yakk.Yakk[0:1] + '</font>' + Yakk.Yakk[1:]
        #YakkRef   = re.search(('(?<=abc)def', 'abcdef'))
        YakkText = YakkText.lower()
        YakkText  = re.sub(r'\@(.*?)\@',       r'<span class="topic">\1</span>', YakkText)                                                           # format topic references
        YakkText  = re.sub(r'see yakk#(\d*)#', r'<font size=-2>see </font><span class="yakk">yakk</span><sup class="yakksup">\1</sup> ', YakkText)   # format see yakk references
        YakkText  = re.sub(r'yakk#(\d*)#',     r'<span class="yakk">yakk</span><sup class="yakksup">\1</sup> ', YakkText)                            # format yakk references
        NickName  = (accounts.objects.filter( AccountNr = Yakk.YakkedBy ).values()[0]).get('AccountNickname')
        Profile   = '<img width="6%" style="opacity:0.9" src=' + mark_safe('data:image/png;base64,' + str( convert2Base64( cv2.imread( ImgPath2 + 'a' + str(Yakk.YakkedBy) + '.png', -1) ) )[2:-1]) + '>'
        HTML     += TimeStamp
        HTML     += YakkText + '<div style="line-height:0.5em">&nbsp;</div>'                                                             # spacing
        HTML     += '<div style="text-align:right"> <font class="like">' + Likes +  '&nbsp;' + str(Yakk.YakkQtyOfLikes) + '</font> &nbsp;&thinsp; <font class="like"> ' + Dislikes + '&nbsp;' + str(Yakk.YakkQtyOfDislikes) + '</font>' + '&nbsp; &nbsp; '
        HTML     += '<a href="javascript:getAccount(' + str(Yakk.YakkedBy) + ')"><font style="font-size:0.8em">' + NickName + '</font>&nbsp; ' +  Profile + '</a> </div><br>'      # nickname + profile pic
        TopicCategory = Yakk.YakkChosenCategory
    SVGColor = ''
    TopicImageFormula   = ''
    TopicImageCategory  = 0
    TopicStatus         = (topics.objects.filter(TopicNr=Yakk.YakkTopicNr).values()[0]).get('TopicStatus')
    if ( TopicStatus == 0 ):
        TopicImage          = getTopicImage( TopicImageFormula, TopicCategory, TopicStatus )
    elif ( TopicStatus == 2 or TopicStatus == 3 ):
        TopicImage          = getOtherImages( TopicStatus )
    else:
        if ( TopicStatus == 4 ):    # non-profit
            SVGColor   = 'rgb(200, 100, 240, 0.5)'
            TopicImage = getOtherImages( TopicStatus )
        elif ( TopicStatus == 5 ):  # profit
            SVGColor   = 'rgb(100, 240, 140, 0.7)'
            TopicImage = getOtherImages( TopicStatus )
        elif ( TopicStatus == 6 ):  # blast
            SVGColor   = 'rgb( 220, 220, 60, 0.9)'
            TopicImage = getOtherImages( TopicStatus )

    TopicTitle          = (topics.objects.filter( TopicNr = Yakk.YakkTopicNr ).values()[0]).get('TopicText')
    #print(Yakks[0])
    # return HttpResponse(SVGContent, content_type='image/svg+xml')
    #SVGColor = 'rgb(200, 100, 240, 0.5)'
    Context = {
        'Likes'      : mark_safe( re.sub('3.0%', '30%', Likes)  ),
        'Dislikes'   : mark_safe( re.sub('3.0%', '30%', Dislikes)  ),
        'TopicImage' : mark_safe( TopicImage ),
        'TopicTitle' : mark_safe( TopicTitle ),
        'FirstYakk'  : mark_safe( (yakks.objects.filter( YakkNr = 1 ).values()[0]).get('Yakk')[:200] ),
        'Yakks'      : mark_safe( HTML ),
        'SVGColor'   : mark_safe(SVGColor)
    }
    #print( SVGContent )
    return render(Request, 'yakks.html', Context )



def createAccount( Request ):
    a = 'dummy'

def getAccount( Request ):

    Python      = json.loads(Request.body)
    XAccountNr  = int( Python['AccountNr'] )
    QS          = accounts.objects.filter( AccountNr = XAccountNr )
    #Filters                 = {}
    #Filters['YakkTopicNr']  = XTopicNr
    #QS                      = Table.objects.filter(**Filters)

    HTML     = ''
    Likes    = '<img width="3.0%" style="opacity:0.4" src=' + mark_safe( 'data:image/png;base64,' + str( convert2Base64( cv2.imread(ImgPath1 + 'like.png',    -1) ) )[2:-1]) + '>'
    Dislikes = '<img width="3.0%" style="opacity:0.4" src=' + mark_safe( 'data:image/png;base64,' + str( convert2Base64( cv2.imread(ImgPath1 + 'dislike.png', -1) ) )[2:-1]) + '>'

    for Account in QS:
        TopicsByCat  = str(Account.AccountQtyOfTopics).split(',')
        YakksByCat   = str(Account.AccountQtyOfYakks).split(',')
        AccountImage = '<img width="50%" style="opacity:0.9" src=' + mark_safe( 'data:image/png;base64,' + str(convert2Base64(cv2.imread( ImgPath2 + 'a' + str(Account.AccountNr) + '.png', -1 )))[2:-1]) + '>'
        Nickname     = str(Account.AccountNickname)
        GPA          = str(Account.AccountGPA)

    Context = {
        'AccountImage'  : mark_safe( AccountImage ),
        'Nickname'      : Nickname,
        'GPA'           : GPA,
        'TopicsByCat'   : TopicsByCat,
        'YakksByCat'    : YakksByCat
    }
    return render(Request, 'accounts.html', Context )

def getOtherImages( TopicStatus ):
    if ( TopicStatus == 2 ):
        return mark_safe('data:image/png;base64,' + str( convert2Base64( cv2.imread( ImgPath1 + 'sensitivized.png', -1)) )[2:])  # [2:] eliminates the leading b'
    elif ( TopicStatus == 3 ):
        return mark_safe('data:image/png;base64,' + str( convert2Base64(cv2.imread(ImgPath1 + 'plain.png', -1)))[2:])
    elif ( TopicStatus == 4 or TopicStatus == 5 or TopicStatus == 6 ):
        return mark_safe('data:image/png;base64,' + str(convert2Base64(cv2.imread(ImgPath1 + 'Status' + str(TopicStatus) + '.png', -1)))[2:])




def getTopicRecord( TopicNr ):

    #... get from Web2 database
    # Key : TopicNr     --> returns TopicCategory, TopicTitle, TopicStatus, TopicImageFormula, FirstYakksPage
    TopicCategory       = 0
    TopicTitle          = ''
    TopicStatus         = 0  # 0:free;  1:auction;  2:owned  3:sensitized
    TopicImageFormula   = ''
    FirstYakk           = "nobody knows anything about eleanor rigby; she picks up the rice in the church"
    Yakks               = []
    if ( TopicNr == 101 ):
        TopicCategory     = 7
        TopicTitle        = "nobody knows anything about eleanor rigby; she picks up the rice in the church"
        TopicStatus       = 3   # 0:free;  1:auction;  2:owned  3:sensitized
        TopicImageFormula = ''
        FirstYakk = 'dadadada asdasd adasdasa'
        Yakks             = ['<font size=+3>k</font>now that once upon a time, the bight and shiny future seemed really <span class="blue">bright</span>...!UP! once upon a time, the future seemed really <span class="blue">bright</span>...!UP!', 'twice upon two times...1DOWN!' ]
    elif ( TopicNr == 102 ):
        TopicCategory     = 7
        TopicTitle        = "why do birds sing? anybody, any idea?"
        TopicStatus       = 2   # 0:free;  1:auction;  2:owned  3:sensitized
        TopicImageFormula = '2*2*225,226,228*141,102,197^5*3*225,226,228*231,206,161^5*3*225,226,228*225,226,228^8*8*106,129,171*231,206,161^6*4*231,206,161*216,0,0^0*1*231,206,161*141,102,197^7*7*106,129,171*225,226,228^1*1*106,129,171*216,0,0^6*4*231,206,161*231,206,161^7*7*225,226,228*225,226,228^0*1*231,206,161*106,129,171^2*2*216,0,0*216,0,0^6*4*225,226,228*231,206,161^2*2*172,225,221*106,129,171^5*3*231,206,161*216,0,0^3*3*141,102,197*216,0,0^0*1*106,129,171*225,226,228^4*2*172,225,221*231,206,161^1*1*141,102,197*172,225,221^5*3*231,206,161*141,102,197^8*8*216,0,0*141,102,197^1*1*172,225,221*106,129,171^0*1*141,102,197*216,0,0^5*3*216,0,0*106,129,171^1*1*231,206,161*225,226,228^7*7*172,225,221*216,0,0^0*1*216,0,0*172,225,221^0*1*225,226,228*231,206,161^8*8*172,225,221*141,102,197^3*3*231,206,161*231,206,161^7*7*225,226,228*216,0,0^2*2*141,102,197*106,129,171^2*2*225,226,228*231,206,161^3*3*106,129,171*106,129,171^0*1*106,129,171*225,226,228^7*7*141,102,197*106,129,171^8*8*106,129,171*141,102,197^7*7*141,102,197*172,225,221^4*2*231,206,161*216,0,0^3*3*231,206,161*216,0,0^6*4*106,129,171*216,0,0^2*2*216,0,0*141,102,197^3*3*141,102,197*106,129,171^8*8*106,129,171*216,0,0^6*4*225,226,228*216,0,0^5*3*172,225,221*231,206,161^2*2*231,206,161*172,225,221^6*4*172,225,221*106,129,171^7*7*225,226,228*106,129,171^3*3*141,102,197*231,206,161^6*4*106,129,171*216,0,0^2*2*216,0,0*216,0,0^2*2*172,225,221*106,129,171^3*3*216,0,0*225,226,228^4*2*216,0,0*225,226,228^3*3*225,226,228*216,0,0^8*8*225,226,228*172,225,221^8*8*225,226,228*172,225,221^4*2*106,129,171*216,0,0^4*2*141,102,197*231,206,161^6*4*225,226,228*106,129,171^3*3*172,225,221*231,206,161^6*4*106,129,171*216,0,0^0*1*106,129,171*106,129,171^1*1*106,129,171*231,206,161^1*1*172,225,221*106,129,171^3*3*141,102,197*172,225,221^0*1*106,129,171*225,226,228^7*7*172,225,221*231,206,161^1*1*216,0,0*216,0,0^0*1*106,129,171*231,206,161^7*7*106,129,171*225,226,228^7*7*225,226,228*172,225,221^5*3*231,206,161*172,225,221^2*2*216,0,0*172,225,221^0*1*231,206,161*106,129,171^7*7*231,206,161*141,102,197^4*2*141,102,197*231,206,161^5*3*106,129,171*231,206,161^0*1*141,102,197*231,206,161^3*3*106,129,171*225,226,228^3*3*216,0,0*141,102,197^4*2*106,129,171*225,226,228^2*2*141,102,197*216,0,0^3*3*172,225,221*172,225,221^0*1*106,129,171*231,206,161^4*2*106,129,171*141,102,197^3*3*141,102,197*225,226,228^2*2*141,102,197*231,206,161^4*2*216,0,0*225,226,228^6*4*141,102,197*231,206,161^2*2*141,102,197*231,206,161^6*4*172,225,221*172,225,221^3*3*172,225,221*225,226,228^7*7*216,0,0*231,206,161^7*7*141,102,197*141,102,197^5*3*106,129,171*141,102,197^8*8*106,129,171*231,206,161^2*2*172,225,221*106,129,171^3*3*106,129,171*231,206,161^4*2*141,102,197*141,102,197^4*2*141,102,197*141,102,197^6*4*231,206,161*231,206,161^2*2*216,0,0*172,225,221^2*2*216,0,0*216,0,0^7*7*216,0,0*172,225,221^6*4*106,129,171*106,129,171^2*2*231,206,161*225,226,228^3*3*231,206,161*216,0,0^7*7*172,225,221*231,206,161^1*1*225,226,228*106,129,171^5*3*216,0,0*172,225,221^7*7*225,226,228*172,225,221^1*1*225,226,228*225,226,228^5*3*141,102,197*231,206,161^6*4*216,0,0*225,226,228^6*4*225,226,228*106,129,171'
        FirstYakk         = 'dadadada asdasd adasdasa the Webb space telescope doe not have anything to do with this yakk, however, one might conjue a distant relatioship between all the lonely people and '
        Yakks             = ['once upon a time, the future seemed really sunny shiny bright...!UP!', 'twice upon two times...1DOWN!' ]

    if ( TopicStatus == 2 ):
        print("BUTTERFLY")
        Sensitized = cv2.imread(ImgPath1 + 'sensitized.png', -1).astype(np.float32)
        TopicImage = mark_safe('data:image/png;base64,' + str(convert2Base64( Sensitized ))[2:])  # [2:] eliminates the leading b'
        return [TopicNr, TopicCategory, TopicTitle, TopicStatus, TopicImage, FirstYakk, Yakks]
    else:
        TopicImage = getTopicImage( TopicImageFormula,TopicCategory , TopicStatus )
        return [ TopicNr, TopicCategory, TopicTitle, TopicStatus, TopicImage, FirstYakk, Yakks ]



def getTopicImage( NFTFormula, TopicCategory, TopicStatus ):

    GivenFormula     = NFTFormula
    GivenBlockData   = []
    GivenBlockData   = GivenFormula.split('^')
    NewFormula       = ''
    Flag             = 1  # 0: from math.random, 1:from file
    if ( NFTFormula == '' ):
        Flag = 0
    isEmitDiskImages = False

    ToileSize   = 25  # in units
    Unit        = 16  # in pixels
    cthColorSet = 0
    Colors      = [  [ 'rgb(216, 0, 0)', 'rgb(141, 102, 197)', 'rgb(172, 225, 221)','rgb(106, 129, 171)', 'rgb(231, 206, 161)', 'rgb(225, 226, 228)' ],
                    [ 'rgb(216, 168, 0)','rgb(41, 102, 197)', 'rgb(172, 25, 21)', 'rgb(6, 29, 71)', 'rgb(231, 206, 61)', 'rgb(225, 226, 228)' ],
                    [ 'rgb(249, 65, 68)', 'rgb(243, 114, 44)', 'rgb(248, 150, 30)', 'rgb(249, 199, 79)', 'rgb(144, 190, 109)', 'rgb(67, 170, 139)', 'rgb(87, 117, 144)', 'rgb(16, 0, 0)' ],
                    [ 'rgb(45, 0, 247)','rgb(106, 0, 244)', 'rgb(137, 0, 242)', 'rgb(188, 0, 221)', 'rgb(229, 0, 164)', 'rgb(242, 0, 137)', 'rgb(255, 182, 0)', 'rgb(0, 0, 0)', 'rgb(0, 0, 200)' ],
                    [ 'rgb(255, 173, 173)','rgb(255, 214, 165)', 'rgb(253, 255, 182)', 'rgb(202, 255, 191)', 'rgb(155, 246, 255)', 'rgb(160, 196, 255)', 'rgb(30, 20, 30)','rgb(20, 30, 30)' ],
                    [ 'rgb(10, 210, 255)', 'rgb(41, 98, 255)', 'rgb(149, 0, 255)', 'rgb(255, 0, 89)', 'rgb(255, 140, 0)', 'rgb(255, 140, 0)', 'rgb(180, 230, 0)', 'rgb(15, 255, 219)', 'rgb(0, 0, 0)' ],
                    [ 'rgb(55, 114, 255)','rgb(240, 56, 255)', 'rgb(239, 112, 157)', 'rgb(226, 189, 112)','rgb(112, 228, 239)', 'rgb(94, 252, 141)', 'rgb(142, 249, 243)', 'rgb(230, 230, 230)' ] ]
    SVGContent = f'<svg id="SVG" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" style="width:{ ToileSize * Unit }px; height:{ ToileSize * Unit }px; background:#cfc;">'

    def assignRandomColor():
        import random
        return random.choice( Colors[ cthColorSet ] )

    def createRandomBlockSize():
        import random
        nonlocal NewFormula
        Size    = random.randint(0,8)
        Width   = Size
        Height  = 0
        if Size == 6:
            Height = 4
        elif Size == 5:
            Height = 3
        elif Size == 4:
            Height = 2
        elif Size in [1, 0]:
            Height = 1
        else:
            Height = Width
        NewFormula += str( Width ) + '*' + str( Height ) + '*'
        return Width, Height

    def createDefs( GradientID, cx, cy, r, Offset1, StopColor1, Offset2, StopColor2):
        return (
            f'<defs>'
            f'<radialGradient id="{ GradientID }" cx="{ cx }" cy="{ cy }" r="{ r }">'
            f'<stop offset="{ Offset1 }" stop-color="{ StopColor1 }" />'
            f'<stop offset="{ Offset2 }" stop-color="{ StopColor2 }" />'
            f'</radialGradient>'
            f'</defs>'
        )

    nthBlock    = 0
    nthGradient = 0

    def createNextBlock():
        nonlocal NewFormula
        if Flag == 0:
            Width, Height = createRandomBlockSize()
            Color         = assignRandomColor().replace(' ','')
            Color1        = assignRandomColor().replace(' ','')
            NewFormula   += Color1[4:].replace(')','') + '*'
            Color2        = assignRandomColor().replace(' ','')
            NewFormula   += Color2[4:].replace(')','') + '^'
        else:
            nonlocal nthBlock
            gbWidth, gbHeight, gbColor1, gbColor2 = GivenBlockData[ nthBlock ].split('*')
            nthBlock  += 1
            Width       = int( gbWidth )
            Height      = int( gbHeight )
            Color1      = 'rgb(' + gbColor1 + ')'
            Color2      = 'rgb(' + gbColor2 + ')'
        nonlocal nthGradient
        nthGradient += 1
        Defs         = createDefs(f'RG{ nthGradient }', '0.50', '0.25', '0.95', '0%', Color1, '100%', Color2 )
        Block        = f'<rect x="0" y="0" width="{ Width * Unit}" height="{ Height * Unit }" fill="url(#RG{ nthGradient })" />'
        return f'{ Defs }{ Block }', Width, Height

    def redeployBlock( DefsBlock, NewAccumulatedX, NewAccumulatedY, NewWidth, NewHeight ):
        nonlocal SVGContent
        DefsBlock   = re.sub('x="\d*"',      f'x="{ NewAccumulatedX * Unit }"', DefsBlock )
        DefsBlock   = re.sub('y="\d*"',      f'y="{ ( NewAccumulatedY * Unit ) }"', DefsBlock )
        DefsBlock   = re.sub('width="\d*"',  f'width="{ str( NewWidth * Unit ) }"', DefsBlock )
        DefsBlock   = re.sub('height="\d*"', f'height="{ str( NewHeight * Unit ) }"', DefsBlock )
        SVGContent += f'{ DefsBlock }'

    #... generate and deploy SVG blocks
    AccumulatedX = 0
    AccumulatedY = 0

    for i in range(0,60,1):

        DefsBlock, Width, Height = createNextBlock()
        redeployBlock( DefsBlock, AccumulatedX, AccumulatedY, Width, Height )
        FixedColumnWidth         = Width
        AccumulatedX            += FixedColumnWidth
        AccumulatedY            += Height
        isNewRow                 = True

        while AccumulatedY <= ToileSize:
            if ( nthBlock > len(GivenBlockData)-1 ):
                return
            AccumulatedX              -= FixedColumnWidth
            DefsBlock, Width, Height   = createNextBlock()
            if Width > FixedColumnWidth:
                Width = FixedColumnWidth
            redeployBlock( DefsBlock, AccumulatedX, AccumulatedY, Width, Height )
            isNewRow                   = False
            AccumulatedX              += Width
            AccumulatedRemainingSpace  = FixedColumnWidth - Width
            FixedRowHeight             = Height

            while isNewRow == False:
                DefsBlock, Width, Height = createNextBlock()
                if Width > AccumulatedRemainingSpace:
                    Width = AccumulatedRemainingSpace
                if Height != FixedRowHeight:
                    Height = FixedRowHeight
                redeployBlock( DefsBlock, AccumulatedX, AccumulatedY, Width, Height )
                AccumulatedX                += Width
                AccumulatedRemainingSpace   -= Width
                if AccumulatedRemainingSpace == 0:
                    AccumulatedY += FixedRowHeight
                    isNewRow = True

        AccumulatedY = 0
        if AccumulatedX >= ToileSize:
            break
    SVGContent     += '</svg>'
    SmallSVGContent = resizeSVG( SVGContent, 52, 52 )

    print( NewFormula )
    #'''
    f = open( ImgPath1 + "beril.svg", 'w')       # w: overwrite, a: append       print('...some text...', file=f)
    f.write( SVGContent )
    f.close()
    #'''
    cairosvg.svg2png( bytestring=SVGContent, write_to = ImgPath1 + 'mondrian400.png' )
    PNG = cairosvg.svg2png( bytestring=SVGContent )

    MergedSaturatedImg = servermergeImages("mondrian400.png", 1, cthColorSet )
    #servermergeImages("mondrian400.png", 1, cthColorSet )
    #return SmallSVGContent
    return MergedSaturatedImg


def servermergeImages( Mondie, SaveMode, cthColorSet ):

    ToBeClipped  = cv2.imread( ImgPath1 + Mondie, -1 ).astype(np.float64)                    # size:3
    ToBeClipped  = np.dstack(( ToBeClipped, np.zeros( ToBeClipped.shape[:-1])))              # size:4
    Background   = cv2.imread( ImgPath1 + 'logox.png', -1 ).astype(np.float64)
    Mask         = cv2.imread(ImgPath1 + 'mask.png', -1 ).astype(np.float64)
    Mask0        = cv2.imread(ImgPath1 + 'mask.png', -1 ).astype(np.float64)

    Merge = applyTransparencyMask( ToBeClipped, Background, Mask )

    Saturation = [ 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7 ]
    if SaveMode == 1:

        SaturationAdjustedImg = changeSaturation( Merge, Saturation [ cthColorSet ] )
        #print('SaturationAdjustedImg shape ', SaturationAdjustedImg.shape)
        #SaturationAdjustedImg = np.dstack(( SaturationAdjustedImg, np.zeros(SaturationAdjustedImg.shape[:-1])))  # size:4
        print('SaturationAdjustedImg shape ', SaturationAdjustedImg.shape)
        #Merge2 = applyTransparencyMask2( SaturationAdjustedImg, Mask0 )


        '''
        maskx = ( Merge[:, :, 0:3] != [0, 0, 0]).any(2)
        SaturationAdjustedImg = cv2.cvtColor( SaturationAdjustedImg, cv2.COLOR_BGR2RGB )
        SaturationAdjustedImg = cv2.cvtColor( SaturationAdjustedImg, cv2.COLOR_RGB2RGBA).astype(np.float64)
        '''

        #######Img9 = cv2.multiply( InvMask, SaturationAdjustedImg ).astype(np.float64) / 255.0
        #######print('SaturationAdjustedImg shape ', Img9.shape)
        #               SaturationAdjustedImg = np.dstack((SaturationAdjustedImg, np.zeros(SaturationAdjustedImg.shape[:-1])))
        #... create the image with alpha channel
        ######img_rgba = cv2.cvtColor( img_rgba, cv2.COLOR_RGB2RGBA )
        #... mask: elements are true any of the pixel value is 0
        #maskx = ( SaturationAdjustedImg[:, :, 0:3] != [0, 0, 0]).any(2)
        #... assign the mask to the last channel of the image
        ########SaturationAdjustedImg[:, :, 3] = (maskx * 255).astype(np.uint8)

        cv2.imwrite( ImgPath1 + 'zNFTs.png', SaturationAdjustedImg )
        return mark_safe( 'data:image/png;base64,' + str( convert2Base64( SaturationAdjustedImg ) )[2:] )   # [2:] eliminates the leading b'
    else:
        cv2.imwrite( ImgPath1 + 'zNFT.png', Merge )


def applyTransparencyMask2( ToBeClipped, Mask ):
    Mask        = Mask.astype(np.float64)
    Img1        = (cv2.multiply( Mask, ToBeClipped ) / 255.0 ).astype(np.float32)
    return Result

def applyTransparencyMask( ToBeClipped, Background, Mask ):
    #Mask       = cv2.blur( Mask, (5, 5))
    InvMask     = cv2.bitwise_not( Mask ).astype(np.float64)
    #InvMask     = cv2.cvtColor( InvMask, cv2.COLOR_RGB2RGBA)
    Mask        = Mask.astype(np.float64)
    Img1        = (cv2.multiply( Mask, ToBeClipped ) / 255.0 ).astype(np.float64)
    Img2        = cv2.multiply( InvMask, Background ).astype(np.float64) / 255.0
    Result      = (cv2.add( Img1, Img2 ))
    Merged       = cv2.addWeighted( Background, 0.5, Result, 0.5, 0.1 ).astype(np.float32)
    #Merge       = cv2.cvtColor(Merge, cv2.COLOR_RGB2RGBA )
    return Merged

def changeSaturation( Merge, SaturationScale ):
    HSV           = cv2.cvtColor( Merge, cv2.COLOR_BGR2HSV )                 #... convert from BGR to HSV
    HSV[:, :, 1]  = np.clip( HSV[:, :, 1] * SaturationScale, 0, 255 )        #... adjust saturation
    AdjustedImg   = cv2.cvtColor( HSV, cv2.COLOR_HSV2BGR )                   #... convert back to BGR from HSV
    return AdjustedImg

def convert2Base64( Image ):
    _, im_arr = cv2.imencode( '.png', Image )  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode( im_bytes )
    return im_b64


def resizeSVG( SVGContent, NewWidth, NewHeight ):
    NewSVGContent = SVGContent
    NewSVGContent = re.sub( 'width:\d*px',  'width:'  + str(NewWidth)  + 'px', NewSVGContent )
    NewSVGContent = re.sub( 'height:\d*px', 'height:' + str(NewHeight) + 'px', NewSVGContent )
    return NewSVGContent










def blankfunction( Request ):
    Response = render( Request, '_main.html', {'Dada'  : '...'} )
    return Response


def mergeImages( Request ):

    '''
    Img1    = cv2.imread( "A:\\_\\triptych\\virtual\\triptych\\commons\\static\\vDB\\logo.png ").astype(np.float64)
    Img2    = cv2.imread( "A:\\_\\triptych\\virtual\\triptych\\commons\\static\\vDB\\mondie.png ").astype(np.float64)
    Merge   = cv2.addWeighted( Img1, 1.0, Img2, 0.0, 0.0 )

    cv2.imwrite( "A:\\_\\triptych\\virtual\\triptych\\commons\\static\\vDB\\merge6.jpg", Merge )
    '''

    Original    = cv2.imread( "A:\\_\\triptych\\virtual\\triptych\\commons\\static\\vDB\\mondie.png" ).astype(np.float64)
    Background  = cv2.imread( "A:\\_\\triptych\\virtual\\triptych\\commons\\static\\vDB\\logo.png" ).astype(np.float64)
    Mask        = cv2.imread("A:\\_\\triptych\\virtual\\triptych\\commons\\static\\vDB\\mask.png" ).astype(np.float64)

    #Mask        = cv2.blur( Mask, (5, 5))
    InvMask     = cv2.bitwise_not( Mask ).astype(np.float64)
    Mask        = Mask.astype(np.float64)
    Img1        = cv2.multiply( Mask, Original) / 255.0
    Img2        = cv2.multiply( InvMask, Background) / 255.0
    #Merge = cv2.addWeighted(Img1, 0.8, Img2, 0.2, 0.0)
    #Merge = cv2.addWeighted(Background, 0.6, Mask, 0.4, 0.0).astype(np.uint8)
    Result      = (cv2.add( Img1, Img2 ))
    Merge   = cv2.addWeighted( Background, 0.5, Result, 0.5, 0.5)
    #Merge   = cv2.addWeighted( Background, 0.4, Merge, 0.6, 0.0 )

    # Result      = cv2.add(Img1, Img2)
    '''
    (h, s, v) = cv2.split(Merge)
    s = s * 0.1
    h = h * 0.3
    v = v * 0.5
    s = np.clip(s, 128, 255)
    Merge = cv2.merge([h, s, v])
    '''


    cv2.imwrite("A:\\_\\triptych\\virtual\\triptych\\commons\\static\\vDB\\result32.jpg", Merge )

    Response = render(Request, '_main.html', {'Dada'  : '...'} )
    return Response



def image_colorfulness(image):
    # split the image into its respective RGB components
    (B, G, R) = cv2.split(image.astype("float"))

    # compute rg = R - G
    rg = np.absolute(R - G)

    # compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)

    # compute the mean and standard deviation of both `rg` and `yb`
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))

    # combine the mean and standard deviations
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))

    # derive the "colorfulness" metric and return it
    return stdRoot + (0.3 * meanRoot)

