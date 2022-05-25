#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# AGOL Account Login & Setup

import arcgis
from arcgis.gis import GIS
import smtplib, ssl
import logging, re, os
#logpath = r"\\HWYPB\NETSHARE\HWYA\HWY-AP\emaint\logs"
#rptpath = r"\\HWYPB\NETSHARE\HWYA\HWY-AP\emaint\reports"
logpath = r'D:\myfiles\HWYAP\branches\HWYL\logs'
rptpath = r'D:\myfiles\HWYAP\branches\HWYL\reports'
#inpath = r'D:\MyFiles\HWYAP\Admin\branches\HWY-C\emerepair'
inpath = r'D:\myfiles\HWYAP\branches\HWYL'
infilename = 'Interstate Poor Pavement Projects FY21-24 Updated.xlsx'
#logpath = r'I:\HI\AP\emerepair\logs'
#rptpath = r'I:\HI\AP\emerepair\reports'
#inpath = r'I:\HI\AP\emerepair'

logger = logging.getLogger('SPaveentries')
logfilenm = r'pavemententries.log'
logfile = os.path.join(logpath,logfilenm) # r"confemaintentries.log"
SPavehdlr = logging.FileHandler(logfile) # 'emaintentries.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
SPavehdlr.setFormatter(formatter)
logger.addHandler(SPavehdlr)
logger.setLevel(logging.INFO)

try:
    # ArcGIS user credentials to authenticate against the portal
    credentials = { 'userName' : '*****', 'passWord' : '*******'} # credentials = { 'userName' : 'dot_****', 'passWord' : '*****'}
    userName = credentials['userName'] # arcpy.GetParameter(2) # 
    passWord =  credentials['passWord'] #  # arcpy.GetParameter(3) 
    #credentials = { 'userName' : arcpy.GetParameter(4), 'passWord' : arcpy.GetParameter(5)}
    # Address of your ArcGIS portal
    portal_url = r"http://histategis.maps.arcgis.com/"
    print("Connecting to {}".format(portal_url))
    logger.info("Connecting to {}".format(portal_url))
    #qgis = GIS(portal_url, userName, passWord)
    qgis = GIS(profile="hisagolprof")
    numfs = 1000 # number of items to query
    print(f"Connected to {qgis.properties.portalHostname} as {qgis.users.me.username}")
    logger.info(f"Connected to {qgis.properties.portalHostname} as {qgis.users.me.username}")

    import arcpy, shutil, sys
    import xml.dom.minidom as DOM
    from arcpy import env
    import unicodedata
    import datetime, tzlocal
    from datetime import date , timedelta, datetime
    from time import sleep
    import math,random
    from os import listdir
    from arcgis.features._data.geodataset.geodataframe import SpatialDataFrame
    from cmath import isnan
    from math import trunc
    from _server_admin.geometry import Point
    from pandas.core.computation.ops import isnumeric
    # email to hidotlaneclsoures@hawaii.gov through outlook # Python 3

except ImportError:
#import ago
    print("error {} ".format(ImportError) )
    # 
    SystemExit()
try:
    import urllib.request, urllib.error, urllib.parse  # Python 2
except ImportError:
    import urllib.request as urllib2  # Python 3
import zipfile
from zipfile import ZipFile
import geojson, json
import fileinput
from os.path import isdir, isfile, join


import pandas as pd, numpy as np
#from pandas import DataFrame as pdf

#import geopandas as gpd

from arcgis import geometry
from arcgis import features 
import arcgis.network as network

from arcgis.features.analyze_patterns import interpolate_points
import arcgis.geocoding as geocode
from arcgis.features.find_locations import trace_downstream
from arcgis.features.use_proximity import create_buffers
from arcgis.features import GeoAccessor as gac, GeoSeriesAccessor as gsac
from arcgis.features import SpatialDataFrame as spedf

from arcgis.features import FeatureLayer

from copy import deepcopy


# In[ ]:


def webexsearch(mgis, title, owner_value, item_type_value, max_items_value=1000,inoutside=False):
    item_match = None
    search_result = mgis.content.search(query= "title:{} AND owner:{}".format(title,owner_value), 
                                          item_type=item_type_value, max_items=max_items_value, outside_org=inoutside)
    if "Imagery Layer" in item_type_value:
        item_type_value = item_type_value.replace("Imagery Layer", "Image Service")
    elif "Layer" in item_type_value:
        item_type_value = item_type_value.replace("Layer", "Service")
    
    for item in search_result:
        if item.title == title:
            item_match = item
            break
    return item_match

def lyrsearch(lyrlist, lyrname):
    lyr_match = None
   
    for lyr in lyrlist:
        if lyr.properties.name == lyrname:
            lyr_match = lyr
            break
    return lyr_match

def create_section(lyr, hdrow, chdrows,rtefeat):
    try:
        object_id = 1
        pline = geometry.Polyline(rtefeat)
        feature = features.Feature(
            geometry=pline[0],
            attributes={
                'OBJECTID': object_id,
                'PARK_NAME': 'My Park',
                'TRL_NAME': 'Foobar Trail',
                'ELEV_FT': '5000'
            }
        )

        lyr.edit_features(adds=[feature])
        #_map.draw(point)

    except Exception as e:
        print("Couldn't create the feature. {}".format(str(e)))
        

def fldvartxt(fldnm,fldtyp,fldnull,fldPrc,fldScl,fldleng,fldalnm,fldreq):
    fld = arcpy.Field()
    fld.name = fldnm
    fld.type = fldtyp
    fld.isNullable = fldnull
    fld.precision = fldPrc
    fld.scale = fldScl
    fld.length = fldleng
    fld.aliasName = fldalnm
    fld.required = fldreq
    return fld

def df_colsame(df):
    """ returns an empty data frame with the same column names and dtypes as df """
    #df0 = pd.DataFrame.spatial({i[0]: pd.Series(dtype=i[1]) for i in df.dtypes.iteritems()}, columns=df.dtypes.index)
    return df

def offdirn(closide,dirn1):
    if closide == 'Right':
        offdirn1 = 'RIGHT'
    elif closide == 'Left':
        offdirn1 = 'LEFT'
        dirn1 = -1*dirn1
    elif closide == 'Center':
        offdirn1 = 'RIGHT'
        dirn1 = 0.5
    elif closide == 'Both':
        offdirn1 = 'RIGHT'
        dirn1 = 0
    elif closide == 'Directional':
        if dirn1 == -1:
            offdirn1 = 'LEFT'
        else:
            offdirn1 = 'RIGHT'
    elif closide == 'Full' or closide == 'All':
        offdirn1 = 'RIGHT'
        dirn1 = 0
    elif closide == 'Shift':
        offdirn1 = 'RIGHT'
    elif closide == 'Local':
        offdirn1 = 'RIGHT'
    else:
        offdirn1 = 'RIGHT'
        dirn1 = 0 
    return offdirn1,dirn1

def deleteupdates(prjstlyrsrc, sectfeats):
    for x in prjstlyrsrc:
        print (" layer: {} ; from item : {} ; URL : {} ; Container : {} ".format(x,x.fromitem,x.url,x.container))
        if 'Projects' in (prjstlyrsrc):
            xfeats =  x.query().features
            if len(xfeats) > 0:
                if isinstance(xfeats,(list,tuple)):
                    if "OBJECTID" in xfeats[0].attributes:
                        oids = "'" + "','".join(str(xfs.attributes['OBJECTID']) for xfs in xfeats if 'OBJECTID' in xfs.attributes ) + "'"
                        oidqry = " OBJECTID in ({}) ".format(oids)
                    elif "OID" in xfeats[0].attributes:    
                        oids = "'" + "','".join(str(xfs.attributes['OID']) for xfs in xfeats if 'OID' in xfs.attributes ) + "'"
                        oidqry = " OID in ({}) ".format(oids)
                    print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
                    
                elif isinstance(xfeats,spedf):
                    if "OBJECTID" in xfeats.columns:
                        oids = "'" + "','".join(str(f1.get_value('OBJECTID')) for f1 in xfeats ) + "'"
                        oidqry = " OBJECTID in ({}) ".format(oids)
                    elif "OID" in xfeats.columns:    
                        oids = "'" + "','".join(str(f1.get_value('OID')) for f1 in xfeats ) + "'"
                        oidqry = " OID in ({}) ".format(oids)
                    print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
                    
                if 'None' in oids:
                    print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
                else:
                    x.delete_features(where=oidqry)

def delayerfeatures(x):
    xfeats =  x.query().features
    if len(xfeats) > 0:
        if isinstance(xfeats,(list,tuple)):
            if "OBJECTID" in xfeats[0].attributes:
                oids = "'" + "','".join(str(xfs.attributes['OBJECTID']) for xfs in xfeats if 'OBJECTID' in xfs.attributes ) + "'"
                oidqry = " OBJECTID in ({}) ".format(oids)
            elif "OID" in xfeats[0].attributes:    
                oids = "'" + "','".join(str(xfs.attributes['OID']) for xfs in xfeats if 'OID' in xfs.attributes ) + "'"
                oidqry = " OID in ({}) ".format(oids)
            print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
            
        elif isinstance(xfeats,spedf):
            if "OBJECTID" in xfeats.columns:
                oids = "'" + "','".join(str(f1.get_value('OBJECTID')) for f1 in xfeats ) + "'"
                oidqry = " OBJECTID in ({}) ".format(oids)
            elif "OID" in xfeats.columns:    
                oids = "'" + "','".join(str(f1.get_value('OID')) for f1 in xfeats ) + "'"
                oidqry = " OID in ({}) ".format(oids)
            print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
            
        if 'None' in oids:
            print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
        else:
            x.delete_features(where=oidqry)
                    
                    
# Given anydate and n1 as 0 or 1 or 2 , etc  it computes Last Friday, First Friday and Second Friday, etc at 4PM
def fridaywk(bdate,n1):
    wkdte = datetime.strftime(bdate,"%w") # + datetime.strftime(bdate,"%z")
    date4pm = datetime.strptime(datetime.strftime(bdate,"%Y-%m-%d"),"%Y-%m-%d") + timedelta(hours=16)
    fr4pm= date4pm + timedelta(days=(5-int(wkdte)+(n1-1)*7))
    return fr4pm


def intextold(intxt,rte,rtename):
    intshortlbl = intxt['address']['ShortLabel']
    intsplitxt = intshortlbl.split(sep='&', maxsplit=1)
    txtret=intsplitxt[1]  # default to the second intersection unless the second one has the route
    for txt in intsplitxt:
        if rtename not in txt or rte not in txt:
            txtret = txt
    return txtret          

def intext(intxt,rte,rtename,fromtxt="Nothing"):
    intshortlbl = intxt['address']['ShortLabel']
    rtext = re.sub("-","",rte)
    if rtename is None:
        rtenametxt = 'Nothing'
    else:    
        rtenametxt = re.sub("-","",rtename)
    intsplitxt = intshortlbl.split(sep='&') #, maxsplit=1)
    intsplitxt = [t1.strip() for t1 in intsplitxt ]
    if len(intsplitxt)==2: 
        txtret=intsplitxt[1]  # default to the second intersection unless the second one has the route
    elif len(intsplitxt)==3:
        txtret=intsplitxt[2]  # default to the second intersection unless the second one has the route
    else:
        txtret=intsplitxt[0]  # default to the second intersection unless the second one has the route
            
    rtenmsplit = [ t2.strip() for t2 in rtenametxt.split(sep=" ")]
    if len(rtenmsplit)>2:
        rtenmsplit = "{} {}".format(rtenmsplit[0].capitalize(),rtenmsplit[1].capitalize())
    else:
        rtenmsplit = "{}".format(rtenmsplit[0].capitalize())
               
    for txt in intsplitxt:
        txtsep = txt.split(sep=" ")
        if len(txtsep)<=2 :
            if (txt[0:2]).isnumeric():
                txt = "Exit " + txt.upper()
        if rtenmsplit not in txt and rtext not in txt and fromtxt!=txt:
            txtret = txt
        else:
            txtret = txt
    return txtret          

def datemidnight(bdate):
    date0am = datetime.strptime(datetime.strftime(bdate,"%Y-%m-%d"),"%Y-%m-%d") + timedelta(hours=0)
    return date0am

# function to return whether the closure date range is a weekend or weekday
def wkend(b,e):
    if b==0 and e <=1: 
        return 1 
    elif b>=1 and b<=5 and e>=1 and e<=5: 
        return 0 
    elif b>=5 and (e==6 or e==0): 
        return 1 
    else: 
        return 0

def beginwk(bdate):
    wkdte = datetime.strftime(bdate,"%w")
    if (wkdte==0):
        bw = bdate + timedelta(days=wkdte)
    else:  # wkdte>=1:
        bw = bdate + timedelta(days=(7-wkdte))
    return bw

def beginthiswk(bdate):
    wkdte = datetime.strftime(bdate,"%w")
    if (wkdte==0):
        bw = bdate - timedelta(days=wkdte)
    else:  # wkdte>=1:
        bw = bdate - timedelta(days=(8-int(wkdte)))
    return bw    
                                                                                                                                                                                                                                                                                                                                                                                                                                                        
def midnextnight(bdate,n1):
    datenextam = datetime.strptime(datetime.strftime(bdate,"%Y-%m-%d"),"%Y-%m-%d") + timedelta(day=n1)
    return datenextam

#BeginDateName,EndDateName:  The month and the day portion of the begin or end date. (ex. November 23)
def dtemon(dte):
    dtext = datetime.strftime(dte-timedelta(hours=10),"%B") + " " +  str(int(datetime.strftime(dte-timedelta(hours=10),"%d")))
    return dtext

# BeginDay, EndDay: Weekday Name of the begin date (Monday, Tuesday, Wednesday, etc.)
def daytext(dte):
    dtext = datetime.strftime(dte-timedelta(hours=10),"%A") 
    return dtext

#BeginTime, EndTime: The time the lane closure begins.  12 hour format with A.M. or P.M. at the end
def hrtext(dte):
    hrtext = datetime.strftime(dte-timedelta(hours=10),"%I:%M %p") 
    return hrtext


def rtempt(lyrts,rtefc,lrte,bmpvalx,offs=0,fldrte='Route'):
    if 'mptbl' in locals():
        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
    else:
        rtevenTbl = "RtePtEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RtePtEvtFC"
        outFeatseed = "EvTbl"
        x1 = random.randrange(1001,2000,1) #1001
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP ".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)
        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)
        # linear reference fields 

    bmpval = bmpvalx
    empval = bmpvalx
    rteFCSel = "RteSelected{}".format(x1)
    rtevenTbl = "RteLinEvents{}".format(x1)
    eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    if (len(rtefc)>0):
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        mpinscur.insertRow((rteid.upper(), bmpval,offs))
        dirnlbl = 'LEFT'
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProPts, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
        # get the geoemtry from the result layer and append to the section feature class
        if arcpy.Exists(eveLinlyr):    
            cntLyr = arcpy.GetCount_management(eveLinlyr)
        if cntLyr.outputCount > 0:
            #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
            insecgeo = None
            # dynamic segementaiton result layer fields used to create the closure segment  
            lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'Shape@JSON']
            evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
            for srow in evelincur:
                #insecgeo = srow.getValue("SHAPE@")
                #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                rtenum = srow[1]
                insecgeo = arcgis.geometry.Geometry(srow[4])
                if insecgeo is None:
                    print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,bmpval,empval,offs ))
                    logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,bmpval,empval,offs ))
                    insecgeo = geomrte.project_as(sprefwgs84)
                else:
                    print('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,bmpval,empval,offs ))
                    logger.info('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,bmpval,empval,offs ))
                insecgeo = insecgeo.project_as(sprefwgs84)
            del evelincur        
        del rteFCSel,lrte,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} create point geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create point geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None    
    return insecgeo


def rtesectpt(lyrts,rteid,bmpvalx,offs,fldrte='Route'):
    if 'mptbl' in locals():
        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
    else:
        rtevenTbl = "RtePtEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RtePtEvtFC"
        outFeatseed = "EvTbl"
        x1 = random.randrange(1001,2000,1) #1001
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP EMP".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)
        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)
        # linear reference fields 
    bmpval = bmpvalx
    empval = bmpvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)<=0):
        if rteid == "5600":
            rteid="560"
        else:
            rteid="560"    
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)>0):
        rteFCSel = featlnclrte.save('in_memory','rtesel')
        ftlnclrte = featlnclrte.features
        rtegeo = ftlnclrte[0].geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        rtept2 = rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)
                
        if (bmpval<bmprte):
            bmpval=bmprte
        if (bmpval>emprte):
            bmpval=bmprte
    
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        arcpy.env.outputMFlag = "Disabled"
        lrte = os.path.join('in_memory','rteselyr')
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        # create the milepost insert cursor fields  
        mpflds = [RteFld.name,bmpFld.name,empFld.name,ofFld.name]
        # create the MilePost Insert cursor 
        mpinscur = arcpy.da.InsertCursor(mptbl, mpflds)  
        
        mpinscur.insertRow((rteid.upper(), bmpval,bmpval,offs))
        dirnlbl = 'LEFT'
        
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProPts, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
        # get the geoemtry from the result layer and append to the section feature class
        if arcpy.Exists(eveLinlyr):    
            cntLyr = arcpy.GetCount_management(eveLinlyr)
        if cntLyr.outputCount > 0:
            #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
            insecgeo = None
            # dynamic segementaiton result layer fields used to create the closure segment  
            lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'EMP', 'Shape@JSON']
            evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
            for srow in evelincur:
                #insecgeo = srow.getValue("SHAPE@")
                #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                rtenum = srow[1]
                insecgeo = arcgis.geometry.Geometry(srow[4])
                if insecgeo is None:
                    print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    insecgeo = geomrte.project_as(sprefwgs84).first_point
                else:
                    print('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    logger.info('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                insecgeo = insecgeo.project_as(sprefwgs84)
            del evelincur        
        del rteFCSel,lrte,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpval,empvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo.first_point)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None    
    return insecgeo

import numbers
import random
def testnumber(x):
    if any([isinstance(x,float),isinstance(x,int)]):
      return True
    else:
      return False
    
def multirtes(rtelyr,xRte,xBMP,xEMP,offs,rtelyrid,fldrte='Route',i1=-999):
    rteslist = xRte.split(sep='|')
    gx=[]
    print('Layer {} :  Route {} ; BMP : {} ; EMP : {} ; offset  : {} ; layer id {}.'.format(rtelyr,xRte,xBMP,xEMP,offs,rtelyrid ))
    
    for rte in rteslist:
        if len(rte)>0:
            gx = rtesectline(rtelyr,rte,xBMP,xEMP,offs,fldrte)
    return gx    
def rtesectline(lyrts,rteid,bmpvalx,empvalx,offs,fldrte='Route',i1=-999):
    sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
    sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }

    if 1==1 : #'mptbl' in locals():
        """        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
          else:   """
        rtevenTbl = "RtePtEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RtePtEvtFC"
        outFeatseed = "EvTbl"
        x1 = random.randrange(1001,2000,1)
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}{}""".format(outFeatseed,x1) 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP EMP".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)
        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)
        # linear reference fields 
    bmpval = bmpvalx
    empval = empvalx
    rteFCSel = "RteSelected{}".format(x1)
    rtevenTbl = "RteLinEvents{}".format(x1)
    eveLinlyr = "{}_{}".format('lrtelyr',x1) #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)<=0):
        if rteid == "5600":
            rteid="560"
        else:
            rteid="560"    
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)>0):
        rteFCSel = featlnclrte.save('in_memory',"{}{}".format('rtesel',x1))
        ftlnclrte = featlnclrte.features
        rtegeo = ftlnclrte[0].geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rteleng = geomrte.get_length(method='PLANAR',units='METERS')
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        rtept2 = rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
# new addition 6/23/2020
        if (rtept1[2] == None):
            rtept1[2] = 0
            print('{} :  Route {} ; original BMP : None ;  Assigned BMP : {} .'.format(i1,rteid,rtept1[2] ))
            logger.info('{} : Route {} ; original BMP : None ;  Assigned BMP : {} .'.format(i1,rteid,rtept1[2] ))
        if (rtept2[2] == None):    
            rtept2[2] = round(rteleng*3.2808333/5280.0,3)
            print('{} :  Route {} ; original EMP :  Assigned ; Assigned EMP : {} .'.format(i1,rteid,rtept2[2] )) 
            logger.info('{} : Route {} ; original EMP : None ;  Assigned EMP : {} .'.format(i1,rteid,rtept2[2] )) 
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)
        #bmpval = pd.to_numeric(bmpval,errors='coerce')
        #empval = pd.to_numeric(empval,errors='coerce')
        if np.isnan(bmpval):
            print('{} : non numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            logger.info('{} : non numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            #return geomrte.project_as(sprefwgs84)
            bmpval = bmprte + 0.001
        else:
            print('{} : numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            logger.info('{} : numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            bmpval = bmprte + 0.001
        if np.isnan(empval):
            print('{} : non numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            logger.info('{} : non numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            if np.isnan(bmpval):
                empval = emprte - 0.001
            else:
                #empval = bmpval + 0.02  # increased the minimum length becasue some sections were not generated
                empval = emprte - 0.001
        else:
            print('{} : numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            logger.info('{} : numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            
        if (empval<bmpval):
            inpval = empval
            empval=bmpval
            bmpval = inpval
        elif (round(empval,3)==0 and bmpval<=0):
            empval=bmpval + 0.02
                
        if (bmpval<bmprte):
            bmpval=bmprte
        if (bmpval>emprte):
            bmpval=emprte-0.02
            empval = emprte
        if (empval>emprte):
            empval=emprte
    
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        arcpy.env.outputMFlag = "Disabled"
        lrte = os.path.join('in_memory','rteselyr{}'.format(x1))
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        # create the milepost insert cursor fields  
        mpflds = [RteFld.name,bmpFld.name,empFld.name,ofFld.name]
        # create the MilePost Insert cursor 
        mpinscur = arcpy.da.InsertCursor(mptbl, mpflds)  
        rtes = rteid.split('?')
        if len(rtes)>1:
            for rte in rtes:
                if len(rte)>0:
                    mpinscur.insertRow((rte.upper(), bmpval,empval,offs))
            print(' multiple routes entered for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            logger.info(' multiple routes entered for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        else:            
            mpinscur.insertRow((rteid.upper(), bmpval,empval,offs))
               
        dirnlbl = 'LEFT'
        
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        arcpy.env.outputMFlag = "Disabled"
        lrte = os.path.join('in_memory','rteselyr{}'.format(x1))
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        
        if (abs(empval-bmpval)<0.02):
            bmpval=max(bmpval,empval)-0.01
            empval=bmpval+0.02
        if len(rtes)>1:
            for rte in rtes:
                if len(rte)>0:
                    mpinscur.insertRow((rte.upper(), bmpval,empval,offs))
            print(' multiple routes entered for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            logger.info(' multiple routes entered for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        else:            
            mpinscur.insertRow((rteid.upper(), bmpval,empval,offs))
        #mpinscur.insertRow((rteid.upper(), bmpval,empval,offs))
        print('\n geometry generation for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        logger.info('\n geometry generation for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        dirnlbl = 'LEFT'
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProLines, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
        # get the geoemtry from the result layer and append to the section feature class
        if arcpy.Exists(eveLinlyr):    
            cntLyr = arcpy.GetCount_management(eveLinlyr)
        if cntLyr.outputCount > 0:
            #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
            insecgeo = None
            # dynamic segementaiton result layer fields used to create the closure segment  
            lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'EMP', 'Shape@JSON']
            evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
            for srow in evelincur:
                #insecgeo = srow.getValue("SHAPE@")
                #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                rtenum = srow[1]
                insecgeo = arcgis.geometry.Geometry(srow[4])
                #print(' geometry : {} type {} ; for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(insecgeo,type(insecgeo),lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                if not insecgeo:
                    print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    # use two mile posts to generate two coordinate and draw a line geometry
                    mplist = [bmpval,empval]
                    offs=0
                    mpres = []
                    mpts = []
                    for m1 in mplist:
                        ptres= milepost2coords(lyrts,rtenum,m1,offs,fldrte)
                        print('milepost2coords returned {} type : {} ; data  : {} ; on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(type(ptres),ptres,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        logger.info('milepost2coords returned {} type : {} ; data : {} ; on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(type(ptres),ptres,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        if type(ptres) is None:
                            ptres = rtept1  
                        elif str(type(ptres)) !=  "<class 'dict'>":
                            print('milepost2coords returned {} geometry : {} ; on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(type(ptres),ptres,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                            logger.info('milepost2coords returned {} geometry : {} ; on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(type(ptres),ptres,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                            ptres = ptres.first_point
                        mpres.append (ptres)
                        if len(ptres) == 0:
                            ptres = {'x': -157.05356057262688, 'y': 21.1357042336581, 'spatialReference': {'wkid': 4326, 'latestWkid': 4326}} 
                        mpts.append([ptres.x,ptres.y, m1]) # (  [lambda x :  for m1 in mplist:
                        srpt = ptres.spatial_reference
                    #line = { "paths" : [ [xb,yb],[xe,ye]], "spatialReference" : {"wkid" : 4326}}    
                    line = {'hasM': True, 'paths': [ mpts ], "spatialReference" : srpt}
                    pline = arcgis.geometry.Polyline(line) #sectgeom = Geometry([[xb,yb],[xe,ye]])
                    print('Polyline : {} for Rte {}'.format(pline,rtenum,mplist))
                    insecgeo = pline
                    if not insecgeo: 
                        insecgeo =  geomrte # arcgis.geometry.Geometry(geomrte)
                else:
                    #print('created Shape : {} for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {} .'.format(insecgeo,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    logger.info('created Shape : {} for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {} .'.format(insecgeo,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                print('Procesing Shape : {} for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {} .'.format(insecgeo,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                insecgeo = insecgeo.project_as(sprefwgs84)
            del evelincur        
        del rteFCSel,lrte,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None
    print('returned Geometry : {} for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {} .'.format(insecgeo,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
    return insecgeo


def three2twod(shp):
    if shp is not None:
        mgeom = shp['paths']
        glen = len(mgeom) # rtepaths[0][len(rtepaths[0])-1] 
        smupltxt = ""
        if glen>0:
            smupline = []
            for il,linex in enumerate(mgeom,0):
                for xy in linex:
                    xylist = []
                    for i,x in enumerate(xy,1):
                        if i==1:
                            xylist.append(x)
                        elif i==2:
                            xylist.append(x)
                    smupline.append(xylist)
        smuplinef = [smupline]
    else:
        smuplinef = []
    return smuplinef


def rtesectmp(lyrts,rteid,bmpvalx,empvalx,offs):
    if arcpy.Exists(mptbl):    
        if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
            arcpy.DeleteRows_management(mptbl)
    bmpval = bmpvalx
    empval = empvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    rtegeo = None
    lyrname = lyrts.properties.name
    featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)<=0):
        if rteid == "5600":
            rteid="560"
        else:
            rteid="560"    
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)>0):
        rteFCSel = featlnclrte.save('in_memory','rtesel')
        ftlnclrte = featlnclrte.features
        rtegeo = ftlnclrte[0].geometry
        geomrte = deepcopy(rtegeo) # arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        rtept2 = rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
        bmprte = rtept1[2]
        emprte = rtept2[2]
        if bmprte==None or emprte==None:
            insecgeo = three2twod(rtegeo)
            #insecgeo = Geometry({ "paths" : insecgeo , "spatialReference" : sprefwebaux })
            insecgeo =arcgis.geometry.Geometry({ "paths" : insecgeo , "spatialReference" : sprefwebaux }) #(insecgeo,sr=sprefwebaux)
            lengeo = insecgeo.length
            insecgeo = insecgeo.project_as(sprefwgs84 ) #sprefwebaux) #insecgeo.project_as(sprefwgs84)
#            print('Route {} ; Rte pre-geometry {} ; projected {} ; new {}  ; length : {} ; layer {} , rte {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format
#                  (rteid,rtegeo,geomrte,insecgeo,lengeo,lyrname,rteid,bmpvalx,empvalx,bmprte,emprte,offs ))
#           logger.info('Route {} ; Rte pre-geometry {} ; projected {} ; new {}  ; length : {} ; layer {} , rte {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format
#                  (rteid,rtegeo,geomrte,insecgeo,lengeo,lyrname,rteid,bmpvalx,empvalx,bmprte,emprte,offs ))
        else:
            bmprte = round(rtept1[2],3)
            emprte = round(rtept2[2],3)
            if (empval<bmpval):
                inpval = empval
                empval=bmpval
                bmpval = inpval
            elif (round(empval,3)==0 and bmpval<=0):
                empval=bmpval + 0.01
                    
            if (bmpval<bmprte):
                bmpval=bmprte
            if (bmpval>emprte):
                bmpval=bmprte
            if (empval>emprte):
                empval=emprte
    
            #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
            arcpy.env.outputMFlag = "Disabled"
            lrte = os.path.join('in_memory','rteselyr')
            arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
            flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
            lrterows = arcpy.da.SearchCursor(lrte,flds)
            
            if (abs(empval-bmpval)<0.01):
                bmpval=max(bmpval,empval)-0.005
                empval=bmpval+0.01
            mpinscur.insertRow((rteid.upper(), bmpval,empval,offs))
            dirnlbl = 'LEFT'
            arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProLines, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
            # get the geoemtry from the result layer and append to the section feature class
            if arcpy.Exists(eveLinlyr):    
                cntLyr = arcpy.GetCount_management(eveLinlyr)
            if cntLyr.outputCount > 0:
                #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
                insecgeo = None
                # dynamic segementaiton result layer fields used to create the closure segment  
                lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'EMP', 'Shape@JSON']
                evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
                for srow in evelincur:
                    #insecgeo = srow.getValue("SHAPE@")
                    #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                    rtenum = srow[1]
                    insecgeo = arcgis.geometry.Geometry(srow[4])
                    if insecgeo == None:
                        print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        insecgeo = geomrte.project_as(sprefwgs84)
                    else:
                        #print('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        #logger.info('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        insecgeo = insecgeo.project_as(sprefwgs84)
                del evelincur,lrte        
        del rteFCSel,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=rtegeo    
    #print('Layer {} ; Route {} created section geometry {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,insecgeo,bmpvalx,empvalx,bmpval,empval,offs ))
    return insecgeo

def rtesectmpx(lyrts,rteid,bmpvalx,empvalx,offs,fldrte):
    if 'mptbl' in locals():
        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
    else:
        rtevenTbl = "RtePolyEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RtePolyEvtFC"
        outFeatseed = "EvTbl"
        x1 = 1001 #random.randrange(1001,2000,1)
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        #fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP EMP".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)
        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)

    bmpval = bmpvalx
    empval = empvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)<=0):
        if rteid == "5600":
            rteid="560"
        else:
            rteid="560"    
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)>0):
        rteFCSel = featlnclrte.save('in_memory','rtesel')
        ftlnclrte = featlnclrte.features
        rtegeo = ftlnclrte[0].geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        rtept2 = rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)
        if (empval<bmpval):
            inpval = empval
            empval=bmpval
            bmpval = inpval
        elif (round(empval,3)==0 and bmpval<=0):
            empval=bmpval + 0.01
                
        if (bmpval<bmprte):
            bmpval=bmprte
        if (bmpval>emprte):
            bmpval=bmprte
        if (empval>emprte):
            empval=emprte
    
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        arcpy.env.outputMFlag = "Disabled"
        lrte = os.path.join('in_memory','rteselyr')
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        
        if (abs(empval-bmpval)<0.01):
            bmpval=max(bmpval,empval)-0.005
            empval=bmpval+0.01
        # create the MilePost Insert cursor 
        mpflds = [RteFld.name,bmpFld.name,empFld.name,ofFld.name]
        
        mpinscur = arcpy.da.InsertCursor(mptbl, mpflds)  
            
        mpinscur.insertRow((rteid.upper(), bmpval,empval,offs))
        dirnlbl = 'LEFT'
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProLines, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
        # get the geoemtry from the result layer and append to the section feature class
        if arcpy.Exists(eveLinlyr):    
            cntLyr = arcpy.GetCount_management(eveLinlyr)
        if cntLyr.outputCount > 0:
            #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
            insecgeo = None
            # dynamic segementaiton result layer fields used to create the closure segment  
            lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'EMP', 'Shape@JSON']
            evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
            for srow in evelincur:
                #insecgeo = srow.getValue("SHAPE@")
                #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                rtenum = srow[1]
                insecgeo = arcgis.geometry.Geometry(srow[4])
                #print(' geometry : {} for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(insecgeo,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                
                if insecgeo is None:
                    print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    insecgeo = geomrte.project_as(sprefwgs84)
                else:
                    print('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    logger.info('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                insecgeo = insecgeo.project_as(sprefwgs84)
            del evelincur        
        del rteFCSel,lrte,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None    
    return insecgeo

def mergeometry(geomfeat):
    mgeom = geomfeat.geometry
    if len(geomfeat)>0:
        rtegeo = geomfeat.geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        glen = len(rtepaths) # rtepaths[0][len(rtepaths[0])-1] 
        rtept2 = rtepaths[glen-1][len(rtepaths[glen-1])-1] #geomrte.last_point
        mgeom =[ [ x for sublist in rtepaths for x in sublist] ]
    return mgeom

def geom3d2d(geomfeat):
    mgeom = geomfeat.geometry
    if len(geomfeat)>0:
        rtegeo = geomfeat.geometry
        rtepaths = rtegeo['paths']
        
        rtept1 = rtepaths[0][0] # geomrte.first_point
        glen = len(rtepaths) # rtepaths[0][len(rtepaths[0])-1] 
        rtept2 = rtepaths[glen-1][len(rtepaths[glen-1])-1] #geomrte.last_point
        mgeom =[ [ x for sublist in rtepaths for x in sublist] ]
    return mgeom

# Remove M values from multiline arcgis shape geometry 
def shpxmeasure(shp):
    slinetxt = ""
    if shp is not None:
        mgeom = shp['paths']
        glen = len(mgeom) # rtepaths[0][len(rtepaths[0])-1] 
        if glen>0:
            shp0 = []
            for il,linex in enumerate(mgeom,0):
                shp1 = []
                for xy in linex:
                    shp2 = []
                    xylist = ""
                    for i,x in enumerate(xy,1):
                        if i==1:
                            xylist = str(x)
                        elif i==2:
                            xylist = xylist + " , " + str(x)
                    shp2.append(xylist)
            shp1.append(shp2)
        shp0.append(shp1)       
    else:
        shp0 = "[]"
    slinetxt = "LineString {}".format(shp)
    #slinetxt = slinetxt.replace("'","").replace("[","(").replace("]",")")            
    return slinetxt



# generate multi-geometric list from an arcgis multi-geometry feature
def xmergeometry(geomfeat):
    mgeom = geomfeat.geometry
    if len(geomfeat)>0:
        rtegeo = geomfeat.geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        glen = len(rtepaths) # rtepaths[0][len(rtepaths[0])-1] 
        rtept2 = rtepaths[glen-1][len(rtepaths[glen-1])-1] #geomrte.last_point
        mgeom =[ [ x for sublist in rtepaths for x in sublist] ]
    return mgeom

# generate multi-geometric list from an arcgis multi-geometry feature
def featmergeometry(geomfeat):
    mgeom = geomfeat.geometry
    if len(geomfeat)>0:
        rtegeo = geomfeat.geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        glen = len(rtepaths) # rtepaths[0][len(rtepaths[0])-1] 
        rtept2 = rtepaths[glen-1][len(rtepaths[glen-1])-1] #geomrte.last_point
        mgeom =[ [ x for sublist in rtepaths for x in sublist] ]
    return mgeom

# generate single geometric list from an arcgis multi-geometry paths 
def xmergeometry(geompaths):
    mgeom = geompaths
    glen = len(geompaths) # rtepaths[0][len(rtepaths[0])-1] 
    if glen>0:
        mgeom =[ x for sublist in geompaths for x in sublist]
    return mgeom

# convert the esri multiline paths to soctrata multiline 
# MULTILINESTRING ((10 10, 20 20, 10 40),(40 40, 30 30, 40 20, 30 10))
def socratamultilinegeom(geompaths):
    mgeom = geompaths
    glen = len(geompaths) # rtepaths[0][len(rtepaths[0])-1] 
    smupltxt = ""
    if glen>0:
        smupline = []
        for il,linex in enumerate(geompaths,0):
            smupline.append([])
            for xy in linex:
                xylist = ""
                for i,x in enumerate(xy,1):
                    if i==1:
                        xylist = str(x)
                    elif i==2:
                        xylist = xylist + " " + str(x)
                smupline[il].append(xylist)
    smupltxt = "MultiLineString {}".format(smupline)
    smupltxt = smupltxt.replace("'","").replace("[","(").replace("]",")")            
    return smupltxt

# convert the esri multiline to soctrata multiline 
# MULTILINESTRING ((10 10, 20 20, 10 40),(40 40, 30 30, 40 20, 30 10))
def socratamultilineshp(shp):
    if shp is not None:
        mgeom = shp['paths']
        glen = len(mgeom) # rtepaths[0][len(rtepaths[0])-1] 
        smupltxt = ""
        if glen>0:
            smupline = []
            for il,linex in enumerate(mgeom,0):
                smupline.append([])
                for xy in linex:
                    xylist = ""
                    for i,x in enumerate(xy,1):
                        if i==1:
                            xylist = str(x)
                        elif i==2:
                            xylist = xylist + " " + str(x)
                    smupline[il].append(xylist)
    else:
        smupline = ""
    smupltxt = "MultiLineString {}".format(smupline)
    smupltxt = smupltxt.replace("'","").replace("[","(").replace("]",")")            
    return smupltxt

# generate single socrata line from an arcgis multiline shape geometry 
def soclineshp(shp):
    slinetxt = ""
    if shp is not None:
        mgeom = shp['paths']
        glen = len(mgeom) # rtepaths[0][len(rtepaths[0])-1] 
        if glen>0:
            socline = []
            for il,linex in enumerate(mgeom,0):
                for xy in linex:
                    xylist = ""
                    for i,x in enumerate(xy,1):
                        if i==1:
                            xylist = str(x)
                        elif i==2:
                            xylist = xylist + " " + str(x)
                    socline.append(xylist)
    else:
        socline = ""
    slinetxt = "LineString {}".format(socline)
    slinetxt = slinetxt.replace("'","").replace("[","(").replace("]",")")            
    return slinetxt


def assyncadds(lyr1,fset):
    sucs1=0
    pres = None
    t1 = 0
    while(sucs1<=0 and t1<10):
        pres = lyr1.edit_features(adds=fset) #.append(prjfset) #.append(prjfset,field_mappings=fldmaprj)
        if pres['addResults'][0]['success']==True:
            sucs1=1
        else:
            t1 += 1
            sleep(7)
    return pres

def assyncaddspt(lyr1,fset):
    sucs1=0
    pres = None
    t1 = 0
    while(sucs1<=0 and t1<5):
        pres = lyr1.edit_features(adds=fset) #.append(prjfset) #.append(prjfset,field_mappings=fldmaprj)
        if pres['addResults'][0]['success']==True:
            sucs1=1
        else:
            t1 += 1
            sleep(5)
    return pres

def assyncedits(lyr1,fset):
    sucs1=0
    errcnt = 0
    pres = None
    while(round(sucs1)==0):
        pres = lyr1.edit_features(updates=fset) #.append(prjfset) #.append(prjfset,field_mappings=fldmaprj)
        if pres['updateResults'][0]['success']==True:
            sucs1=1
        else:
            errcnt+=1
            terr = datetime.datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p")
            logger.error("Attempt {} at {} ; Result : {} ; Layer {} ; attributes {} ; geometry {} ".format(errcnt,terr, pres,lyr.properties.name,fset.features[0].attributes,fset.features[0].geometry))
            #if errcnt<=10:
            sleep(7)
            #else:    
            #    sucs1 = -1
    return pres


def qryhistdate(bdate,d1=0):
    dateqry = datetime.strftime((bdate-timedelta(days=d1)),"%m-%d-%Y")
    return dateqry
 
    
def searchcontentbytimestamp(input_days):
    # UTC time
    now_dt = datetime.datetime.utcnow()
    then_dt = now_dt - timedelta(days=int(input_days))

    # construct the string for range search, see ESRI doc for string format
    now = '000000'+str(int(now_dt.timestamp()))+'000'
    then = '000000'+str(int(then_dt.timestamp()))+'000'

    items = gis.content.search(
     query = 'uploaded: [' + then + ' TO ' + now + ']', 
     max_items=10000
    )

    # sort the items by modified date
    items2 = sorted(items,key=lambda item:item.modified)

    for item in items2:
        str_time = datetime.datetime.fromtimestamp(item.modified/1000).strftime('%Y-%m-%d %H:%M:%S')
        print("Modified Time:{0}, Title:{1}".format(str_time,item.title))


    return items2




def pts2mpost(lyrtes,rteid,listpts,fldrte,searange,spref):
    mpdata = []
    featlnclrte = lyrts.query(where = "{} in  ({}{}{}) ".format(fldrte," '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if 'rteFCSel' in locals():
        del rteFCSel            
    ftlnclrte = featlnclrte.features
    if (len(ftlnclrte)>0):
        rtegeo = ftlnclrte[0].geometry
        rtegeo['spatialReference'] = featlnclrte.spatial_reference
        geomrte = arcgis.geometry.Geometry(rtegeo)
        rteleng = geomrte.get_length(method='PLANAR',units='METERS')
        rtepaths = rtegeo['paths']
        # eliminate the gaps merge the paths 
        rtept1 = rtepaths[0][0] # geomrte.first_point
        glen = len(rtepaths) # rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
        rtept2 = rtepaths[glen-1][len(rtepaths[glen-1])-1]
        # new addition 6/8/2020
        if (rtept1[2] == None):
            rtept1[2] = 0
        if (rtept2[2] == None):    
            rtept2[2] = round(rteleng*3.2808333/5280.0,3)  # assuming route length is in meters
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)
        rtegeox = [[ x for sublist in rtepaths for x in sublist]]
        rtegeo['paths'] =  rtegeox
        featlnclrte.features[0].geometry['paths'] = rtegeox
        print("Rte {} ; Bmp : {} ; emp : {} ;  has {} sections; Search Range {} ".format(rteid,bmprte,emprte,glen,searange))
        has_m = "DISABLED"
        has_z = "DISABLED"
        geotype = "POINT"
        x1 = 1001 #random.randrange(1001,2000,1)
        outFeatseed = "EvTbl"
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1)
        # linear reference fields 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        
        # geopoint featureclass to store the lane closure locations 
        geoPtFC = arcpy.CreateFeatureclass_management("in_memory", lrsGeoPTbl, geotype,spatial_reference=arcpy.SpatialReference(spref['wkid']))#,'',has_m, has_z,spref) #.getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        arcpy.AddField_management(geoPtFC, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(geoPtFC, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(geoPtFC, empFld.name, empFld.type, empFld.precision, empFld.scale)
        geoPtFCnm = "{}".format(geoPtFC)
        ptflds = [RteFld.name,"SHAPE@XY"]
        rteFCSel = featlnclrte.save('in_memory','rtefcsel{}'.format(x1))
        if 'geoPtFC' in locals():
            if arcpy.Exists(geoPtFC):
                if int(arcpy.GetCount_management(geoPtFC).getOutput(0)) > 0:
                    arcpy.DeleteRows_management(geoPtFC) 
            ptinscur = arcpy.da.InsertCursor(geoPtFC,ptflds)
            ptcurflds= [f.name for f in arcpy.ListFields(geoPtFC)] # (lrte, [f.name for f in arcpy.ListFields(lrte)])
            print("Pt Cursor Flds : {}".format(ptcurflds))

        # layer names for the linear reference results
        rtevenTbl = "RteLinEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RteLinEvtFC"
        outFeatseed = "EvTbl"
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP EMP".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)



        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))


        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)


        # create the milepost insert cursor fields  
        mpflds = [RteFld.name,bmpFld.name,empFld.name,ofFld.name]
        
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        if 'lrte' in locals():
            del lrte            
        lrte = os.path.join('in_memory','rteselyr{}'.format(x1))
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        #lrterows = arcpy.da.SearchCursor(lrte, [f.name for f in arcpy.ListFields(lrte)]) # all fields in rte
        #rtelyr = "rteselyr" #os.path.join('in_memory','rteselyr')
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        #[print('{}, {}, {}'.format(row[0], row[2],row[1])) for row in lrterows]
        # get each point feature geometry
        rteMP = []
        stops = ""
            #print (" a {}  ".format(" test "))
        dirn = 1
        # delete previous route and mile post record if it exists
        if arcpy.Exists(mptbl): 
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)

        ptcoords = []
        for pt0 in listpts:
            ptcoords.append(pt0)
            inrow = [rteid,(pt0['x'],pt0['y'])]
            ptinscur.insertRow(inrow)            
                    
            # use the geopoint data to section the route
            if 'gevTbl' in locals():
                del gevTbl 
            #x1 = random.randrange(2001,3000,1)               
            gevTbl = os.path.join("in_memory","lnclptbl{}".format(x1))
            if arcpy.Exists(gevTbl):
                if int(arcpy.GetCount_management(gevTbl).getOutput(0)) > 0:
                    arcpy.DeleteRows_management(gevTbl)
            arcpy.LocateFeaturesAlongRoutes_lr(geoPtFC,lrte,fldrte,searange,gevTbl,eveProPts)
            # use LRS routines to generate section
        
            if 'mevRows' in locals():
                del mevRows 
            mevflds = [f.name for f in arcpy.ListFields(gevTbl)]    
            mevRows = arcpy.da.SearchCursor(gevTbl,mevflds )
            mpdata.clear()                                                                                                                                                                                                                                                                                                                                                                                                                            

            mp0 = -999
            offset = 0
            for mprow in mevRows:
                if mp0!=mprow[1]:
                    mpdata.append(mprow[1])
                    mp0 = mprow[1]

        return mpdata

def milepost2coords(lyrts,rteid,bmpvalx,offs,fldrte='Route'):
    if 'mptbl' in locals():
        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
    else:
        rtevenTbl = "RtePtEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RtePtEvtFC"
        outFeatseed = "EvTbl"
        x1 = 1001 #random.randrange(1001,2000,1)
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP EMP".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)
        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)
        # linear reference fields 
    bmpval = bmpvalx
    empval = bmpvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)<=0):
        if rteid == "5600":
            rteid="560"
        else:
            rteid="560"    
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)>0):
        rteFCSel = featlnclrte.save('in_memory','rtesel')
        ftlnclrte = featlnclrte.features
        rtegeo = ftlnclrte[0].geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        rtept2 = rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)
                
        if (bmpval<bmprte):
            bmpval=bmprte
        if (bmpval>emprte):
            bmpval=bmprte
    
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        arcpy.env.outputMFlag = "Disabled"
        lrte = os.path.join('in_memory','rteselyr')
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        # create the milepost insert cursor fields  
        mpflds = [RteFld.name,bmpFld.name,empFld.name,ofFld.name]
        # create the MilePost Insert cursor 
        mpinscur = arcpy.da.InsertCursor(mptbl, mpflds)  
        
        mpinscur.insertRow((rteid.upper(), bmpval,bmpval,offs))
        dirnlbl = 'LEFT'
        
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProPts, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
        # get the geoemtry from the result layer and append to the section feature class
        if arcpy.Exists(eveLinlyr):    
            cntLyr = arcpy.GetCount_management(eveLinlyr)
        if cntLyr.outputCount > 0:
            #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
            insecgeo = None
            # dynamic segementaiton result layer fields used to create the closure segment  
            lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'EMP', 'Shape@JSON']
            evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
            for srow in evelincur:
                #insecgeo = srow.getValue("SHAPE@")
                #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                rtenum = srow[1]
                insecgeo = arcgis.geometry.Geometry(srow[4])
                if insecgeo is None:
                    print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    insecgeo = geomrte.project_as(sprefwgs84).first_point
                else:
                    print('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    logger.info('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                if len(insecgeo)==0: # is None: 
                    insecgeo = rtegeo                 
                else:
                    insecgeo = insecgeo.project_as(sprefwgs84)
            del evelincur        
        del rteFCSel,lrte,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpval,empvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo.first_point)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None    
    return insecgeo

    


# In[ ]:


def webexsearch(mgis, title, owner_value, item_type_value, max_items_value=1000,inoutside=False):
    item_match = None
    search_result = mgis.content.search(query= "title:{} AND owner:{}".format(title,owner_value), 
                                          item_type=item_type_value, max_items=max_items_value, outside_org=inoutside)
    if "Imagery Layer" in item_type_value:
        item_type_value = item_type_value.replace("Imagery Layer", "Image Service")
    elif "Layer" in item_type_value:
        item_type_value = item_type_value.replace("Layer", "Service")
    
    for item in search_result:
        if item.title == title:
            item_match = item
            break
    return item_match

def lyrsearch(lyrlist, lyrname):
    lyr_match = None
   
    for lyr in lyrlist:
        if lyr.properties.name == lyrname:
            lyr_match = lyr
            break
    return lyr_match

def create_section(lyr, hdrow, chdrows,rtefeat):
    try:
        object_id = 1
        pline = geometry.Polyline(rtefeat)
        feature = features.Feature(
            geometry=pline[0],
            attributes={
                'OBJECTID': object_id,
                'PARK_NAME': 'My Park',
                'TRL_NAME': 'Foobar Trail',
                'ELEV_FT': '5000'
            }
        )

        lyr.edit_features(adds=[feature])
        #_map.draw(point)

    except Exception as e:
        print("Couldn't create the feature. {}".format(str(e)))
        

def fldvartxt(fldnm,fldtyp,fldnull,fldPrc,fldScl,fldleng,fldalnm,fldreq):
    fld = arcpy.Field()
    fld.name = fldnm
    fld.type = fldtyp
    fld.isNullable = fldnull
    fld.precision = fldPrc
    fld.scale = fldScl
    fld.length = fldleng
    fld.aliasName = fldalnm
    fld.required = fldreq
    return fld

def df_colsame(df):
    """ returns an empty data frame with the same column names and dtypes as df """
    #df0 = pd.DataFrame.spatial({i[0]: pd.Series(dtype=i[1]) for i in df.dtypes.iteritems()}, columns=df.dtypes.index)
    return df

def offdirn(closide,dirn1):
    if closide == 'Right':
        offdirn1 = 'RIGHT'
    elif closide == 'Left':
        offdirn1 = 'LEFT'
        dirn1 = -1*dirn1
    elif closide == 'Center':
        offdirn1 = 'RIGHT'
        dirn1 = 0.5
    elif closide == 'Both':
        offdirn1 = 'RIGHT'
        dirn1 = 0
    elif closide == 'Directional':
        if dirn1 == -1:
            offdirn1 = 'LEFT'
        else:
            offdirn1 = 'RIGHT'
    elif closide == 'Full' or closide == 'All':
        offdirn1 = 'RIGHT'
        dirn1 = 0
    elif closide == 'Shift':
        offdirn1 = 'RIGHT'
    elif closide == 'Local':
        offdirn1 = 'RIGHT'
    else:
        offdirn1 = 'RIGHT'
        dirn1 = 0 
    return offdirn1,dirn1

def deleteupdates(prjstlyrsrc, sectfeats):
    for x in prjstlyrsrc:
        print (" layer: {} ; from item : {} ; URL : {} ; Container : {} ".format(x,x.fromitem,x.url,x.container))
        if 'Projects' in (prjstlyrsrc):
            xfeats =  x.query().features
            if len(xfeats) > 0:
                if isinstance(xfeats,(list,tuple)):
                    if "OBJECTID" in xfeats[0].attributes:
                        oids = "'" + "','".join(str(xfs.attributes['OBJECTID']) for xfs in xfeats if 'OBJECTID' in xfs.attributes ) + "'"
                        oidqry = " OBJECTID in ({}) ".format(oids)
                    elif "OID" in xfeats[0].attributes:    
                        oids = "'" + "','".join(str(xfs.attributes['OID']) for xfs in xfeats if 'OID' in xfs.attributes ) + "'"
                        oidqry = " OID in ({}) ".format(oids)
                    print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
                    
                elif isinstance(xfeats,spedf):
                    if "OBJECTID" in xfeats.columns:
                        oids = "'" + "','".join(str(f1.get_value('OBJECTID')) for f1 in xfeats ) + "'"
                        oidqry = " OBJECTID in ({}) ".format(oids)
                    elif "OID" in xfeats.columns:    
                        oids = "'" + "','".join(str(f1.get_value('OID')) for f1 in xfeats ) + "'"
                        oidqry = " OID in ({}) ".format(oids)
                    print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
                    
                if 'None' in oids:
                    print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
                else:
                    x.delete_features(where=oidqry)

def delayerfeatures(x):
    xfeats =  x.query().features
    if len(xfeats) > 0:
        if isinstance(xfeats,(list,tuple)):
            if "OBJECTID" in xfeats[0].attributes:
                oids = "'" + "','".join(str(xfs.attributes['OBJECTID']) for xfs in xfeats if 'OBJECTID' in xfs.attributes ) + "'"
                oidqry = " OBJECTID in ({}) ".format(oids)
            elif "OID" in xfeats[0].attributes:    
                oids = "'" + "','".join(str(xfs.attributes['OID']) for xfs in xfeats if 'OID' in xfs.attributes ) + "'"
                oidqry = " OID in ({}) ".format(oids)
            print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
            
        elif isinstance(xfeats,spedf):
            if "OBJECTID" in xfeats.columns:
                oids = "'" + "','".join(str(f1.get_value('OBJECTID')) for f1 in xfeats ) + "'"
                oidqry = " OBJECTID in ({}) ".format(oids)
            elif "OID" in xfeats.columns:    
                oids = "'" + "','".join(str(f1.get_value('OID')) for f1 in xfeats ) + "'"
                oidqry = " OID in ({}) ".format(oids)
            print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
            
        if 'None' in oids:
            print (" from item : {} ; oids : {} ; ".format(x.fromitem,oids))
        else:
            x.delete_features(where=oidqry)
                    
                    
# Given anydate and n1 as 0 or 1 or 2 , etc  it computes Last Friday, First Friday and Second Friday, etc at 4PM
def fridaywk(bdate,n1):
    wkdte = datetime.strftime(bdate,"%w") # + datetime.strftime(bdate,"%z")
    date4pm = datetime.strptime(datetime.strftime(bdate,"%Y-%m-%d"),"%Y-%m-%d") + timedelta(hours=16)
    fr4pm= date4pm + timedelta(days=(5-int(wkdte)+(n1-1)*7))
    return fr4pm


def intextold(intxt,rte,rtename):
    intshortlbl = intxt['address']['ShortLabel']
    intsplitxt = intshortlbl.split(sep='&', maxsplit=1)
    txtret=intsplitxt[1]  # default to the second intersection unless the second one has the route
    for txt in intsplitxt:
        if rtename not in txt or rte not in txt:
            txtret = txt
    return txtret          

def intext(intxt,rte,rtename,fromtxt="Nothing"):
    intshortlbl = intxt['address']['ShortLabel']
    rtext = re.sub("-","",rte)
    if rtename is None:
        rtenametxt = 'Nothing'
    else:    
        rtenametxt = re.sub("-","",rtename)
    intsplitxt = intshortlbl.split(sep='&') #, maxsplit=1)
    intsplitxt = [t1.strip() for t1 in intsplitxt ]
    if len(intsplitxt)==2: 
        txtret=intsplitxt[1]  # default to the second intersection unless the second one has the route
    elif len(intsplitxt)==3:
        txtret=intsplitxt[2]  # default to the second intersection unless the second one has the route
    else:
        txtret=intsplitxt[0]  # default to the second intersection unless the second one has the route
            
    rtenmsplit = [ t2.strip() for t2 in rtenametxt.split(sep=" ")]
    if len(rtenmsplit)>2:
        rtenmsplit = "{} {}".format(rtenmsplit[0].capitalize(),rtenmsplit[1].capitalize())
    else:
        rtenmsplit = "{}".format(rtenmsplit[0].capitalize())
               
    for txt in intsplitxt:
        txtsep = txt.split(sep=" ")
        if len(txtsep)<=2 :
            if (txt[0:2]).isnumeric():
                txt = "Exit " + txt.upper()
        if rtenmsplit not in txt and rtext not in txt and fromtxt!=txt:
            txtret = txt
        else:
            txtret = txt
    return txtret          

def datemidnight(bdate):
    date0am = datetime.strptime(datetime.strftime(bdate,"%Y-%m-%d"),"%Y-%m-%d") + timedelta(hours=0)
    return date0am

# function to return whether the closure date range is a weekend or weekday
def wkend(b,e):
    if b==0 and e <=1: 
        return 1 
    elif b>=1 and b<=5 and e>=1 and e<=5: 
        return 0 
    elif b>=5 and (e==6 or e==0): 
        return 1 
    else: 
        return 0

def beginwk(bdate):
    wkdte = datetime.strftime(bdate,"%w")
    if (wkdte==0):
        bw = bdate + timedelta(days=wkdte)
    else:  # wkdte>=1:
        bw = bdate + timedelta(days=(7-wkdte))
    return bw

def beginthiswk(bdate):
    wkdte = datetime.strftime(bdate,"%w")
    if (wkdte==0):
        bw = bdate - timedelta(days=wkdte)
    else:  # wkdte>=1:
        bw = bdate - timedelta(days=(8-int(wkdte)))
    return bw    
                                                                                                                                                                                                                                                                                                                                                                                                                                                        
def midnextnight(bdate,n1):
    datenextam = datetime.strptime(datetime.strftime(bdate,"%Y-%m-%d"),"%Y-%m-%d") + timedelta(day=n1)
    return datenextam

#BeginDateName,EndDateName:  The month and the day portion of the begin or end date. (ex. November 23)
def dtemon(dte):
    dtext = datetime.strftime(dte-timedelta(hours=10),"%B") + " " +  str(int(datetime.strftime(dte-timedelta(hours=10),"%d")))
    return dtext

# BeginDay, EndDay: Weekday Name of the begin date (Monday, Tuesday, Wednesday, etc.)
def daytext(dte):
    dtext = datetime.strftime(dte-timedelta(hours=10),"%A") 
    return dtext

#BeginTime, EndTime: The time the lane closure begins.  12 hour format with A.M. or P.M. at the end
def hrtext(dte):
    hrtext = datetime.strftime(dte-timedelta(hours=10),"%I:%M %p") 
    return hrtext


def rtempt(lyrts,rtefc,lrte,bmpvalx,offs=0,fldrte='Route'):
    if 'mptbl' in locals():
        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
    else:
        rtevenTbl = "RtePtEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RtePtEvtFC"
        outFeatseed = "EvTbl"
        x1 = 1001 #random.randrange(1001,2000,1)
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP ".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)
        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)
        # linear reference fields 

    bmpval = bmpvalx
    empval = bmpvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    if (len(rtefc)>0):
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        mpinscur.insertRow((rteid.upper(), bmpval,offs))
        dirnlbl = 'LEFT'
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProPts, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
        # get the geoemtry from the result layer and append to the section feature class
        if arcpy.Exists(eveLinlyr):    
            cntLyr = arcpy.GetCount_management(eveLinlyr)
        if cntLyr.outputCount > 0:
            #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
            insecgeo = None
            # dynamic segementaiton result layer fields used to create the closure segment  
            lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'Shape@JSON']
            evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
            for srow in evelincur:
                #insecgeo = srow.getValue("SHAPE@")
                #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                rtenum = srow[1]
                insecgeo = arcgis.geometry.Geometry(srow[4])
                if insecgeo is None:
                    print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,bmpval,empval,offs ))
                    logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,bmpval,empval,offs ))
                    insecgeo = geomrte.project_as(sprefwgs84)
                else:
                    print('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,bmpval,empval,offs ))
                    logger.info('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,bmpval,empval,offs ))
                insecgeo = insecgeo.project_as(sprefwgs84)
            del evelincur        
        del rteFCSel,lrte,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} create point geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create point geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None    
    return insecgeo


def rtesectpt(lyrts,rteid,bmpvalx,offs,fldrte='Route'):
    if 'mptbl' in locals():
        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
    else:
        rtevenTbl = "RtePtEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RtePtEvtFC"
        outFeatseed = "EvTbl"
        x1 = 1001 #random.randrange(1001,2000,1)
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP EMP".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)
        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)
        # linear reference fields 
    bmpval = bmpvalx
    empval = bmpvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)<=0):
        if rteid == "5600":
            rteid="560"
        else:
            rteid="560"    
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)>0):
        rteFCSel = featlnclrte.save('in_memory','rtesel')
        ftlnclrte = featlnclrte.features
        rtegeo = ftlnclrte[0].geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        rtept2 = rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)
                
        if (bmpval<bmprte):
            bmpval=bmprte
        if (bmpval>emprte):
            bmpval=bmprte
    
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        arcpy.env.outputMFlag = "Disabled"
        lrte = os.path.join('in_memory','rteselyr')
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        # create the milepost insert cursor fields  
        mpflds = [RteFld.name,bmpFld.name,empFld.name,ofFld.name]
        # create the MilePost Insert cursor 
        mpinscur = arcpy.da.InsertCursor(mptbl, mpflds)  
        
        mpinscur.insertRow((rteid.upper(), bmpval,bmpval,offs))
        dirnlbl = 'LEFT'
        
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProPts, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
        # get the geoemtry from the result layer and append to the section feature class
        if arcpy.Exists(eveLinlyr):    
            cntLyr = arcpy.GetCount_management(eveLinlyr)
        if cntLyr.outputCount > 0:
            #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
            insecgeo = None
            # dynamic segementaiton result layer fields used to create the closure segment  
            lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'EMP', 'Shape@JSON']
            evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
            for srow in evelincur:
                #insecgeo = srow.getValue("SHAPE@")
                #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                rtenum = srow[1]
                insecgeo = arcgis.geometry.Geometry(srow[4])
                if insecgeo is None:
                    print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    insecgeo = geomrte.project_as(sprefwgs84).first_point
                else:
                    print('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    logger.info('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                insecgeo = insecgeo.project_as(sprefwgs84)
            del evelincur        
        del rteFCSel,lrte,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpval,empvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo.first_point)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None    
    return insecgeo

import numbers
import random
def testnumber(x):
    if any([isinstance(x,float),isinstance(x,int)]):
      return True
    else:
      return False
    
def multirtes(rtelyr,xRte,xBMP,xEMP,offs,rtelyrid,fldrte='Route',i1=-999):
    rteslist = xRte.split(sep='|')
    gx=[]
    print('Layer {} :  Route {} ; BMP : {} ; EMP : {} ; offset  : {} ; layer id {}.'.format(rtelyr,xRte,xBMP,xEMP,offs,rtelyrid ))
    
    for rte in rteslist:
        if len(rte)>0:
            gx = rtesectline(rtelyr,rte,xBMP,xEMP,offs,fldrte)
    return gx    
def rtesectline(lyrts,rteid,bmpvalx,empvalx,offs,fldrte='Route',i1=-999):
    sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
    sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }

    if 1==1 : #'mptbl' in locals():
        """        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
          else:   """
        rtevenTbl = "RtePtEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RtePtEvtFC"
        outFeatseed = "EvTbl"
        x1 = random.randrange(1001,2000,1)
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP EMP".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)
        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)
        # linear reference fields 
    bmpval = bmpvalx
    empval = empvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "{}_{}".format('lrtelyr',x1) #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)<=0):
        if rteid == "5600":
            rteid="560"
        else:
            rteid="560"    
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)>0):
        rteFCSel = featlnclrte.save('in_memory',"{}{}".format('rtesel',x1))
        ftlnclrte = featlnclrte.features
        rtegeo = ftlnclrte[0].geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rteleng = geomrte.get_length(method='PLANAR',units='METERS')
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        rtept2 = rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
# new addition 6/23/2020
        if (rtept1[2] == None):
            rtept1[2] = 0
            print('{} :  Route {} ; original BMP : None ;  Assigned BMP : {} .'.format(i1,rteid,rtept1[2] ))
            logger.info('{} : Route {} ; original BMP : None ;  Assigned BMP : {} .'.format(i1,rteid,rtept1[2] ))
        if (rtept2[2] == None):    
            rtept2[2] = round(rteleng*3.2808333/5280.0,3)
            print('{} :  Route {} ; original EMP :  Assigned ; Assigned EMP : {} .'.format(i1,rteid,rtept2[2] )) 
            logger.info('{} : Route {} ; original EMP : None ;  Assigned EMP : {} .'.format(i1,rteid,rtept2[2] )) 
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)
        #bmpval = pd.to_numeric(bmpval,errors='coerce')
        #empval = pd.to_numeric(empval,errors='coerce')
        if np.isnan(bmpval):
            print('{} : non numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            logger.info('{} : non numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            #return geomrte.project_as(sprefwgs84)
            bmpval = bmprte + 0.001
        else:
            print('{} : numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            #bmpval = bmprte + 0.001
        if np.isnan(empval):
            print('{} : non numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            logger.info('{} : non numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            if np.isnan(bmpval):
                empval = emprte - 0.001
            else:
                empval = bmpval + 0.02  # increased the minimum length becasue some sections were not generated
                empval = emprte - 0.001
        else:
            print('{} : numeric value on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(i1,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            
        if (empval<bmpval):
            inpval = empval
            empval=bmpval
            bmpval = inpval
        elif (round(empval,3)==0 and bmpval<=0):
            empval=bmpval + 0.02
                
        if (bmpval<bmprte):
            bmpval=bmprte
        if (bmpval>emprte):
            bmpval=emprte-0.02
            empval = emprte
        if (empval>emprte):
            empval=emprte
    
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        arcpy.env.outputMFlag = "Disabled"
        lrte = os.path.join('in_memory','rteselyr')
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        # create the milepost insert cursor fields  
        mpflds = [RteFld.name,bmpFld.name,empFld.name,ofFld.name]
        # create the MilePost Insert cursor 
        mpinscur = arcpy.da.InsertCursor(mptbl, mpflds)  
        rtes = rteid.split('?')
        if len(rtes)>1:
            for rte in rtes:
                if len(rte)>0:
                    mpinscur.insertRow((rte.upper(), bmpval,empval,offs))
            print(' multiple routes entered for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            logger.info(' multiple routes entered for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        else:            
            mpinscur.insertRow((rteid.upper(), bmpval,empval,offs))
               
        dirnlbl = 'LEFT'
        
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        arcpy.env.outputMFlag = "Disabled"
        lrte = os.path.join('in_memory','rteselyr{}'.format(x1))
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        
        if (abs(empval-bmpval)<0.02):
            bmpval=max(bmpval,empval)-0.01
            empval=bmpval+0.02
        if len(rtes)>1:
            for rte in rtes:
                if len(rte)>0:
                    mpinscur.insertRow((rte.upper(), bmpval,empval,offs))
            print(' multiple routes entered for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
            logger.info(' multiple routes entered for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        else:            
            mpinscur.insertRow((rteid.upper(), bmpval,empval,offs))
        #mpinscur.insertRow((rteid.upper(), bmpval,empval,offs))
        print('\n geometry generation for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        logger.info('\n geometry generation for Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        dirnlbl = 'LEFT'
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProLines, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
        # get the geoemtry from the result layer and append to the section feature class
        if arcpy.Exists(eveLinlyr):    
            cntLyr = arcpy.GetCount_management(eveLinlyr)
        if cntLyr.outputCount > 0:
            #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
            insecgeo = None
            # dynamic segementaiton result layer fields used to create the closure segment  
            lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'EMP', 'Shape@JSON']
            evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
            for srow in evelincur:
                #insecgeo = srow.getValue("SHAPE@")
                #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                rtenum = srow[1]
                insecgeo = arcgis.geometry.Geometry(srow[4])
                #print(' geometry : {} type {} ; for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(insecgeo,type(insecgeo),lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                if not insecgeo:
                    print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    # use two mile posts to generate two coordinate and draw a line geometry
                    mplist = [bmpval,empval]
                    offs=0
                    mpres = []
                    mpts = []
                    for m1 in mplist:
                        ptres= milepost2coords(lyrts,rtenum,m1,offs,fldrte)
                        print('milepost2coords returned  type : {} ; data  : {} ; on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(type(ptres),ptres,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        logger.info('milepost2coords returned type : {} ; data : {} ; on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(type(ptres),ptres,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        if type(ptres) is None:
                            ptres = rtept1  
                        elif str(type(ptres)) != "<class 'dict'>":
                            print('milepost2coords returned {} geometry : {} ; on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(type(ptres),ptres,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                            logger.info('milepost2coords returned {} geometry : {} ; on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(type(ptres),ptres,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                            ptres = ptres.first_point
                        mpres.append (ptres)
                        if len(ptres) == 0:
                            ptres = {'x': -157.05356057262688, 'y': 21.1357042336581, 'spatialReference': {'wkid': 4326, 'latestWkid': 4326}} 
                        mpts.append([ptres.x,ptres.y, m1]) # (  [lambda x :  for m1 in mplist:
                        srpt = ptres.spatial_reference
                    #line = { "paths" : [ [xb,yb],[xe,ye]], "spatialReference" : {"wkid" : 4326}}    
                    line = {'hasM': True, 'paths': [ mpts ], "spatialReference" : srpt}
                    pline = arcgis.geometry.Polyline(line) #sectgeom = Geometry([[xb,yb],[xe,ye]])
                    print('Polyline : {} for Rte {}'.format(pline,rtenum,mplist))
                    insecgeo = pline
                    if not insecgeo: 
                        insecgeo =  geomrte # arcgis.geometry.Geometry(geomrte)
                else:
                    #print('created Shape : {} for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {} .'.format(insecgeo,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    logger.info('created Shape : {} for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {} .'.format(insecgeo,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                print('Procesing Shape : {} for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {} .'.format(insecgeo,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                insecgeo = insecgeo.project_as(sprefwgs84)
            del evelincur        
        del rteFCSel,lrte,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None
    print('returned Geometry : {} for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {} .'.format(insecgeo,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
    return insecgeo

def three2twod(shp):
    if shp is not None:
        mgeom = shp['paths']
        glen = len(mgeom) # rtepaths[0][len(rtepaths[0])-1] 
        smupltxt = ""
        if glen>0:
            smupline = []
            for il,linex in enumerate(mgeom,0):
                for xy in linex:
                    xylist = []
                    for i,x in enumerate(xy,1):
                        if i==1:
                            xylist.append(x)
                        elif i==2:
                            xylist.append(x)
                    smupline.append(xylist)
        smuplinef = [smupline]
    else:
        smuplinef = []
    return smuplinef


def rtesectmp(lyrts,rteid,bmpvalx,empvalx,offs):
    if 'mptbl' in locals():
        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
    bmpval = bmpvalx
    empval = empvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    rtegeo = None
    lyrname = lyrts.properties.name
    featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)<=0):
        if rteid == "5600":
            rteid="560"
        else:
            rteid="560"    
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)>0):
        rteFCSel = featlnclrte.save('in_memory','rtesel')
        ftlnclrte = featlnclrte.features
        rtegeo = ftlnclrte[0].geometry
        geomrte = deepcopy(rtegeo) # arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        rtept2 = rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
        bmprte = rtept1[2]
        emprte = rtept2[2]
        if bmprte==None or emprte==None:
            insecgeo = three2twod(rtegeo)
            #insecgeo = Geometry({ "paths" : insecgeo , "spatialReference" : sprefwebaux })
            insecgeo =arcgis.geometry.Geometry({ "paths" : insecgeo , "spatialReference" : sprefwebaux }) #(insecgeo,sr=sprefwebaux)
            lengeo = insecgeo.length
            insecgeo = insecgeo.project_as(sprefwgs84 ) #sprefwebaux) #insecgeo.project_as(sprefwgs84)
#            print('Route {} ; Rte pre-geometry {} ; projected {} ; new {}  ; length : {} ; layer {} , rte {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format
#                  (rteid,rtegeo,geomrte,insecgeo,lengeo,lyrname,rteid,bmpvalx,empvalx,bmprte,emprte,offs ))
#           logger.info('Route {} ; Rte pre-geometry {} ; projected {} ; new {}  ; length : {} ; layer {} , rte {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format
#                  (rteid,rtegeo,geomrte,insecgeo,lengeo,lyrname,rteid,bmpvalx,empvalx,bmprte,emprte,offs ))
        else:
            bmprte = round(rtept1[2],3)
            emprte = round(rtept2[2],3)
            if (empval<bmpval):
                inpval = empval
                empval=bmpval
                bmpval = inpval
            elif (round(empval,3)==0 and bmpval<=0):
                empval=bmpval + 0.01
                    
            if (bmpval<bmprte):
                bmpval=bmprte
            if (bmpval>emprte):
                bmpval=bmprte
            if (empval>emprte):
                empval=emprte
    
            #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
            arcpy.env.outputMFlag = "Disabled"
            lrte = os.path.join('in_memory','rteselyr')
            arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
            flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
            lrterows = arcpy.da.SearchCursor(lrte,flds)
            
            if (abs(empval-bmpval)<0.01):
                bmpval=max(bmpval,empval)-0.005
                empval=bmpval+0.01
            mpinscur.insertRow((rteid.upper(), bmpval,empval,offs))
            dirnlbl = 'LEFT'
            arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProLines, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
            # get the geoemtry from the result layer and append to the section feature class
            if arcpy.Exists(eveLinlyr):    
                cntLyr = arcpy.GetCount_management(eveLinlyr)
            if cntLyr.outputCount > 0:
                #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
                insecgeo = None
                # dynamic segementaiton result layer fields used to create the closure segment  
                lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'EMP', 'Shape@JSON']
                evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
                for srow in evelincur:
                    #insecgeo = srow.getValue("SHAPE@")
                    #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                    rtenum = srow[1]
                    insecgeo = arcgis.geometry.Geometry(srow[4])
                    if insecgeo == None:
                        print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        insecgeo = geomrte.project_as(sprefwgs84)
                    else:
                        #print('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        #logger.info('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                        insecgeo = insecgeo.project_as(sprefwgs84)
                del evelincur,lrte        
        del rteFCSel,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrname,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=rtegeo    
    #print('Layer {} ; Route {} created section geometry {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,insecgeo,bmpvalx,empvalx,bmpval,empval,offs ))
    return insecgeo

def rtesectmpo(lyrts,rteid,bmpvalx,empvalx,offs,fldrte):
    if 'mptbl' in locals():
        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
    else:
        rtevenTbl = "RtePolyEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RtePolyEvtFC"
        outFeatseed = "EvTbl"
        x1 = 1001 #random.randrange(1001,2000,1)
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        #fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP EMP".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)
        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)

    bmpval = bmpvalx
    empval = empvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)<=0):
        if rteid == "5600":
            rteid="560"
        else:
            rteid="560"    
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)>0):
        rteFCSel = featlnclrte.save('in_memory','rtesel')
        ftlnclrte = featlnclrte.features
        rtegeo = ftlnclrte[0].geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        rtept2 = rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)
        if (empval<bmpval):
            inpval = empval
            empval=bmpval
            bmpval = inpval
        elif (round(empval,3)==0 and bmpval<=0):
            empval=bmpval + 0.01
                
        if (bmpval<bmprte):
            bmpval=bmprte
        if (bmpval>emprte):
            bmpval=bmprte
        if (empval>emprte):
            empval=emprte
    
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        arcpy.env.outputMFlag = "Disabled"
        lrte = os.path.join('in_memory','rteselyr')
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        
        if (abs(empval-bmpval)<0.01):
            bmpval=max(bmpval,empval)-0.005
            empval=bmpval+0.01
        # create the MilePost Insert cursor 
        mpflds = [RteFld.name,bmpFld.name,empFld.name,ofFld.name]
        
        mpinscur = arcpy.da.InsertCursor(mptbl, mpflds)  
            
        mpinscur.insertRow((rteid.upper(), bmpval,empval,offs))
        dirnlbl = 'LEFT'
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProLines, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
        # get the geoemtry from the result layer and append to the section feature class
        if arcpy.Exists(eveLinlyr):    
            cntLyr = arcpy.GetCount_management(eveLinlyr)
        if cntLyr.outputCount > 0:
            #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
            insecgeo = None
            # dynamic segementaiton result layer fields used to create the closure segment  
            lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'EMP', 'Shape@JSON']
            evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
            for srow in evelincur:
                #insecgeo = srow.getValue("SHAPE@")
                #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                rtenum = srow[1]
                insecgeo = arcgis.geometry.Geometry(srow[4])
                #print(' geometry : {} for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(insecgeo,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                
                if insecgeo is None:
                    print('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    logger.info('Not able to create section geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    insecgeo = geomrte.project_as(sprefwgs84)
                else:
                    print('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                    logger.info('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
                insecgeo = insecgeo.project_as(sprefwgs84)
            del evelincur        
        del rteFCSel,lrte,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None    
    return insecgeo

def mergeometry(geomfeat):
    mgeom = geomfeat.geometry
    if len(geomfeat)>0:
        rtegeo = geomfeat.geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        glen = len(rtepaths) # rtepaths[0][len(rtepaths[0])-1] 
        rtept2 = rtepaths[glen-1][len(rtepaths[glen-1])-1] #geomrte.last_point
        mgeom =[ [ x for sublist in rtepaths for x in sublist] ]
    return mgeom

def geom3d2d(geomfeat):
    mgeom = geomfeat.geometry
    if len(geomfeat)>0:
        rtegeo = geomfeat.geometry
        rtepaths = rtegeo['paths']
        
        rtept1 = rtepaths[0][0] # geomrte.first_point
        glen = len(rtepaths) # rtepaths[0][len(rtepaths[0])-1] 
        rtept2 = rtepaths[glen-1][len(rtepaths[glen-1])-1] #geomrte.last_point
        mgeom =[ [ x for sublist in rtepaths for x in sublist] ]
    return mgeom

# Remove M values from multiline arcgis shape geometry 
def shpxmeasure(shp):
    slinetxt = ""
    if shp is not None:
        mgeom = shp['paths']
        glen = len(mgeom) # rtepaths[0][len(rtepaths[0])-1] 
        if glen>0:
            shp0 = []
            for il,linex in enumerate(mgeom,0):
                shp1 = []
                for xy in linex:
                    shp2 = []
                    xylist = ""
                    for i,x in enumerate(xy,1):
                        if i==1:
                            xylist = str(x)
                        elif i==2:
                            xylist = xylist + " , " + str(x)
                    shp2.append(xylist)
            shp1.append(shp2)
        shp0.append(shp1)       
    else:
        shp0 = "[]"
    slinetxt = "LineString {}".format(shp)
    #slinetxt = slinetxt.replace("'","").replace("[","(").replace("]",")")            
    return slinetxt



# generate multi-geometric list from an arcgis multi-geometry feature
def xmergeometry(geomfeat):
    mgeom = geomfeat.geometry
    if len(geomfeat)>0:
        rtegeo = geomfeat.geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        glen = len(rtepaths) # rtepaths[0][len(rtepaths[0])-1] 
        rtept2 = rtepaths[glen-1][len(rtepaths[glen-1])-1] #geomrte.last_point
        mgeom =[ [ x for sublist in rtepaths for x in sublist] ]
    return mgeom

# generate multi-geometric list from an arcgis multi-geometry feature
def featmergeometry(geomfeat):
    mgeom = geomfeat.geometry
    if len(geomfeat)>0:
        rtegeo = geomfeat.geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        glen = len(rtepaths) # rtepaths[0][len(rtepaths[0])-1] 
        rtept2 = rtepaths[glen-1][len(rtepaths[glen-1])-1] #geomrte.last_point
        mgeom =[ [ x for sublist in rtepaths for x in sublist] ]
    return mgeom

# generate single geometric list from an arcgis multi-geometry paths 
def xmergeometry(geompaths):
    mgeom = geompaths
    glen = len(geompaths) # rtepaths[0][len(rtepaths[0])-1] 
    if glen>0:
        mgeom =[ x for sublist in geompaths for x in sublist]
    return mgeom

# convert the esri multiline paths to soctrata multiline 
# MULTILINESTRING ((10 10, 20 20, 10 40),(40 40, 30 30, 40 20, 30 10))
def socratamultilinegeom(geompaths):
    mgeom = geompaths
    glen = len(geompaths) # rtepaths[0][len(rtepaths[0])-1] 
    smupltxt = ""
    if glen>0:
        smupline = []
        for il,linex in enumerate(geompaths,0):
            smupline.append([])
            for xy in linex:
                xylist = ""
                for i,x in enumerate(xy,1):
                    if i==1:
                        xylist = str(x)
                    elif i==2:
                        xylist = xylist + " " + str(x)
                smupline[il].append(xylist)
    smupltxt = "MultiLineString {}".format(smupline)
    smupltxt = smupltxt.replace("'","").replace("[","(").replace("]",")")            
    return smupltxt

# convert the esri multiline to soctrata multiline 
# MULTILINESTRING ((10 10, 20 20, 10 40),(40 40, 30 30, 40 20, 30 10))
def socratamultilineshp(shp):
    if shp is not None:
        mgeom = shp['paths']
        glen = len(mgeom) # rtepaths[0][len(rtepaths[0])-1] 
        smupltxt = ""
        if glen>0:
            smupline = []
            for il,linex in enumerate(mgeom,0):
                smupline.append([])
                for xy in linex:
                    xylist = ""
                    for i,x in enumerate(xy,1):
                        if i==1:
                            xylist = str(x)
                        elif i==2:
                            xylist = xylist + " " + str(x)
                    smupline[il].append(xylist)
    else:
        smupline = ""
    smupltxt = "MultiLineString {}".format(smupline)
    smupltxt = smupltxt.replace("'","").replace("[","(").replace("]",")")            
    return smupltxt

# generate single socrata line from an arcgis multiline shape geometry 
def soclineshp(shp):
    slinetxt = ""
    if shp is not None:
        mgeom = shp['paths']
        glen = len(mgeom) # rtepaths[0][len(rtepaths[0])-1] 
        if glen>0:
            socline = []
            for il,linex in enumerate(mgeom,0):
                for xy in linex:
                    xylist = ""
                    for i,x in enumerate(xy,1):
                        if i==1:
                            xylist = str(x)
                        elif i==2:
                            xylist = xylist + " " + str(x)
                    socline.append(xylist)
    else:
        socline = ""
    slinetxt = "LineString {}".format(socline)
    slinetxt = slinetxt.replace("'","").replace("[","(").replace("]",")")            
    return slinetxt


def assyncadds(lyr1,fset):
    sucs1=0
    pres = None
    t1 = 0
    while(sucs1<=0 and t1<10):
        pres = lyr1.edit_features(adds=fset) #.append(prjfset) #.append(prjfset,field_mappings=fldmaprj)
        if pres['addResults'][0]['success']==True:
            sucs1=1
        else:
            t1 += 1
            sleep(7)
    return pres

def assyncaddspt(lyr1,fset):
    sucs1=0
    pres = None
    t1 = 0
    while(sucs1<=0 and t1<5):
        pres = lyr1.edit_features(adds=fset) #.append(prjfset) #.append(prjfset,field_mappings=fldmaprj)
        if pres['addResults'][0]['success']==True:
            sucs1=1
        else:
            t1 += 1
            sleep(5)
    return pres

def assyncedits(lyr1,fset):
    sucs1=0
    errcnt = 0
    pres = None
    while(round(sucs1)==0):
        pres = lyr1.edit_features(updates=fset) #.append(prjfset) #.append(prjfset,field_mappings=fldmaprj)
        if pres['updateResults'][0]['success']==True:
            sucs1=1
        else:
            errcnt+=1
            terr = datetime.datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p")
            logger.error("Attempt {} at {} ; Result : {} ; Layer {} ; attributes {} ; geometry {} ".format(errcnt,terr, pres,lyr.properties.name,fset.features[0].attributes,fset.features[0].geometry))
            #if errcnt<=10:
            sleep(7)
            #else:    
            #    sucs1 = -1
    return pres


def qryhistdate(bdate,d1=0):
    dateqry = datetime.strftime((bdate-timedelta(days=d1)),"%m-%d-%Y")
    return dateqry
 
    
def searchcontentbytimestamp(input_days):
    # UTC time
    now_dt = datetime.datetime.utcnow()
    then_dt = now_dt - timedelta(days=int(input_days))

    # construct the string for range search, see ESRI doc for string format
    now = '000000'+str(int(now_dt.timestamp()))+'000'
    then = '000000'+str(int(then_dt.timestamp()))+'000'

    items = gis.content.search(
     query = 'uploaded: [' + then + ' TO ' + now + ']', 
     max_items=10000
    )

    # sort the items by modified date
    items2 = sorted(items,key=lambda item:item.modified)

    for item in items2:
        str_time = datetime.datetime.fromtimestamp(item.modified/1000).strftime('%Y-%m-%d %H:%M:%S')
        print("Modified Time:{0}, Title:{1}".format(str_time,item.title))


    return items2




def pts2mpost(lyrtes,rteid,listpts,fldrte,searange,spref):
    mpdata = []
    featlnclrte = lyrts.query(where = "{} in  ({}{}{}) ".format(fldrte," '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if 'rteFCSel' in locals():
        del rteFCSel            
    ftlnclrte = featlnclrte.features
    if (len(ftlnclrte)>0):
        rtegeo = ftlnclrte[0].geometry
        rtegeo['spatialReference'] = featlnclrte.spatial_reference
        geomrte = arcgis.geometry.Geometry(rtegeo)
        rteleng = geomrte.get_length(method='PLANAR',units='METERS')
        rtepaths = rtegeo['paths']
        # eliminate the gaps merge the paths 
        rtept1 = rtepaths[0][0] # geomrte.first_point
        glen = len(rtepaths) # rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
        rtept2 = rtepaths[glen-1][len(rtepaths[glen-1])-1]
        # new addition 6/8/2020
        if (rtept1[2] == None):
            rtept1[2] = 0
        if (rtept2[2] == None):    
            rtept2[2] = round(rteleng*3.2808333/5280.0,3)  # assuming route length is in meters
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)
        rtegeox = [[ x for sublist in rtepaths for x in sublist]]
        rtegeo['paths'] =  rtegeox
        featlnclrte.features[0].geometry['paths'] = rtegeox
        print("Rte {} ; Bmp : {} ; emp : {} ;  has {} sections; Search Range {} ".format(rteid,bmprte,emprte,glen,searange))
        has_m = "DISABLED"
        has_z = "DISABLED"
        geotype = "POINT"
        x1 = 1001 #random.randrange(1001,2000,1)
        outFeatseed = "EvTbl"
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1)
        # linear reference fields 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        
        # geopoint featureclass to store the lane closure locations 
        geoPtFC = arcpy.CreateFeatureclass_management("in_memory", lrsGeoPTbl, geotype,spatial_reference=arcpy.SpatialReference(spref['wkid']))#,'',has_m, has_z,spref) #.getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        arcpy.AddField_management(geoPtFC, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(geoPtFC, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(geoPtFC, empFld.name, empFld.type, empFld.precision, empFld.scale)
        geoPtFCnm = "{}".format(geoPtFC)
        ptflds = [RteFld.name,"SHAPE@XY"]
        rteFCSel = featlnclrte.save('in_memory','rtefcsel{}'.format(x1))
        if 'geoPtFC' in locals():
            if arcpy.Exists(geoPtFC):
                if int(arcpy.GetCount_management(geoPtFC).getOutput(0)) > 0:
                    arcpy.DeleteRows_management(geoPtFC) 
            ptinscur = arcpy.da.InsertCursor(geoPtFC,ptflds)
            ptcurflds= [f.name for f in arcpy.ListFields(geoPtFC)] # (lrte, [f.name for f in arcpy.ListFields(lrte)])
            print("Pt Cursor Flds : {}".format(ptcurflds))

        # layer names for the linear reference results
        rtevenTbl = "RteLinEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RteLinEvtFC"
        outFeatseed = "EvTbl"
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP EMP".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)



        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))


        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)


        # create the milepost insert cursor fields  
        mpflds = [RteFld.name,bmpFld.name,empFld.name,ofFld.name]
        
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        if 'lrte' in locals():
            del lrte            
        lrte = os.path.join('in_memory','rteselyr{}'.format(x1))
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        #lrterows = arcpy.da.SearchCursor(lrte, [f.name for f in arcpy.ListFields(lrte)]) # all fields in rte
        #rtelyr = "rteselyr" #os.path.join('in_memory','rteselyr')
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        #[print('{}, {}, {}'.format(row[0], row[2],row[1])) for row in lrterows]
        # get each point feature geometry
        rteMP = []
        stops = ""
            #print (" a {}  ".format(" test "))
        dirn = 1
        # delete previous route and mile post record if it exists
        if arcpy.Exists(mptbl): 
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)

        ptcoords = []
        for pt0 in listpts:
            ptcoords.append(pt0)
            inrow = [rteid,(pt0['x'],pt0['y'])]
            ptinscur.insertRow(inrow)            
                    
            # use the geopoint data to section the route
            if 'gevTbl' in locals():
                del gevTbl 
            #x1 = random.randrange(2001,3000,1)               
            gevTbl = os.path.join("in_memory","lnclptbl{}".format(x1))
            if arcpy.Exists(gevTbl):
                if int(arcpy.GetCount_management(gevTbl).getOutput(0)) > 0:
                    arcpy.DeleteRows_management(gevTbl)
            arcpy.LocateFeaturesAlongRoutes_lr(geoPtFC,lrte,fldrte,searange,gevTbl,eveProPts)
            # use LRS routines to generate section
        
            if 'mevRows' in locals():
                del mevRows 
            mevflds = [f.name for f in arcpy.ListFields(gevTbl)]    
            mevRows = arcpy.da.SearchCursor(gevTbl,mevflds )
            mpdata.clear()                                                                                                                                                                                                                                                                                                                                                                                                                            

            mp0 = -999
            offset = 0
            for mprow in mevRows:
                if mp0!=mprow[1]:
                    mpdata.append(mprow[1])
                    mp0 = mprow[1]

        return mpdata

def milepost2coords(lyrts,rteid,bmpvalx,offs,fldrte='Route'):
    if 'mptbl' in locals():
        if arcpy.Exists(mptbl):    
            if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
                arcpy.DeleteRows_management(mptbl)
    else:
        rtevenTbl = "RtePtEvents"
        eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
        eveLRSFC = "RtePtEvtFC"
        outFeatseed = "EvTbl"
        x1 = random.randrange(1001,2000,1) # 1001 #
        lrsGeoPTbl = """LRS_{}{}""".format(outFeatseed,x1) # DynaSeg result feature table created from LRS points location along routes 
        outfeatbl = """Rt{}""".format(outFeatseed) 
        OidFld = fldvartxt("ObjectID","LONG",False,28,"","","OID",True) 
        # create the bmp and direction field for the merged result table 
        RteFld = fldvartxt(fldrte,"TEXT",False,"","",60,fldrte,True) 
        fldrte = RteFld.name
        # create the bmp and direction field for the merged result table 
        bmpFld = fldvartxt("BMP","DOUBLE",False,18,11,"","BMP",True) 

        # create the emp and direction field for the result table 
        #empFld = arcpy.Field()
        empFld = fldvartxt("EMP","DOUBLE",True,18,11,"","EMP",False) 
        ofFld = fldvartxt("Offset","DOUBLE",True,18,11,"","Offset",False) 
        # linear reference link properties 
        eveProPts = "{} POINT BMP EMP".format(fldrte)
        eveProLines = "{} LINE BMP EMP".format(fldrte)
        mptbl = str(arcpy.CreateTable_management("in_memory","{}{}".format(rtevenTbl,x1)).getOutput(0))
        # add BMP , EMP and RteDirn fields to the linear reference lane closure table
        #arcpy.AddField_management(mptbl, OidFld.name, OidFld.type, OidFld.precision, OidFld.scale)
        arcpy.AddField_management(mptbl, RteFld.name, RteFld.type, RteFld.precision, RteFld.scale)
        arcpy.AddField_management(mptbl, bmpFld.name, bmpFld.type, bmpFld.precision, bmpFld.scale)
        arcpy.AddField_management(mptbl, empFld.name, empFld.type, empFld.precision, empFld.scale)
        arcpy.AddField_management(mptbl, ofFld.name, ofFld.type, ofFld.precision, ofFld.scale)
        # linear reference fields 
    bmpval = bmpvalx
    empval = bmpvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "lrtelyr{}".format(x1) #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)<=0):
        if rteid == "5600":
            rteid="560"
        else:
            rteid="560"    
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteid,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featlnclrte)>0):
        rteFCSel = featlnclrte.save('in_memory','rtesel{}'.format(x1))
        ftlnclrte = featlnclrte.features
        rtegeo = ftlnclrte[0].geometry
        geomrte = arcgis.geometry.Geometry(rtegeo,sr=sprefwebaux)
        rtepaths = rtegeo['paths']
        rtept1 = rtepaths[0][0] # geomrte.first_point
        rtept2 = rtepaths[0][len(rtepaths[0])-1] #geomrte.last_point
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)
                
        if (bmpval<bmprte):
            bmpval=bmprte
        if (bmpval>emprte):
            bmpval=bmprte
    
        #rteFCSel = featlnclrte.save(lcfgdboutpath,'rtesel')
        arcpy.env.outputMFlag = "Disabled"
        lrte = os.path.join('in_memory','rteselyr{}'.format(x1))
        arcpy.CreateRoutes_lr(rteFCSel,RteFld.name, lrte, "TWO_FIELDS", bmpFld.name, empFld.name)
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        # create the milepost insert cursor fields  
        mpflds = [RteFld.name,bmpFld.name,empFld.name,ofFld.name]
        # create the MilePost Insert cursor 
        mpinscur = arcpy.da.InsertCursor(mptbl, mpflds)  
        
        mpinscur.insertRow((rteid.upper(), bmpval,bmpval,offs))
        dirnlbl = 'LEFT'
        
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProPts, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
        # get the geoemtry from the result layer and append to the section feature class
        if arcpy.Exists(eveLinlyr):    
            cntLyr = arcpy.GetCount_management(eveLinlyr)
        if cntLyr.outputCount > 0:
            #lrsectfldnms = [ f.name for f in arcpy.ListFields(eveLinlyr)]
            insecgeo = None
            # dynamic segementaiton result layer fields used to create the closure segment  
            lrsectfldnms = ['ObjectID', 'Route', 'BMP', 'EMP', 'Shape@JSON']
            evelincur = arcpy.da.SearchCursor(eveLinlyr,lrsectfldnms)
            for srow in evelincur:
                #insecgeo = srow.getValue("SHAPE@")
                #print("id : {} , Rte : {} , BMP {} , EMP : {} , Geom : {} ".format(srow[0],srow[1],srow[2],srow[3],srow[4]))
                rtenum = srow[1]
                insecgeo = arcgis.geometry.Geometry(srow[4])
                if insecgeo is None:
                    print('Not able to create event geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    logger.info('Not able to create event geometry for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    insecgeo = {'x': -157.05356057262688, 'y': 21.1357042336581, 'spatialReference': {'wkid': 4326, 'latestWkid': 4326}} #geomrte.project_as(sprefwgs84).first_point
                else:
                    print('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                    logger.info('created project section for layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
                try: # if insecgeo is not None:
                    insecgeo = insecgeo.project_as(sprefwgs84)
                    print("Created Point Rte {} ; BMP : {} ; Geometry {} ".format(srow[1],BMPVal,srow[4]))
                except Exception as e:
                    print("Couldn't create Point feature. {} ; Rte : {} ; Geometry {} ".format(str(e),srow[1],srow[4]))
                    insecgeo = {'x': -157.05356057262688, 'y': 21.1357042336581, 'spatialReference': {'wkid': 4326, 'latestWkid': 4326}} #geomrte.project_as(sprefwgs84).first_point

            del evelincur        
        del rteFCSel,lrte,rtevenTbl  
    else:
        rteidx = "460"  # Molokaii route 0 to 15.55 mileage
        print('Route {} not found using {} create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,empval,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpval,empvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo[0][0])
            if insecgeo is not None:
                insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None    
    return insecgeo

    


# In[ ]:


infilenm = r'Interstate Poor Pavement Projects FY21-24 Updated.xlsx' # 'Repair_Recon_Sites_20201217V3.xlsx'
xlSPavefile = os.path.join(inpath,infilenm)
sht = 'projectlocations'
print ("xls path {} ; Sheet  : {} . ".format(xlSPavefile, sht) )
SPaveRoutespdf = pd.read_excel(xlSPavefile, sht)
print ("sheet {} ; PDF  : {} ; with rows  : {} . ".format(sht, SPaveRoutespdf.columns , len(SPaveRoutespdf)) )


# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, os
plt.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


disfilenm = r'Raw_Data_Distress2021_Interstates_SR.xlsx' # 'Repair_Recon_Sites_20201217V3.xlsx'
disPavefile = os.path.join(inpath,disfilenm)
disht = 'Raw_Data_Distress2021_Interstat'
print ("xls path {} ; Sheet  : {} . ".format(disPavefile, disht) )
disPaveRoutespdf = pd.read_excel(disPavefile, disht)
print ("sheet {} ; PDF  : {} ; with rows  : {} . ".format(disht, disPaveRoutespdf.columns , len(disPaveRoutespdf)) )


# In[ ]:


# clean out column names
discolnms = disPaveRoutespdf.columns
disanecols = []
for col in discolnms:
    col=col.replace(' ','_')
    disanecols.append(col.split(',')[0])
print ("pre cols {} ; new cols   : {} . ".format(discolnms ,disanecols))


# In[ ]:


print('\nImport the 2021 condition collected in the first quarter of 2021 by Mandli\n')
print ("-"*35 + "General Information" +'-'*(70 - len('General Information')))
print ("shape(Rows x Columns) = " + str(disPaveRoutespdf.shape))
print ("size(# of cells) = " + str(disPaveRoutespdf.size))
print ("-"*35+ "Column Names" +'-'*(70 - len('Column Names')))
disPaveRoutespdf.columns = disanecols
print (disPaveRoutespdf.columns)
print ("-"*35 + "Column Type Counts" +'-'*(70 - len('Column Type Counts')))
print ("Colums Types : {}".format(disPaveRoutespdf.dtypes.value_counts()))
#print ("-"*35 + "Column Types" +'-'*(70 - len('Column Types')))
#print(df.dtypes)
print ("Dataframe Description: {}".format(disPaveRoutespdf.describe()))
#df.head()
#infilenm = r'Interstate Poor Pavement Projects FY21-24 Updated.xlsx' # 'Repair_Recon_Sites_20201217V3.xlsx'


# In[ ]:


selcols = ['PKEY','ROUTE','PAVETYPE','BMP','EMP','BRIDGE_LTH','CONST_LTH','LNDEV_LTH','RR_LTH','SPDBP_LTH', 'TUNNEL_LTH','SOURCE', 'LRM_NAME', 'DELIVERYID', 'HPMS_IRI_C', 'HPMS_RUT_C', 'HPMS_FLT_C', 'HPMS_PCT_C', 'HPMS_COND','HPMS_Through_Lanes', 'Miles', 'LaneMiles']

disPaveRoutespdfc = disPaveRoutespdf[(disPaveRoutespdf['LANE_ID'] == 'SIN') & (disPaveRoutespdf['DIRECTION'] == 'Positive')] [selcols]

disPaveRoutespdfc['Non_Pavement_Length'] = disPaveRoutespdfc['BRIDGE_LTH']+disPaveRoutespdfc['TUNNEL_LTH']+ disPaveRoutespdfc['CONST_LTH']+disPaveRoutespdfc['LNDEV_LTH']+disPaveRoutespdfc['RR_LTH']+disPaveRoutespdfc['SPDBP_LTH']
disPaveRoutespdfc['Weighted_Pavement_Length'] = disPaveRoutespdfc.apply(lambda x : (x['Miles']-x['Non_Pavement_Length']/5280)*x['HPMS_Through_Lanes'],axis=1)
disPaveRoutespdfco = deepcopy(disPaveRoutespdfc) #.copy()
print("Columns {}".format(disPaveRoutespdfco.columns))


# In[ ]:


Total = disPaveRoutespdfco.groupby(by=['HPMS_COND']).sum()['Weighted_Pavement_Length'].sum()
Good = disPaveRoutespdfco.groupby(by=['HPMS_COND']).sum()['Weighted_Pavement_Length']['GOOD']
Fair = disPaveRoutespdfco.groupby(by=['HPMS_COND']).sum()['Weighted_Pavement_Length']['FAIR']
Poor = disPaveRoutespdfco.groupby(by=['HPMS_COND']).sum()['Weighted_Pavement_Length']['POOR']

Good_p = Good/Total * 100
Fair_p = Fair/Total * 100
Poor_p = Poor/Total * 100

print ('This is the 2021 condition collected in the first quarter of 2021. This condition does not include the H-2 Grinding Project')
print ('\nTotal Interstate pavement  is %.2f lane mile \n Good Pavement is %.2f lane mile\n Fair Pavement is %.2f lane mile\n Poor Pavement is %.2f lane mile ' %(Total,Good,Fair,Poor))
print ('\nPercent Good Pavement is %.2f%% \nPercent Fair Pavement is %.2f%% \nPercent Poor Pavement is %.2f%%' %(Good_p,Fair_p,Poor_p))


# In[ ]:


disPaveRoutespdfcox = deepcopy(disPaveRoutespdfco)
Total = disPaveRoutespdfcox.groupby(by=['HPMS_COND'],as_index=False).sum()['Weighted_Pavement_Length'].sum()
disPaveRoutespdfcoxs = disPaveRoutespdfcox.groupby(by=['HPMS_COND'],as_index=False).sum()

#disPaveRoutespdfcoxs= disPaveRoutespdfcoxs.apply(lambda x: x/Total*100) 

print ('This is the 2021 condition collected in the first quarter of 2021. This condition does not include the H-2 Grinding Project')
print ('\nTotal Interstate {} Pavement in lane miles\n {} '.format(list(disPaveRoutespdfcoxs.keys()),disPaveRoutespdfcoxs.value_counts()))
#print ('\nTotal Interstate Good Pavement in lane miles\n {} '.format(disPaveRoutespdfcoxs['PctRating'].value_counts()))


# In[ ]:


plt.figure(figsize = (8,8))
colorz = ['#73977D','#F2B749', '#C33B49']
plt.title('2021 Estimated Percent Conditon before H-2 Grinding', fontdict={'fontsize': 14, 'weight':'bold'})
plt.pie([Good_p,Fair_p,Poor_p], labels = ['Good','Fair','Poor'],autopct='%1.2f%%',colors = colorz,
              textprops={'fontsize': 12, 'color':'white','weight':'bold'})
plt.legend()
plt.show()


# In[ ]:


disPaveRoutespdfcop = deepcopy(disPaveRoutespdfco)
print ('These are the scope of H-2 Grinding, and the Poor should become Fair(or Good) after the H-2 Grinding')
disPaveRoutespdfcop[
    (disPaveRoutespdfcop['ROUTE'] == 'H-2')&
    (disPaveRoutespdfcop['BMP'] >= 1.8)&
    (disPaveRoutespdfcop['BMP'] <= 2.8)&
    (disPaveRoutespdfcop['HPMS_COND'] == 'POOR')]


# In[ ]:


disPaveRoutespdfcop = deepcopy(disPaveRoutespdfco)
print ('These are the scope of H-2 Grinding, and the Poor should become Fair(or Good) after the H-2 Grinding')
disPaveRoutespdfcop.loc[
    (disPaveRoutespdfcop['ROUTE'] == 'H-2')&
    (disPaveRoutespdfcop['BMP'] >= 1.8)&
    (disPaveRoutespdfcop['BMP'] <= 2.8) &
    (disPaveRoutespdfcop['HPMS_COND'] == 'POOR'),'HPMS_COND'] = 'FAIR'


# In[ ]:


print ('These are the scope of H-2 Grinding, and the Poor should become Fair(or Good) after the H-2 Grinding')
disPaveRoutespdfcop[
    (disPaveRoutespdfcop['ROUTE'] == 'H-2')&
    (disPaveRoutespdfcop['BMP'] >= 1.8)&
    (disPaveRoutespdfcop['BMP'] <= 2.8)&
    (disPaveRoutespdfcop['HPMS_COND'] == 'POOR')]


# In[ ]:


Total = disPaveRoutespdfcop.groupby(by=['HPMS_COND']).sum()['Weighted_Pavement_Length'].sum()
Good = disPaveRoutespdfcop.groupby(by=['HPMS_COND']).sum()['Weighted_Pavement_Length']['GOOD']
Fair = disPaveRoutespdfcop.groupby(by=['HPMS_COND']).sum()['Weighted_Pavement_Length']['FAIR']
Poor = disPaveRoutespdfcop.groupby(by=['HPMS_COND']).sum()['Weighted_Pavement_Length']['POOR']

Good_p = Good/Total * 100
Fair_p = Fair/Total * 100
Poor_p = Poor/Total * 100

print ('This is the 2021 condition collected in the first quarter of 2021. This condition does not include the H-2 Grinding Project')
print ('\nTotal Interstate pavement  is %.2f lane mile \n Good Pavement is %.2f lane mile\n Fair Pavement is %.2f lane mile\n Poor Pavement is %.2f lane mile ' %(Total,Good,Fair,Poor))
print ('\nPercent Good Pavement is %.2f%% \nPercent Fair Pavement is %.2f%% \nPercent Poor Pavement is %.2f%%' %(Good_p,Fair_p,Poor_p))


# In[ ]:


plt.figure(figsize = (8,8))
colorz = ['#73977D','#F2B749', '#C33B49']
plt.title('2021 Estimated Percent Conditon after H-2 Grinding', fontdict={'fontsize': 14, 'weight':'bold'})
plt.pie([Good_p,Fair_p,Poor_p], labels = ['Good','Fair','Poor'],autopct='%1.2f%%',colors = colorz,
              textprops={'fontsize': 12, 'color':'white','weight':'bold'})
plt.legend()
plt.show()


# In[ ]:


#import arcgis
#from arcgis.gis import GIS

# ArcGIS user credentials to authenticate against the portal
#credentials = { 'userName' : 'dot_gbelleau', 'passWord' : '*******'} 
#userName = credentials['userName'] # arcpy.GetParameter(2) # 
#passWord =  credentials['passWord'] #  # arcpy.GetParameter(3) # "
# Address of your ArcGIS portal
#portal_url = r"http://histategis.maps.arcgis.com/"
#print("Connecting to {}".format(portal_url))
#gis = GIS(portal_url, userName, passWord)
#shpxmeasure(routesdf['SHAPE'].head(0)) 
#print ("{}".format(routesdf.columns)) 
#print ("{}".format(routesdf['SHAPE'].head(0))) 
SPaveFSTitle = 'HiDOT Pavement Project Limits' # arcpy.GetParameter(0) 
itypeHISPavesrc= "Feature Service" #  "Feature Layer" # "Feature Service" #   # "Service Definition"
HISPavenm = 'HiDOT Pavement Project Limits'
HISPaveLyrnm = 'HiDOT Pavement Project Routes'
inoutside = False
max_items_value= 1000
#equsgsmap = qgis.content.get("31cfc5b138e24dee866c457948773ac4")
#print("Title : {} - type : {} ; created  : {} - {} ; Modified : {} - {} ".format(equsgsmap.title,equsgsmap.type,equsgsmap.created,datetime.fromtimestamp(equsgsmap.created/1e3),equsgsmap.modified,datetime.fromtimestamp(equsgsmap.modified/1e3)))
#for item in equsgsmap:
#    print("Item : {}".format(item))
search_result = qgis.content.search(query= "title:{} AND owner:{}".format(SPaveFSTitle,userName), 
                                          item_type=itypeHISPavesrc, max_items=max_items_value, outside_org=inoutside)
print("Title : {} - type : {} ; found   : {} ".format(SPaveFSTitle,itypeHISPavesrc,search_result))


# In[ ]:


#import arcgis
#from arcgis.gis import GIS

# ArcGIS user credentials to authenticate against the portal
#credentials = { 'userName' : 'dot_gbelleau', 'passWord' : '*******'} 
#userName = credentials['userName'] # arcpy.GetParameter(2) # 
#passWord =  credentials['passWord'] #  # arcpy.GetParameter(3) # "
# Address of your ArcGIS portal
#portal_url = r"http://histategis.maps.arcgis.com/"
#print("Connecting to {}".format(portal_url))
#gis = GIS(portal_url, userName, passWord)
#shpxmeasure(routesdf['SHAPE'].head(0)) 
#print ("{}".format(routesdf.columns)) 
#print ("{}".format(routesdf['SHAPE'].head(0))) 
SPaveFSTitle = 'HiDOT Interstate Pavement Project Limits' # arcpy.GetParameter(0) 
itypeHISPavesrc= "Feature Service" #  "Feature Layer" # "Feature Service" #   # "Service Definition"
HISPavenm = 'HiDOT Interstate Pavement Project Limits'
HISPaveLyrnm = 'HiDOT Interstate Routes Pavement Project'
inoutside = False
max_items_value= 1000
#equsgsmap = qgis.content.get("31cfc5b138e24dee866c457948773ac4")
#print("Title : {} - type : {} ; created  : {} - {} ; Modified : {} - {} ".format(equsgsmap.title,equsgsmap.type,equsgsmap.created,datetime.fromtimestamp(equsgsmap.created/1e3),equsgsmap.modified,datetime.fromtimestamp(equsgsmap.modified/1e3)))
#for item in equsgsmap:
#    print("Item : {}".format(item))
search_result = qgis.content.search(query= "title:{} AND owner:{}".format(SPaveFSTitle,userName), 
                                          item_type=itypeHISPavesrc, max_items=max_items_value, outside_org=inoutside)
print("Title : {} - type : {} ; found   : {} ".format(SPaveFSTitle,itypeHISPavesrc,search_result))


# In[ ]:


# ArcGIS to Socrata Dataframe Setup


# get the date and time
curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S") 
# convert unixtime to local time zone
#x1=1547062200000
#tbeg = datetime.date.today().strftime("%A, %d. %B %Y %I:%M%p")
tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p")
#tlocal = datetime.fromtimestamp(x1/1e3 , tzlocal.get_localzone())

x = random.randrange(0,1000,1)               
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }

# ID or Title of the feature service to update
#featureService_ID = '9243138b20f74429b63f4bd81f59bbc9' # arcpy.GetParameter(0) #  "3fcf2749dc394f7f9ecb053771669fc4" "30614eb4dd6c4d319a05c6f82b049315" # "c507f60f298944dbbfcae3005ad56bc4"
SPaveFSTitle = 'HiDOT Pavement Project Limits' # arcpy.GetParameter(0) 
itypeHISPavesrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
HISPavenm = 'HiDOT Pavement Project Limits'
HISPaveLyrnm = 'Pavement Preservation Limits'

hirtsTitle = 'HIDOTRoutes' # arcpy.GetParameter(0) #  'e9a9bcb9fad34f8280321e946e207378'
itypelrts="Feature Service" # "Feature Layer" # "Service Definition"
wmlrtsnm = 'HIDOTRoutes'
rteFCSelNm = 'rtesel'
servicename =  SPaveFSTitle # "HiDOT_Fatal_HISPaveh_Entry" # 
tempPath = sys.path[0]
arcpy.env.overwriteOutput = True

logger.info("Title : {} Geometry Processing begins at {} ".format(SPaveFSTitle,tbeg))                                                                                                                                                                                                                                                                                                                                                                                   
print("Title : {}  Geometry Processing begins at {} ".format(SPaveFSTitle,tbeg))                                                                                                                                                                                                                                                                                                                                                                                   

#print("Temp path : {}".format(tempPath))
# ArcGIS user credentials to authenticate against the portal
credentials = { 'userName' : 'dot_mmekuria', 'passWord' : '********'}
userName = credentials['userName'] # arcpy.GetParameter(2) # 
passWord = credentials['passWord'] # "ChrisMaz" #  # arcpy.GetParameter(3) # "ChrisMaz"
#credentials = { 'userName' : arcpy.GetParameter(4), 'passWord' : arcpy.GetParameter(5)}
# Address of your ArcGIS portal
#portal_url = r"http://histategis.maps.arcgis.com/"
#print("Connecting to {}".format(portal_url))
#qgis = GIS(portal_url, userName, passWord)
#qgis = GIS(profile="hisagolprof")
numfs = 1000 # number of items to query
#    sdItem = qgis.content.get(lcwebmapid)
ekOrg = False

#prjstatusFSTitle = 'HIDOTProjectStatusGeometries' # 'HIDOTProjectStatusLayers' #  'HIDOTProjectStatus' #   arcpy.GetParameter(0) 
itype="Feature Service" # "Feature Layer" # "Service Definition"
servtype = 'featureService'
print (" Query if {} layer exists as {}. ".format (SPaveFSTitle,itype))
logger.info (" Query if {} layer exists as {}. ".format (SPaveFSTitle,itype))
prjlyrdelist = "['{}']".format(SPaveFSTitle)
#    sdItem = qgis.content.get(lcwebmapid)
# search for maintenance source data
print("Searching for feature source {} from {} item for user {} and Service Title {} on AGOL...".format(itype,portal_url,userName,servicename))
logger.info("Searching for lane closure source {} from {} item for user {} and Service Title {} on AGOL...".format(itype,portal_url,userName,servicename))
HISPavesrc = webexsearch(qgis, servicename, userName, itype,numfs,ekOrg)
#qgis.content.search(query="title:{} AND owner:{}".format(prjstSrcFSTitle, userName), item_type=itype,outside_org=False,max_items=numfs) #[0]
#print (" Content search result : {} ; ".format(HISPavesrc))
if HISPavesrc != None:
    print (" Feature URL: {} ; Title : {} ; Id : {} ".format(HISPavesrc.url,HISPavesrc.title,HISPavesrc.id))
    logger.info (" Feature URL: {} ; Title : {} ; Id : {} ".format(HISPavesrc.url,HISPavesrc.title,HISPavesrc.id))
else:
    print (" Feature : {} ; with layer  : {} does not exist. ".format(servicename ,HISPavenm))
    logger.info (" Feature : {} ; with layer  : {} does not exist. ".format(servicename,HISPavenm))
    


# In[ ]:


# ArcGIS to Socrata Dataframe Setup


# get the date and time
curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S") 
# convert unixtime to local time zone
#x1=1547062200000
#tbeg = datetime.date.today().strftime("%A, %d. %B %Y %I:%M%p")
tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p")
#tlocal = datetime.fromtimestamp(x1/1e3 , tzlocal.get_localzone())

x = random.randrange(0,1000,1)               
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }

# ID or Title of the feature service to update
#featureService_ID = '9243138b20f74429b63f4bd81f59bbc9' # arcpy.GetParameter(0) #  "3fcf2749dc394f7f9ecb053771669fc4" "30614eb4dd6c4d319a05c6f82b049315" # "c507f60f298944dbbfcae3005ad56bc4"
SPaveFSTitle = 'HiDOT Interstate Pavement Project Limits' # arcpy.GetParameter(0) 
itypeHISPavesrc= "Feature Service" #  "Feature Layer" # "Feature Service" #   # "Service Definition"
HISPavenm = 'HiDOT Interstate Pavement Project Limits'
HISPaveLyrnm = 'HiDOT Interstate Routes Pavement Project'

hirtsTitle = 'HIDOTRoutes' # arcpy.GetParameter(0) #  'e9a9bcb9fad34f8280321e946e207378'
itypelrts="Feature Service" # "Feature Layer" # "Service Definition"
wmlrtsnm = 'HIDOTRoutes'
rteFCSelNm = 'rtesel'
servicename =  SPaveFSTitle # "HiDOT_Fatal_HISPaveh_Entry" # 
tempPath = sys.path[0]
arcpy.env.overwriteOutput = True

logger.info("Title : {} Geometry Processing begins at {} ".format(SPaveFSTitle,tbeg))                                                                                                                                                                                                                                                                                                                                                                                   
print("Title : {}  Geometry Processing begins at {} ".format(SPaveFSTitle,tbeg))                                                                                                                                                                                                                                                                                                                                                                                   

#print("Temp path : {}".format(tempPath))
# ArcGIS user credentials to authenticate against the portal
credentials = { 'userName' : 'dot_mmekuria', 'passWord' : '********'}
userName = credentials['userName'] # arcpy.GetParameter(2) # 
passWord = credentials['passWord'] # "ChrisMaz" #  # arcpy.GetParameter(3) # "ChrisMaz"
#credentials = { 'userName' : arcpy.GetParameter(4), 'passWord' : arcpy.GetParameter(5)}
# Address of your ArcGIS portal
#portal_url = r"http://histategis.maps.arcgis.com/"
#print("Connecting to {}".format(portal_url))
#qgis = GIS(portal_url, userName, passWord)
#qgis = GIS(profile="hisagolprof")
numfs = 1000 # number of items to query
#    sdItem = qgis.content.get(lcwebmapid)
ekOrg = False

#prjstatusFSTitle = 'HIDOTProjectStatusGeometries' # 'HIDOTProjectStatusLayers' #  'HIDOTProjectStatus' #   arcpy.GetParameter(0) 
itype="Feature Service" # "Feature Layer" # "Service Definition"
servtype = 'featureService'
print (" Query if {} layer exists as {}. ".format (SPaveFSTitle,itype))
logger.info (" Query if {} layer exists as {}. ".format (SPaveFSTitle,itype))
prjlyrdelist = "['{}']".format(SPaveFSTitle)
#    sdItem = qgis.content.get(lcwebmapid)
# search for maintenance source data
print("Searching for feature source {} from {} item for user {} and Service Title {} on AGOL...".format(itype,portal_url,userName,servicename))
logger.info("Searching for lane closure source {} from {} item for user {} and Service Title {} on AGOL...".format(itype,portal_url,userName,servicename))
HISPavesrc = webexsearch(qgis, servicename, userName, itype,numfs,ekOrg)
#qgis.content.search(query="title:{} AND owner:{}".format(prjstSrcFSTitle, userName), item_type=itype,outside_org=False,max_items=numfs) #[0]
#print (" Content search result : {} ; ".format(HISPavesrc))
if HISPavesrc != None:
    print (" Feature URL: {} ; Title : {} ; Id : {} ".format(HISPavesrc.url,HISPavesrc.title,HISPavesrc.id))
    logger.info (" Feature URL: {} ; Title : {} ; Id : {} ".format(HISPavesrc.url,HISPavesrc.title,HISPavesrc.id))
else:
    print (" Feature : {} ; with layer  : {} does not exist. ".format(servicename ,HISPavenm))
    logger.info (" Feature : {} ; with layer  : {} does not exist. ".format(servicename,HISPavenm))
    


# In[ ]:


# Use data from Pandas Dataframe disPaveRoutespdfcop
SPavesdf = deepcopy(disPaveRoutespdfcop)
print (" PDF Columns : {} ; with columns  : {} . ".format( SPavesdf.columns , len(SPavesdf.columns)) )
SPavedf.group_by(['PKEY', 'ROUTE', 'PAVETYPE', 'BMP', 'EMP', 'BRIDGE_LTH', 'CONST_LTH',
       'LNDEV_LTH', 'RR_LTH', 'SPDBP_LTH', 'TUNNEL_LTH', 'SOURCE', 'LRM_NAME',
       'DELIVERYID', 'HPMS_IRI_C', 'HPMS_RUT_C', 'HPMS_FLT_C', 'HPMS_PCT_C',
       'HPMS_COND', 'HPMS_Through_Lanes'])


# In[ ]:


bmpcol = 'BMP'
empcol = 'EMP'
rteid = 'ROUTE'
qrycol = rteid
rtelyrid = 'HiDOTRoutes'
offs = 0
qrykey = ''
#print("{}".format(SPavesdf[qrycol].head(1)))
qrystr = "{} != '{}'".format(qrycol,qrykey)
routesdf = deepcopy(SPavesdf) #.query(qrystr)
listrtes = routesdf[rteid].value_counts()
print ("number of SPave Routes entered with {} = {} ; Routes : {} ; Counts : {}".format(qrystr,len(routesdf),list(listrtes.keys()),list(listrtes.values)))
logger.info ("number of SPave Routes entered with {} = {} ; Routes : {} ; Counts : {}".format(qrystr,len(routesdf),list(listrtes.keys()),list(listrtes.values)))
l=0
fldstring = [rteid,'PKEY','PAVETYPE', 'HPMS_COND']
fldfloat = ['BMP','EMP']
routesdf = routesdf.astype({col:float for col in fldfloat},errors='ignore')
routesdf = routesdf.astype({col:str for col in fldstring},errors='ignore')
"""
coldates = [ ] #coldates = ['Event_Approx_Start_Date','Event_Approx_End_Date','State_Orig_Emergency_Proclam_Date',
#            'Fed_Disaster_Declar_Date','Rpr_Restor_NTP_Date','Rpr_Restor_Completion_Date']
for coln in routesdf.columns:
    routesdf[coln] = routesdf[coln].replace(r'\%?', value='', regex=False)
#for coln in coldates:#
    routesdf[coln] = pd.to_datetime(routesdf[coln],format="%Y-%m-%d %H:%M:%S", errors='coerce')
fldfloat = ['BMP','EMP']
for coln in fldfloat:
    routesdf[coln] = pd.to_numeric(routesdf[coln],errors='coerce',downcast='float')

for coln in fldstring:
    routesdf[coln] = routesdf[coln].astype(str)

    
for coln in routesdf.columns:
    routesdf[coln] = routesdf[coln].replace('nan', '') #, regex=True)

#qrystr = "{} != '{}'".format(qrycol,qrykey)
#routesdf = routesdf.query(qrystr)
"""
listrtes = routesdf[rteid].value_counts()
    
print ("number of SPave Routes entered after transfromation ; Routes : {} ; Counts : {} ; Values : {} \n Data : {}".format(len(routesdf),list(listrtes.keys()),list(listrtes.values),routesdf))
logger.info ("number of SPave Routes entered after transfromation ; Routes : {} ; Counts : {} ; Values : {} \n Data : {}".format(len(routesdf),list(listrtes.keys()),list(listrtes.values),routesdf))


# In[ ]:


def regsub(x,cmpx=r'[?\n+]'):
    if x is None:
        return x
    return re.sub(cmpx, '|',x)

rtekeys = list(listrtes.keys())
print(rtekeys)
rtekeys0  = [ regsub(str(y)) for y in rtekeys ] #   (re.sub(r'[\n+]', '|',rtekeys))
print(rtekeys0)
rtekomp1 = re.compile(r'[?+]')  #  r'0-9a-zA-Z\-') #,(rtekeys))
#print(re.sub(rtekomp, '',rtekeys))
rtekeys1  = (re.sub(rtekomp1, '',str(rtekeys0)))
print(rtekeys1)
rtekomp2 = re.compile(r'[\n+](?=[0-9])')  #  r'0-9a-zA-Z\-') #,(rtekeys))
rtekeys2  = (re.sub(r'(\n+)', '|',rtekeys1))
print(rtekeys2)
cmpy = re.compile(r'[?\n+]')  #  r'0-9a-zA-Z\-') #,(rtekeys))
routesdf[rteid] = routesdf[rteid].apply(lambda x : regsub(x,cmpy)) 
listrtes = routesdf[rteid].value_counts()
print ("number of HiDOT SPave Routes entered with {} = {} ; Routes : {} ; Counts : {}".format(cmpy,len(routesdf),list(listrtes.keys()),list(listrtes.values)))
logger.info ("number of HiDOT SPave Routes entered with {} = {} ; Routes : {} ; Counts : {}".format(cmpy,len(routesdf),list(listrtes.keys()),list(listrtes.values)))


# In[ ]:


print(routesdf[rteid].value_counts())
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
print("{}".format(routesdf.dtypes))

routeydf = deepcopy(routesdf)  #routesdf.rename (columns=SPaverenamecols,inplace=False)
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
print(routeydf[rteid].value_counts())
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')

print(routesdf)
#routesdf[rteid] =routesdf.astype({rteid: 'str'}).dtypes 


# In[ ]:


# access the route feature layer , search for route source data
itypeHISPavesrc= "Feature Service" # "Feature Layer" #   # "Service Definition"

print("Searching for route source {} from {} item for Service Title {} on AGOL...".format(itypeHISPavesrc,portal_url,hirtsTitle))
fsroutesrc = webexsearch(qgis, hirtsTitle, userName, itypeHISPavesrc,numfs,ekOrg)
#qgis.content.search(query="title:{} AND owner:{}".format(SPaveFSTitle, userName), item_type=itypeHISPavesrc,outside_org=False,max_items=numfs) #[0]
print (" Feature URL: {} ; Title : {} ; Id : {} ".format(fsroutesrc.url,fsroutesrc.title,fsroutesrc.id))
lyroutesrc = fsroutesrc.layers
# header layer
rtelyr = lyrsearch(lyroutesrc, wmlrtsnm)
print (" Feature : {} ; name : {} ; Id : {} ".format(wmlrtsnm,rtelyr.properties.name,rtelyr))


# In[ ]:


#print("{}".format(routesdf[qrycol].head(1)))
bmpcol = 'BMP'
empcol = 'EMP'
rteid = 'Route'
rteidpdf = 'ROUTE'
qrycol = rteid

rtelyrid = 'HiDOTRoutes'
offs = 0
qrykey = ''
qrystr = "{} != '{}'".format(qrycol,qrykey)
#routeydf = deepcopy(routesdf)
print ("number of Pavement Routes with {} = {} and routes{} ".format(qrystr,len(routeydf),routeydf[rteidpdf].to_list()))
logger.info ("number of Routes entered with {} = {} and routes{} ".format(qrystr,len(routeydf),routeydf[rteidpdf].to_list()))
#routeydf['SHAPE']= routeydf.apply(lambda x : multirtes(rtelyr,str(x[rteid]),x[bmpcol],x[empcol],offs,rtelyrid),axis=1)
routeydf['SHAPE']= routeydf.apply(lambda x : rtesectline(rtelyr,x[rteidpdf],x[bmpcol],x[empcol],offs),axis=1) #(rtelyr,rte,xBMP,xEMP,offs,fldrte)
print ("SDF coumns {} and total count {}".format(routeydf.columns,len(routeydf.columns),routeydf['SHAPE'].head(1)))

print(routeydf[rteidpdf].value_counts(rteidpdf))
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
SPavecsvnm = r'HiDOT Pavement Project Limitsy.csv'
SPavesdfile = os.path.join(inpath,SPavecsvnm)
routeydf.to_csv(SPavesdfile)
print("{}".format((routeydf.dtypes)))


# In[ ]:


fldrte='Route'
offset=0
# Process geometry
# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print (" dataframe type  : {}  ".format(type(routeydf)))
#idx= pd.Index(projsw2ysdf) #(ignore_index=True)  for concat
# delete existing data first
#SPaverenamecols = {'Route' : 'Route'}
SPavesdf = deepcopy(routeydf)
#SPavesdf.rename (columns=SPaverenamecols,inplace=True)
SPavegeoac = gac(SPavesdf)
SPavewgs84 =  SPavegeoac.set_geometry('SHAPE',sr=sprefwgs84)
#SPavewgs84 =  SPavegeoac.project(sprefwgs84)

#SPavesw2ysdfx = gac.from_df(routesdf,  sr=sprefwgs84, geometry_column='SHAPE')
#SPavegeoacx = gac(SPavesw2ysdfx)
SPavefeats = SPavegeoac.to_featureset()
print (" features length : {} ; feature {} ".format(len(SPavefeats),SPavefeats))


# In[ ]:


# if layer data does not exist import fresh data into ArcGIS from excel
itypeHISPavesrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
SPaveFSTitle = 'HiDOT Interstate Pavement Project Limits' # arcpy.GetParameter(0) 
itypeHISPavesrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
HISPavenm = 'Interstate Pavement Preservation Limits' #'HiDOTSPaveORTP2045 Project Limits'
HISPaveLyrnm = 'Interstate Pavement Preservation Limits'

try:
    #curDate = strftime("%Y%m%d%H%M%S") 
    userName= "dot_mmekuria"
    if HISPavesrc != None:
        print (" Feature URL: {} ; Title : {} ; Id : {} ".format(HISPavesrc.url,HISPavesrc.title,HISPavesrc.id))
        logger.info (" Feature URL: {} ; Title : {} ; Id : {} ".format(HISPavesrc.url,HISPavesrc.title,HISPavesrc.id))
        # ID or Title of the feature service to update
        #print (" Content search result : {} ; ".format(fsprjstsrc))
        SPavelyrs = HISPavesrc.layers
        lyrnamelist = [ x.properties.name for i1,x in enumerate(SPavelyrs,1)]
        # header layer
        fs = len(SPavelyrs) #len(lyrtefs)
        if (fs>0):
            SPavelyr = lyrsearch(SPavelyrs, HISPavenm)
        else:
            print (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(HISPavenm,HISPavesrc.title,HISPavesrc.id,lyrnamelist))
            logger.info (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(HISPavenm,HISPavesrc.title,HISPavesrc.id,lyrnamelist))
            
    else:
        print (" Feature : {} ; with layer  : {} does not exist. ".format(servicename ,HISPavenm))
        logger.info (" Feature : {} ; with layer  : {} does not exist. ".format(servicename,HISPavenm))
        SPavelyr = SPavegeoac.to_featurelayer(title=HISPavenm, gis=qgis, tags='Projects, HDOT,Pavement, Routes', folder=None)
        print(" layer : {} created ".format(SPavelyr))
        emergefcol = SPavegeoac.to_feature_collection(name="{}_col".format(HISPavenm), drawing_info=None, extent=None, global_id_field=None)
        
    print (" Feature URL: {} ; Title : {} ; Id : {} \n Layers - {}  ".format(HISPavesrc.url,HISPavesrc.title,HISPavesrc.id,lyrnamelist))
    logger.info (" Feature URL: {} ; Title : {} ; Id : {} \n Layers - {} ".format(HISPavesrc.url,HISPavesrc.title,HISPavesrc.id,lyrnamelist))
except Exception as e:
    print(' Error : {} ;   layer {} Project status script '.format(str(e),HISPavenm))
    logger.error(' Error : {} ;  layer {} Project status script '.format(str(e),HISPavenm ))


# In[ ]:


import ipywidgets as widgets

def calc_dist(moahu, g):
    print("Computing length of drawn polyline...")
    length = lengths(g['spatialReference'], [g], "", "geodesic")
    print("Length: " + str(length[0]) + " m.")
    return g


#SPavelyr = SPavegeoac.to_featurelayer(title=(SPaveintnm+'_test'), gis=qgis, tags='projects, pss, HDOT, maintenance, repair', folder=None)

# text box widget
emap = qgis.map("Oahu,Hawaii")
#emap.extent = SPavelyr.properties.extent
emap
#emap.add_layer(SPavelyr)
# Set calc_dist as the callback function to be invoked when a polyline is drawn on the map
emap.on_draw_end(calc_dist)

location = widgets.Text(value='Honolulu, Hawaii', placeholder='Honolulu, Hawaii',
                        description='Location:', disabled=False)

# command button widget
gobtn = widgets.Button(description='Go', disabled=False,
                       button_style='', tooltip='Go', icon='check')

# define what happens whent the command button is clicked
def on_gobutton_clicked(b):
    global df
    global emap
    global oldslider
    
    # geocode the place name and set that as the map's extent
    area = arcgis.geocoding.geocode(location.value)[0]
    emap.extent = area['extent']
    #df = filter_images()
    
gobtn.on_click(on_gobutton_clicked)

location_items = [location, gobtn]
widgets.HBox(location_items)
emap


# In[ ]:


# if layer data does not exist import fresh data into ArcGIS from excel
itypeHISPavesrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
SPaveFSTitle = 'HiDOT Interstate Pavement Project Limits' # arcpy.GetParameter(0) 
itypeHISPavesrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
HISPavenm = 'Interstate Pavement Preservation Limits' #'HiDOTSPaveORTP2045 Project Limits'
HISPaveLyrnm = 'Interstate Pavement Preservation Limits'


if HISPavesrc != None:

    # process the mile post data into geometry 
    # HISPave layers
    fHISPavenm = HISPavenm
    HISPavelyr = lyrsearch(HISPavesrc, fHISPavenm)
    if HISPavelyr != None:
        HISPavedf = HISPavelyr.query(as_df=True)
        HISPaveflds = [fd.name for fd in HISPavelyr.properties.fields]

    #'msgbox tdate
        datesectqry = "{} {}".format(fHISPavenm, HISPaveflds)

        print ("SPave Query {} ; {} number of SPave Routes {} ".format(datesectqry,HISPavedf['RoadType'].value_counts(),len(HISPavedf)))

        qrycol = 'Route'

        qrykey = ''
        qrystr = "{} != '{}'".format(qrycol,qrykey)
        milepostdf = HISPavedf.query(qrystr)
        print ("number of SPave Routes entered with {} = {}".format(qrystr,len(milepostdf)))
    #logpath = r"D:\MyFiles\HWYAP\HISPavees\logs"
    #rptpath = r"D:\MyFiles\HWYAP\HISPavees\reports"

        rptname = "HISPaveDataMilePost.csv"
        csvfile = os.path.join(rptpath, rptname)
        milepostdf.to_csv(csvfile)
    else:
        print ("SPave Source {} ; does not contain layer named {} ; Query Result  {} ".format(HISPavesrc, fHISPavenm,HISPavelyr))
        
    #for srow in  milepostdf:
    


# In[ ]:


print(routesdf[rteid].value_counts())
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
print("{}".format(routesdf.dtypes))

print(routesdf['Route'].value_counts())
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
print(routeydf['Route'].value_counts())
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')


type(routesdf)
#routesdf[rteid] =routesdf.astype({rteid: 'str'}).dtypes 


# In[ ]:


coldates = [ ] #coldates = ['Event_Approx_Start_Date','Event_Approx_End_Date','State_Orig_Emergency_Proclam_Date',
#            'Fed_Disaster_Declar_Date','Rpr_Restor_NTP_Date','Rpr_Restor_Completion_Date']
for coln in routesdf.columns:
    routesdf[coln] = routesdf[coln].replace(r'\?', value='', regex=False)
for coln in coldates:
    routesdf[coln] = pd.to_datetime(routesdf[coln],format="%Y-%m-%d %H:%M:%S", errors='coerce')
fldfloat = ['BMP','EMP']
for coln in fldfloat:
    routesdf[coln] = pd.to_numeric(routesdf[coln],errors='coerce',downcast='float')
fldstring = [rteid]
for coln in routesdf.columns:
    if coln!=rteid:
        routesdf[coln] = routesdf[coln].replace('?', '', regex=False)
for coln in routesdf.columns:
    routesdf[coln] = routesdf[coln].replace('---', '', regex=False)
for coln in coldates:
    routesdf[coln] = pd.to_datetime(routesdf[coln],format="%Y-%m-%d %H:%M:%S", errors='coerce')
fldfloat = ['BMP','EMP']
for coln in fldfloat:
    routesdf[coln] = pd.to_numeric(routesdf[coln],errors='coerce',downcast='float')
fldstring = [rteid,'Direction','Material','Route']
for coln in fldstring:
    try:
        routesdf[coln] = routesdf.astype({ coln : 'str' }).dtypes # routesdf[coln] = pd.Series(routesdf[coln],dtype="string")
    except Exception as e:
        print(' Error : {} ;  string column {}  failed '.format(str(e),coln ))
        logger.error(' Error : {} ;  string column {}  failed '.format(str(e),coln ))
#routesdf = routesdf.astype({col:str for col in fldstring},errors='ignore')

for coln in fldstring:
    routesdf[coln] = routesdf[coln].replace('','nan') #, regex=True)
    
for coln in routesdf.columns:
    routesdf[coln] = routesdf[coln].replace('nan', '') #, regex=True)


# In[ ]:


print(routesdf[rteid].value_counts(rteid))
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
SPavecsvnm = r'HiDOT Pavement Project Limits.csv'
SPavesdfile = os.path.join(inpath,SPavecsvnm)
routesdf.to_csv(SPavesdfile)
print("{}".format((routesdf.dtypes)))


# In[ ]:


#evtrename = ["'{}' : '{}'".format(x, x[(len(x)-9):len(x)]) for x in routesdf.columns ]
#print("{}"".format(evtrename))

SPaverenamecols = {'RightLanePoorMilePct' :'Right Lane  Poor %','RightLanePoorMile' :'Right LanePoor Mile',
                  'RightLaneAPoorPct' :'Right Lane Almost Poor %','RightLaneAPoorMile' :'Right Lane Almost Poor Mile','AllLanePoorMile' :'All Lane Poor  Mile','AllLaneAPoorMile' :'All lane Almost Poor',
                  'SHAPE' : 'SHAPE'}
routeydf = deepcopy(routesdf)  #routesdf.rename (columns=SPaverenamecols,inplace=False)

print("Routesdf : {} ; DTypes : {}".format(routesdf['Route'].value_counts(),routesdf.dtypes))
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
print("Routexdf : {} ; DTypes : {}".format(routeydf['Route'].value_counts(),routeydf.dtypes))
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')


# In[ ]:


#print("{}".format(routesdf[qrycol].head(1)))
bmpcol = 'BMP'
empcol = 'EMP'
rteid = 'Route'
qrycol = rteid
rtelyrid = 'HiDOTRoutes'
offs = 0
qrykey = ''
qrystr = "{} != '{}'".format(qrycol,qrykey)
#routeydf = deepcopy(routesdf)
print ("number of Pavement Routes with {} = {} and routes{} ".format(qrystr,len(routeydf),routeydf[rteid].to_list()))
logger.info ("number of Routes entered with {} = {} and routes{} ".format(qrystr,len(routeydf),routeydf[rteid].to_list()))
routeydf['SHAPE']= routeydf.apply(lambda x : multirtes(rtelyr,str(x[rteid]),x[bmpcol],x[empcol],offs,rtelyrid),axis=1)
print ("SDF coumns {} and total count {}".format(routeydf.columns,len(routeydf.columns),routeydf['SHAPE'].head(1)))

print(routeydf[rteid].value_counts(rteid))
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
SPavecsvnm = r'HiDOT Pavement Project Limitsy.csv'
SPavesdfile = os.path.join(inpath,SPavecsvnm)
routeydf.to_csv(SPavesdfile)
print("{}".format((routeydf.dtypes)))


# In[ ]:


#print("{}".format(routesdf[qrycol].head(1)))
bmpcol = 'BMP'
empcol = 'EMP'
rteid = 'Route'
qrycol = rteid
rtelyrid = 'HiDOTRoutes'
offs = 0
qrykey = ''
qrystr = "{} != '{}'".format(qrycol,qrykey)
#routeydf = deepcopy(routesdf)
print ("number of Pavement Routes with {} = {} and routes{} ".format(qrystr,len(routeydf),routeydf[rteid].to_list()))
logger.info ("number of Routes entered with {} = {} and routes{} ".format(qrystr,len(routeydf),routeydf[rteid].to_list()))
routeydf['SHAPE']= routeydf.apply(lambda x : multirtes(rtelyr,str(x[rteid]),x[bmpcol],x[empcol],offs,rtelyrid),axis=1)
print ("SDF coumns {} and total count {}".format(routeydf.columns,len(routeydf.columns),routeydf['SHAPE'].head(1)))

print(routeydf[rteid].value_counts(rteid))
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
SPavecsvnm = r'HiDOT Pavement Project Limitsy.csv'
SPavesdfile = os.path.join(inpath,SPavecsvnm)
routeydf.to_csv(SPavesdfile)
print("{}".format((routeydf.dtypes)))


# In[ ]:


try:
    #curDate = strftime("%Y%m%d%H%M%S") 
    userName= "dot_mmekuria"
    if HISPavesrc != None:
        print (" Feature URL: {} ; Title : {} ; Id : {} ".format(HISPavesrc.url,HISPavesrc.title,HISPavesrc.id))
        logger.info (" Feature URL: {} ; Title : {} ; Id : {} ".format(HISPavesrc.url,HISPavesrc.title,HISPavesrc.id))
        # ID or Title of the feature service to update
        #print (" Content search result : {} ; ".format(fsprjstsrc))
        SPavelyrs = HISPavesrc.layers
        lyrnamelist = [ x.properties.name for i1,x in enumerate(SPavelyrs,1)]
        # header layer
        fs = len(SPavelyrs) #len(lyrtefs)
        if (fs>0):
            SPavelyr = lyrsearch(SPavelyrs, HISPavenm)
            print (" Found {} Layer {} with  id : {} ; Layer {}   ".format(HISPavenm,HISPavesrc.title,HISPavesrc.id,SPavelyr))
            logger.info (" Found {} Layer {} with  id : {} ; Layer {}   ".format(HISPavenm,HISPavesrc.title,HISPavesrc.id,SPavelyr))
        else:
            print (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(HISPavenm,HISPavesrc.title,HISPavesrc.id,lyrnamelist))
            logger.info (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(HISPavenm,HISPavesrc.title,HISPavesrc.id,lyrnamelist))
    else:
        print (" No  Layer {} with  Title  {} Found ".format(HISPavenm,HISPavesrc))
        logger.info (" No  Layer {} with  Title {} found  ".format(HISPavenm,HISPavesrc))
except Exception as e:
    print(' Error : {} ;   layer {} Project status script '.format(str(e),HISPavenm))
    logger.error(' Error : {} ;  layer {} Project status script '.format(str(e),HISPavenm ))


# In[ ]:


fldrte='Route'
offset=0
# Process geometry
# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print (" dataframe type  : {}  ".format(type(routexdf)))
#idx= pd.Index(projsw2ysdf) #(ignore_index=True)  for concat
# delete existing data first
#SPaverenamecols = {'Route' : 'Route'}
SPavesdf = deepcopy(routeydf)
#SPavesdf.rename (columns=SPaverenamecols,inplace=True)
SPavegeoac = gac(SPavesdf)
SPavewgs84 =  SPavegeoac.set_geometry('SHAPE',sr=sprefwgs84)
#SPavewgs84 =  SPavegeoac.project(sprefwgs84)

#SPavesw2ysdfx = gac.from_df(routesdf,  sr=sprefwgs84, geometry_column='SHAPE')
#SPavegeoacx = gac(SPavesw2ysdfx)
SPavefeats = SPavegeoac.to_featureset()
print (" features length : {} ; feature {} ".format(len(SPavefeats),SPavefeats))


# In[ ]:


SPavelyrs = HISPavesrc.layers
SPavelyr = lyrsearch(SPavelyrs, HISPavenm)
fldrte='Route'
offset=0
print("type : {} ; recordset : {} ".format(SPavelyrs,SPavelyr))
print("Query Features : {} ".format(SPavelyr.query()))
# Process geometry
# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print (" dataframe type  : {}  ".format(type(routexdf)))
#idx= pd.Index(projsw2ysdf) #(ignore_index=True)  for concat
# delete existing data first
delayerfeatures(SPavelyr)
SPaverenamecols = {'Route' : 'Route'}
SPavesdf = deepcopy(routeydf)
SPavesdf.rename (columns=SPaverenamecols,inplace=True)
SPavegeoac = gac(SPavesdf)
SPavewgs84 =  SPavegeoac.set_geometry('SHAPE',sr=sprefwgs84)
#SPavewgs84 =  SPavegeoac.project(sprefwgs84)

#SPavesw2ysdfx = gac.from_df(routesdf,  sr=sprefwgs84, geometry_column='SHAPE')
#SPavegeoacx = gac(SPavesw2ysdfx)
SPavefeats = SPavegeoac.to_featureset()
print (" features length : {} ; feature {} ".format(len(SPavefeats),SPavefeats))
# add to existing  layer 
resadd  = assyncadds(SPavelyr,SPavefeats)
print (" sdf features  : {} ; result {} ".format(len(SPavefeats),resadd))


# In[ ]:


print (" features length : {} ; feature {} ".format(len(SPavefeats),SPavefeats))


# In[ ]:


SPavelyrs = HISPavesrc.layers
SPavelyr = lyrsearch(SPavelyrs, HISPavenm)
fldrte='Route'
offset=0
print("type : {} ; recordset : {} ".format(SPavelyrs,SPavelyr))
print("Query Features : {} ".format(SPavelyr.query()))
# Process geometry
# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print (" dataframe type  : {}  ".format(type(routexdf)))
#idx= pd.Index(projsw2ysdf) #(ignore_index=True)  for concat

SPavesdf = deepcopy(routeydf)
SPavegeoac = gac(routeydf)
SPavewgs84 =  SPavegeoac.set_geometry('SHAPE',sr=sprefwgs84)
#SPavewgs84 =  SPavegeoac.project(sprefwgs84)

#SPavesw2ysdfx = gac.from_df(routesdf,  sr=sprefwgs84, geometry_column='SHAPE')
#SPavegeoacx = gac(SPavesw2ysdfx)
SPavefeats = SPavegeoac.to_featureset()
# add to existing  layer 
resadd  = assyncaddspt(SPavelyr,SPavefeats)
print (" sdf features  : {} ; result {} ".format(len(SPavefeats),resadd))

def rtefeat(x,SPavelyr,rtelyr,offset,fldrte='Route'):
    print ("{}".format(frow))
    idx = x.index
    rteid = x.Route_Num
    bmpvalx = x.BMP
    empvalx = x.EMP
    gx = rtesectmp(rtelyr,rteid,bmpvalx,empvalx,offset,fldrte) # rtempt(rtelyr,rteFCSelNm,rteid,bmpvalx,offset,fldrte)
    resupdate = assyncadds(SPaveintlyr,newfset) 
    
    print("type : {} ; recordset : {} \n - type {} - geom : {} \n\n ".format(type(frow),frow.SHAPE,type(gx),gx))
    sdfrow = geomilepostdf.query("globalid=='{}'".format(frow.globalid))
    print("type : {} ; updated geometry : {} \n - shape col : {} \n\n ".format(type(sdfrow),sdfrow.index[0],sdfrow['SHAPE']))
    sdfrow.loc[sdfrow.index[0],'SHAPE'] = [gx]  # sdfrow.apply(lambda x : gx , axis=1 ) # gx # sdfrow.apply(lambda x : gx,axis=1 ) .loc[0,'SHAPE']
    print("type : {} ; updated geometry : {} \n - shape col : {} \n\n ".format(type(sdfrow),sdfrow,sdfrow['SHAPE']))
    newfset = gac(sdfrow).to_featureset()
    print ("updated : {} \n\n".format(newfset.to_dict()))
    resupdate = assyncedits(SPaveintlyr,newfset) 
    print("result : {}".format(resupdate))    

def addsdfeats(x,SPavelyr,rtelyr,offset,fldrte='Route'):
    print ("{}".format(frow))
    idx = x.index
    rteid = x.Route_Num
    bmpvalx = x.BMP
    empvalx = x.EMP
    gx = rtesectmp(rtelyr,rteid,bmpvalx,empvalx,offset,fldrte) # rtempt(rtelyr,rteFCSelNm,rteid,bmpvalx,offset,fldrte)
    resupdate = assyncadds(SPaveintlyr,newfset) 
    
    print("type : {} ; recordset : {} \n - type {} - geom : {} \n\n ".format(type(frow),frow.SHAPE,type(gx),gx))
    sdfrow = geomilepostdf.query("globalid=='{}'".format(frow.globalid))
    print("type : {} ; updated geometry : {} \n - shape col : {} \n\n ".format(type(sdfrow),sdfrow.index[0],sdfrow['SHAPE']))
    sdfrow.loc[sdfrow.index[0],'SHAPE'] = [gx]  # sdfrow.apply(lambda x : gx , axis=1 ) # gx # sdfrow.apply(lambda x : gx,axis=1 ) .loc[0,'SHAPE']
    print("type : {} ; updated geometry : {} \n - shape col : {} \n\n ".format(type(sdfrow),sdfrow,sdfrow['SHAPE']))
    newfset = gac(sdfrow).to_featureset()
    print ("updated : {} \n\n".format(newfset.to_dict()))
    resupdate = assyncedits(SPaveintlyr,newfset) 
    print("result : {}".format(resupdate))    
    
    
bmpcol = 'BMP'  # 'MP_Start'
empcol = 'EMP' # 'MP_End'
offset = 0
# delete existing data first
delayerfeatures(SPavelyr)
geomilepostdf = deepcopy(routeydf) 
geomilepostdf['SHAPE']=geomilepostdf.apply(lambda x : rtefeat(x,SPavelyr,rtelyr,offset,fldrte))


# In[ ]:


# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print (" dataframe type  : {}  ".format(type(routexdf)))
#idx= pd.Index(projsw2ysdf) #(ignore_index=True)  for concat

SPavesdf = deepcopy(routeydf)
SPavegeoac = gac(routeydf)
SPavewgs84 =  SPavegeoac.set_geometry('SHAPE',sr=sprefwgs84)
#SPavewgs84 =  SPavegeoac.project(sprefwgs84)

#SPavesw2ysdfx = gac.from_df(routesdf,  sr=sprefwgs84, geometry_column='SHAPE')
#SPavegeoacx = gac(SPavesw2ysdfx)
SPavefeats = SPavegeoac.to_featureset()
# add to existing  layer 
print (" sdf features  : {}  ".format(len(SPavefeats)))
# shape file creation
SPaveshpnm = r'HiDOT Pavement Project Limits.shp'
SPaveshpfile = os.path.join(inpath,SPaveshpnm)
SPavelyr = SPavefeats.save(inpath,SPaveshpnm, encoding="utf8")
# shape file creation
SPavefgbnm = r'HiDOT Pavement Project Limits.fgb'
SPavefgbfile = os.path.join(inpath,SPaveshpnm)
SPavefgb = SPavefeats.save(inpath,SPavefgbnm, encoding="utf8")

print(" Feature Class layer : {} created ".format(SPavefgb,SPavefgbfile))

SPavefeatsdf = SPavefeats.sdf
#progfl = qgis.content.import_data(SPavefeatsdf,title='Projects Closed within 2 Years',tags='projects,pss,closed',target_sr=4326)
#SPavefeatjson = SPavefeats.to_json
SPavefeatgeojson = SPavefeats.to_geojson
SPaveintgeojsoname = "SPavelan.geojson"
SPaveintgeojsonpath = os.path.join(rptpath, SPaveintgeojsoname)
#SPaveintfcname = "SPaveintData.fgb"
#SPaveintfcpath = os.path.join(rptpath, SPaveintfcname)
gjfile = open(SPaveintgeojsonpath, 'w')
gjfile.write(SPavefeatgeojson)
gjfile.close()
print(" Geojson data written to : {}  ".format(SPaveintgeojsonpath))


# In[ ]:


print (" sdf features  : {}  ".format(len(SPavefeats)))
SPaveintnm = 'HiDOT Pavement Project Limits'

valires = SPavegeoac.validate(strict=True)
print(" Feature validation : {} created ".format(valires))
# feature layer creation
SPavelyr = SPavegeoac.to_featurelayer(title=SPaveintnm, gis=qgis, tags='projects, STIP, HDOT, SPave, routes', folder=None)
print(" Feature Class layer : {} created ".format(SPavelyr))
sdfeats = SPavefeats.sdf
#sdfeats['SHAPE']

# shape file creation
#SPaveshpnm = r'Repair_Recon_Sites_20201217sdfv2.shp'
#SPaveshpfile = os.path.join(inpath,SPaveshpnm)
#SPavelyr = SPavegeoac.to_featureclass(SPaveshpfile, overwrite=True, has_z=None, has_m=False)
print(" Feature Class layer : {} created ".format(SPavelyr))


# In[ ]:



SPavelayer= 'HiDOT Pavement Project Limits'
SPavefeatfcol = SPavegeoac.to_feature_collection(name=SPavelayer, drawing_info=None, extent=None, global_id_field=None)
SPaveinfcdict = dict(SPavefeatfcol.properties)
SPaveinjson = json.dumps({"featureCollection": {"layers": [SPaveinfcdict]}})
#print (" JSON feature collection  : {}  ".format(SPaveinjson)) 
SPaveinitem_properties = {'title': SPavelayer ,
                        'description':'HDOT Pavement Repair and Maintenance projects ' + \
                         'Using HWY-L Excel data ',
                        'tags': 'projects, pss, HDOT, repair, status, maintenance ',
                        'text':SPaveinjson,
                        'type':'Feature Collection'}
SPaveinitem = qgis.content.add(SPaveinitem_properties)


#SPaveinitem
#qgis.content.add(type='featureLayer')
#SPavefeatfcol = arcgis.features.FeatureCollection(SPavefeats,name='Projects Closed within 2 Years')

#SPavelyr = SPavegeoac.to_featurelayer(title='Emergency Repair and Maintenance projects', gis=qgis, tags='projects, pss, HDOT, emergency, repair', folder=None)
#print(" layer : {}  ".format(SPavelyr))

#dfcsv = pd.read_csv(csvfile)
#print (" csv sdf features head : {}  ".format(dfcsv.head(1)))


#tmp_file = tempfile.mkstemp(suffix='.geojson')
#with open(SPaveintgeojsonpath, 'w') as outfile:
#    geojson.dump(SPaveinjson, outfile)
print (" Geojson file  : {}  output ".format(SPaveintgeojsonpath))
#fcfile = SPavegeoac.to_featureclass(SPaveintfcpath, overwrite=True, has_z=None, has_m=True)


# In[ ]:


# if layer data does not exist import fresh data into ArcGIS from excel 
try:
    #curDate = strftime("%Y%m%d%H%M%S") 
    userName= "dot_mmekuria"
    # ID or Title of the feature service to update
    if SPaveintsrc != None:
    #print (" Content search result : {} ; ".format(fsprjstsrc))
        SPavelyrs = SPaveintsrc.layers
        lyrnamelist = [ x.properties.name for i1,x in enumerate(SPavelyrs,1)]
        # header layer
        fs = len(SPavelyrs) #len(lyrtefs)
        if (fs>0):
            SPavelyr = lyrsearch(SPavelyrs, SPaveintnm)
        else:
            print (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(SPaveintnm,SPaveintsrc.title,SPaveintsrc.id,lyrnamelist))
            logger.info (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(SPaveintnm,SPaveintsrc.title,SPaveintsrc.id,lyrnamelist))
            
    else:
        SPavelyr = SPavegeoac.to_featurelayer(title="HiDOT Emergency Maintenance and Repair Projects", gis=qgis, tags='projects, pss, HDOT, maintenance, repair', folder=None)
        print(" layer : {} created ".format(SPavelyr))
        SPavegeoacx = SPavegeoac.to_feature_collection(name=SPaveintnm, drawing_info=None, extent=None, global_id_field=None)
        
    print (" Feature URL: {} ; Title : {} ; Id : {} \n Layers - {}  ".format(SPaveintsrc.url,SPaveintsrc.title,SPaveintsrc.id,lyrnamelist))
    logger.info (" Feature URL: {} ; Title : {} ; Id : {} \n Layers - {} ".format(SPaveintsrc.url,SPaveintsrc.title,SPaveintsrc.id,lyrnamelist))
except Exception as e:
    print(' Error : {} ;  fetching layer {}  script '.format(str(e),SPaveintnm ))
    logger.error(' Error : {} ;  fetching layer {}  script '.format(str(e),SPaveintnm ))


# In[ ]:


# Process geometry
bmpcol = 'MP_Start'
empcol = 'MP_End'
offset = 0
geomilepostdf = deepcopy(routesdf) 
for ix,frow in enumerate(geomilepostdf.itertuples(),0):
    print ("{}".format(frow))
    idx = frow.index
    rteid = frow.Route_Num
    bmpvalx = frow.MP_Start
    empvalx = frow.MP_End
    fldrte= 'Route'
    gx = rtesectmp(rtelyr,rteid,bmpvalx,empvalx,offset,fldrte) # rtempt(rtelyr,rteFCSelNm,rteid,bmpvalx,offset,fldrte)
    
    print("type : {} ; recordset : {} \n - type {} - geom : {} \n\n ".format(type(frow),frow.SHAPE,type(gx),gx))
    sdfrow = geomilepostdf.query("globalid=='{}'".format(frow.globalid))
    print("type : {} ; updated geometry : {} \n - shape col : {} \n\n ".format(type(sdfrow),sdfrow.index[0],sdfrow['SHAPE']))
    sdfrow.loc[sdfrow.index[0],'SHAPE'] = [gx]  # sdfrow.apply(lambda x : gx , axis=1 ) # gx # sdfrow.apply(lambda x : gx,axis=1 ) .loc[0,'SHAPE']
    print("type : {} ; updated geometry : {} \n - shape col : {} \n\n ".format(type(sdfrow),sdfrow,sdfrow['SHAPE']))
    newfset = gac(sdfrow).to_featureset()
    print ("updated : {} \n\n".format(newfset.to_dict()))
    resupdate = assyncedits(SPaveintlyr,newfset) 
    print("result : {}".format(resupdate))


# In[ ]:


# update the coordinates using the newly generated coordinates 

#equsgsmap = qgis.content.search("31cfc5b138e24dee866c457948773ac4")

equsgsmap = qgis.content.get("31cfc5b138e24dee866c457948773ac4")
print("{}".format(equsgsmap) )

equsgsmap.get_data(try_json=True)


# In[ ]:


# Export ArcGIS Dataframe to .CSV

logpath = r"D:\MyFiles\HWYAP\SPaveintes\logs"
rptpath = r"D:\MyFiles\HWYAP\SPaveintes\reports"
# SPaveint layers
SPaveintnm = 'HiDOT Pavement Project Limits'
SPaveintentrysrc = SPaveintsrc.layers
SPaveintentrylyr = lyrsearch(SPaveintentrysrc, SPaveintnm)
SPaveintfeatset = SPaveintentrylyr.query(where='1=1', out_fields='*')
SPaveintfeats = SPaveintfeatset.features
#SPaveintdf = SPaveintfeats.sdf
SPaveintrpath =r"D:\MyFiles\HWYAP\SPaveintes\reports" # r"C:\Work Database Data\SPaveint\Data"
SPaveintcsvname = "SPaveintData.csv"
SPaveintcsvpath = os.path.join(SPaveintrpath, SPaveintcsvname)
SPaveintcsv = SPaveintdf.to_csv(SPaveintcsvpath)
SPaveintjsoname = "SPaveintData.geojson"
SPaveintjsonpath = os.path.join(SPaveintrpath, SPaveintjsoname)
SPaveintdf = SPaveintfeatset.df #SPaveintentrylyr.query(where='1=1', out_fields='*',as_df=True)
#SPaveintgeojson =SPaveintfeats.to_geojson() #SPaveintjsonpath) # 
#arcgis.features.FeatureLayerCollection.upload(SPaveintgeojson,description="Fatal SPaveint Dataset")
#SPaveintgeojson = SPaveintfeats.save(rptpath,SPaveintjsonname)
SPaveintpname = "SPaveintData.shp"
SPaveintpath = os.path.join(SPaveintrpath, SPaveintpname)
#SPaveintp = SPaveintdf.save(SPaveintpath)
SPaveintpfile = SPaveintfeatset.save(SPaveintrpath, SPaveintpname, encoding='utf8') # eatlnclrte.save('in_memory','rtesel')
print ("GeoJson : {} ; Feats : {}".format(SPaveintpfile,len(SPaveintfeats)))


# In[ ]:


#Using ArcGIS GeoJSON data replace
from socrata.authorization import Authorization
from socrata import Socrata
import os
import sys

auth = Authorization(
  'highways.hidot.hawaii.gov',
  os.environ['MY_SOCRATA_USERNAME'],
  os.environ['MY_SOCRATA_PASSWORD']
)

socrata = Socrata(auth)
view = socrata.views.lookup('xr73-pg3t')

with open('SPaveintData.geojson', 'rb') as my_file:
  (revision, job) = socrata.using_config('SPaveintData_12-03-2020_cc15', view).geojson(my_file)
  # These next 2 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  job = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
  sys.exit(0 if job.attributes['status'] == 'successful' else 1)


# In[ ]:


#Using ArcGIS GeoJSON data upsert
from socrata.authorization import Authorization
from socrata import Socrata
import os
import sys

auth = Authorization(
  'highways.hidot.hawaii.gov',
  os.environ['MY_SOCRATA_USERNAME'],
  os.environ['MY_SOCRATA_PASSWORD']
)

socrata = Socrata(auth)
view = socrata.views.lookup('xr73-pg3t')

with open('SPaveintData.geojson', 'rb') as my_file:
  (revision, job) = socrata.using_config('SPaveintData_12-03-2020_ffa2', view).geojson(my_file)
  # These next 2 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  job = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
  sys.exit(0 if job.attributes['status'] == 'successful' else 1)


# In[ ]:


# Authenticate and Update Socrata Using .CSV


from socrata.authorization import Authorization
from socrata import Socrata
import os
import sys
MyAPIKey = "****" #Add API Key Here
MyAPIPw = "****" #Add API Password Here

auth = Authorization(
  'highways.hidot.hawaii.gov',
  MyAPIKey,
  MyAPIPw
)

"""
Chris's dataset
socrata = Socrata(auth)
view = socrata.views.lookup('5pi7-pfhe')

with open(SPaveinthcsvpath, 'rb') as csvfeats:
  (revision, job) = socrata.using_config('FatalSPaveinthData_11-02-2020_0e39', view).csv(csvfeats)
  # These next 2 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  job = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
  sys.exit(0 if job.attributes['status'] == 'successful' else 1)

"""

socrata = Socrata(auth)
view = socrata.views.lookup('xr73-pg3t')

with open(SPaveinthjsonpath, 'rb') as SPaveinthgeojson:
  (revision, job) = socrata.using_config('Fatal SPaveinth SocData_11-24-2020_3408', view).geojson(SPaveinthgeojson)
  # These next 2 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  job = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
  sys.exit(0 if job.attributes['status'] == 'successful' else 1)


# In[ ]:


# append using geojson from ArcGIS 
from socrata.authorization import Authorization
from socrata import Socrata
import os
import sys

auth = Authorization(
  'highways.hidot.hawaii.gov',
  os.environ['MY_SOCRATA_USERNAME'],
  os.environ['MY_SOCRATA_PASSWORD']
)

socrata = Socrata(auth)
view = socrata.views.lookup('xr73-pg3t')

with open('HIFatalSPaveinthes2018.geojson', 'rb') as my_file:
  (revision, job) = socrata.using_config('HIFatalSPaveinthes2018_11-25-2020_1a22', view).geojson(my_file)
  # These next 2 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  job = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
  sys.exit(0 if job.attributes['status'] == 'successful' else 1)

