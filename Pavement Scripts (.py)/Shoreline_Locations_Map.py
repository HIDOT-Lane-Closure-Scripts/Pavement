#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime, tzlocal
from datetime import date , timedelta, datetime
from time import sleep
from socrata.authorization import Authorization
from socrata import Socrata
import os
import sys
MyAPIKey = "***" #Add API Key Here
MyAPIPw = "***" #Add API Password Here

socauth = Authorization(
  'highways.hidot.hawaii.gov',
  MyAPIKey,
  MyAPIPw
)


# In[ ]:


socradata = Socrata(socauth)
socdataid = 'rh4f-u3x6'  # https://highways.hidot.hawaii.gov/dataset/Shoreline-Ranking/rh4f-u3x6
shoreline = socradata.views.lookup(socdataid)
cbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p")
print ("date {}   ; dataset : {} ; view : {} ;".format(cbeg,socdataid,shoreline))


# In[ ]:


# AGOL Account Login & Setup

import arcgis
from arcgis.gis import GIS
import smtplib, ssl
import logging, re, os
#logpath = r"\\HWYPB\NETSHARE\HWYA\HWY-AP\emaint\logs"
#rptpath = r"\\HWYPB\NETSHARE\HWYA\HWY-AP\emaint\reports"
logpath = r'd:\myfiles\HWYAP\branches\HWYL\logs'
rptpath = r'd:\myfiles\HWYAP\branches\HWYL\reports'
#inpath = r'D:\MyFiles\HWYAP\Admin\branches\HWY-C\emerepair'
inpath = r'd:\myfiles\HWYAP\branches\HWYL'
#infilename = ' Poor Shoreline Projects FY21-24 Updated.xlsx'
#logpath = r'I:\HI\AP\emerepair\logs'
#rptpath = r'I:\HI\AP\emerepair\reports'
#inpath = r'I:\HI\AP\emerepair'

logger = logging.getLogger('Shorelocentries')
logfilenm = r'Shorelocationentries.log'
logfile = os.path.join(logpath,logfilenm) # r"confemaintentries.log"
Shorelochdlr = logging.FileHandler(logfile) # 'emaintentries.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
Shorelochdlr.setFormatter(formatter)
logger.addHandler(Shorelochdlr)
logger.setLevel(logging.INFO)

try:
    # ArcGIS user credentials to authenticate against the portal
    credentials = { 'userName' : '***', 'passWord' : '*******'} # credentials = { 'userName' : 'dot_***', 'passWord' : '***'} #Enter ArcGIS Credentials here
    userName = credentials['userName'] # arcpy.GetParameter(2) # 
    passWord =  credentials['passWord'] #  # arcpy.GetParameter(3) # 
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


# define functions to be used in the processing of the project data into ArcGIS and Socrata Geometries
from arcgis import geometry

def assyncadds(lyr,fset):
    sucs1=0
    errcnt = 0
    pres = None
    while(round(sucs1)==0):
        pres = lyr.edit_features(adds=fset) #.append(prjfset) #.append(prjfset,field_mappings=fldmaprj)
        if pres['addResults'][0]['success']==True:
            sucs1=1
        else:
            errcnt+=1
            terr = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p")
            logger.error("Attempt {} at {} ; Result : {} ; Layer {} ; features {} ; ".format(errcnt,terr, pres,lyr.properties.name,fset))
            if errcnt<=5:
                sleep(5)
            else:    
                sucs1 = -1
    return pres

def assyncaddsingle(lyr,fset):
    sucs1=0
    errcnt = 0
    presult = []
    pres = None
    for feat in fset:
        fcsingle = [feat] 
        while(round(sucs1)==0):
            pres = lyr.edit_features(adds=fcsingle) #.append(prjfset) #.append(prjfset,field_mappings=fldmaprj)
            if pres['addResults'][0]['success']==True:
                sucs1=1
                presult.append(pres)
            else:
                errcnt+=1
                terr = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p")
                logger.error("Attempt {} at {} ; Result : {} ; Layer {} ; attributes {} ; geometry {} ".format(errcnt,terr, pres,lyr.properties.name,fset.features[0].attributes,fset.features[0].geometry))
                if errcnt<=5:
                    sleep(5)
                else:    
                    sucs1 = -1
                    presult.append(pres)
    return presult


    
def stripjson (fldval):
    #print("{}".format(fldval))
    newval = fldval['ok']
    return newval

def wkt2arcgeom (fldval,srf):
    #newval = str(fldval).replace("coordinates","paths").replace("type","spatialreference").replace("MultiLineString","{'wkid' : 4326}")
    coords = fldval["coordinates"] 
    newgeom = { "paths" : coords, "spatialReference" :  srf  } 
    pline = geometry.Polyline(newgeom)
    #print("Geometry Type {} ; valid ? {}".format(pline.type,pline.is_valid()))
    return pline

# group by Shelly's request We would have: •	Safety ; •	System Mitigation;•	Capacity; •	Congestion; •	Bike/Ped; •	Other
#So Compliance would be included in the Other category and Modernization likely in the Capacity category.
def shelgroup(fldval):
    catgy = fldval
    if (fldval!=None):
        if (fldval.lower() in ['modern']):
            catgy = 'capacity'
        if (fldval.lower() in ['other']):
            catgy = 'other'
        elif (fldval.lower() in ['compliance']):
            catgy = 'other'
        else:
            catgy=fldval.lower()
    else:
        if (len(fldval)==0):
            catgy = 'syst presrv'
    #print("Geometry Type {} ; valid ? {}".format(pline.type,pline.is_valid()))
    return catgy

def webexsearch(mgis, title, owner_value, item_type_value, max_items_value=1000,inoutside=False):
    item_match = None
    search_result = mgis.content.search(query= title + ' AND owner:' + owner_value, 
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
    elif closide == 'Conflict' or closide == 'All':
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
    intsplitxt = intshortlbl.split(sep='&', maxsplit=1)
    txtret=intsplitxt[1]  # default to the second intersection unless the second one has the route
    rtenmsplit = rtenametxt.split(sep=" ")
    if len(rtenmsplit)>2:
        rtenmsplit = "{} {}".format(rtenmsplit[0].capitalize(),rtenmsplit[1].capitalize())
    else:
        rtenmsplit = "{}".format(rtenmsplit[0]).capitalize()
               
    for txt in intsplitxt:
        txtsep = txt.split(sep=" ")
        if len(txtsep)<=2 and txtsep[1]=='':
            txt= "Exit " + txt.upper()
        if rtenmsplit not in txt and rtext not in txt and fromtxt!=txt:
            txtret = txt
    return txtret          


def replace(client,fourby, df):
    data = df.to_dict(orient='records', into=NativeDict)
    # pprint(data)

    # set up client for api calls
    #client = Socrata(url, app_token, username=user, password=password)
    # upsert new row using client
    try:
        res = client.replace(fourby, data)
    except Exception as e:
        print('whoops')
        res = e

    logResult(fourby, res)
    print(res)
    client.close()

    return res


def logResult(fourby, res):
    logStr = fourby + ": " + str(res) + "\n"
    logFile = open(logfilenm, 'a')
    logFile.write(logStr)
    logFile.close()
    
class NativeDict(dict):
    """
        Helper class to ensure that only native types are in the dicts produced by
        :func:`to_dict() <pandas.DataFrame.to_dict>`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(((k, self.convert_if_needed(v)) for row in args for k, v in row), **kwargs)

    @staticmethod
    def convert_if_needed(value):
        """
            Converts `value` to native python type.
        """
        if pd.isnull(value):
            return None
        if isinstance(value, pd.Timestamp):
            return value.isoformat()
        if hasattr(value, 'dtype'):
            mapper = {'i': int, 'u': int, 'f': float}
            _type = mapper.get(value.dtype.kind, lambda x: x)
            return _type(value)
        if value == 'NaT':
            return None
        return value


# function to return whether the closure date range is a weekend or weekday
def wkend(b,e):
    if b==0 and e <=1: 
        return 1 
    elif b>=1 and e<=5: 
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

def fridaywk(bdate,n1):
    wkdte = datetime.strftime(bdate,"%w") # + datetime.strftime(bdate,"%z")
    date4pm = datetime.strptime(datetime.strftime(bdate,"%Y-%m-%d"),"%Y-%m-%d") + timedelta(hours=16)
    fr4pm= date4pm + timedelta(days=(5-int(wkdte)+(n1-1)*7))
    return fr4pm


def lanestypeside(clside,cltype,nlanes,clfact):
    if clfact.upper()=="SHOULDER":
        lts = "Shoulder closed" 
    else: # not a shoulder (lane, ramp, etc)      
        if clside.upper()=="BOTH":
            lts = cltype + " closure " + clside.lower() + " lanes"
        elif clside.upper() in ["RIGHT","LEFT" ,"CENTER"]:
            if nlanes>1:
                lts = str(nlanes) + " " + clside.lower() + " lanes closed"
            else:
                lts = clside.capitalize() + " lane closed"
        elif clside.upper()=="DIRECTIONAL":
            lts = "Lanes closed in one direction"
        elif clside.upper()=="SHIFT":
            lts="Lanes shifted"
        elif clside.upper()=="FULL":
            lts = "Conflict lane closure" 
        else:
            lts = "{} {} {}(s) closure".format(nlanes, clside , clfact )     
    return lts        
    #[ClosureSide]="Right",IIf([NumLanes]>1,[NumLanes] & " right lanes closed","Right lane closed"),[ClosureSide]="Left",IIf([NumLanes]>1,[NumLanes] & " left lanes closed","Left lane closed"),[ClosureSide]="Center",IIf([NumLanes]>1,[NumLanes] & " center lanes closed","Center lane closed"),[ClosureSide]="Conflict","Conflict lane closure",[ClosureSide]="Directional","Lanes closed in one direction",[ClosureSide]="Shift","Lanes shifted")

#OnRoad: IIf([Route]="H-1" Or [Route]="H-2" Or [Route]="H-3",[Route],IIf([Route]="H-201",[RoadName],IIf(Left([Route],2)="H-",Left([Route],3) & " off ramp",[RoadName])))
def routeinfo(rteid,rtename):
    if rteid.upper() in ["H-1", "H-2", "H-3"]:
        rtext = rteid.upper() 
    elif rteid.upper() in ["H-201"]:
        rtext = rtename 
    elif rteid[1:2] =="H-":
        rtext = "Off Ramp" 
    else:
        rtext = rtename 
    if len(rtext)==0:
        rtext = rteid    
    return rtext        

#DirectionWords: IIf([direct] Is Null,""," in " & [direct] & " direction")
def dirinfo(dirn):
    if len(dirn)==0:
        dirtext = ""
    else:
        dirtext = dirn + " direction " 
    return dirtext

#BeginDateName,EndDateName:  The month and the day portion of the begin or end date. (ex. November 23)
def dtemon(dte):
    #dtext = datetime.strftime(dte-timedelta(hours=10),"%B") + " " +  str(int(datetime.strftime(dte-timedelta(hours=10),"%d")))
    dtext = datetime.strftime(dte-timedelta(hours=0),"%B") + " " +  str(int(datetime.strftime(dte-timedelta(hours=0),"%d")))
    return dtext

# BeginDay, EndDay: Weekday Name of the begin date (Monday, Tuesday, Wednesday, etc.)
def daytext(dte):
    dtext = datetime.strftime(dte-timedelta(hours=0),"%A") 
    return dtext

def dateonly(bdate,h1=0):
    datemid = datetime.strptime(datetime.strftime(bdate,"%Y-%m-%d"),"%Y-%m-%d") + timedelta(hours=h1)
    return datemid

#BeginTime, EndTime: The time the lane closure begins.  12 hour format with A.M. or P.M. at the end
def hrtext(dte):
    hrtext = datetime.strftime(dte-timedelta(hours=0),"%I:%M %p") 
    return hrtext

""" # FullSentence: [LanesTypeSide] & " on " & [OnRoad] & [DirectionWords] & IIf([BeginDateName]=[EndDateName]," on " 
& [BeginDay] & ", " & [BeginDateName]," from " & [BeginDay] & ", " & [BeginDateName] & " to " & [EndDay] & ", " 
& [EndDateName]) & ", " & [BeginTime] & " to " & [EndTime] & " " & [Special Remarks]
"""
def fulltext (lts,rtext,dirtext,begdymon,endymon,begdynm,endynm,begtm,endtm,begint,endint,rmarks,fldnm="OBJECTID",val1=0,urlink="",emailink=""):
    #fultext = lts + " on " + rtext + dirtext 
    if (begint==endint):
        begendint = "In the vicinity of {}".format(begint)
    else:
        begendint = "Between intersections of {} and {}".format(begint,endint)
    qu = "\""
    rtextlnk = "<a href={}{}?{}={}{}> {} </a>".format(qu,urlink,fldnm,val1,qu,rtext)        
    if begdynm == endynm:
        fultext = "{} on {}  {} on {}, {}, {} to {}, {},  {}".format(lts, rtextlnk, dirtext, begdynm, begdymon,begtm, endtm,begendint,rmarks)
    else:    
        fultext = "{} on {}  {} from {}, {}, to {}, {}, {} to {}, {}, Remarks : {}".format(lts, rtextlnk, dirtext, begdynm, begdymon,endynm, endymon,begtm, endtm,begendint,rmarks) 
    return fultext

def oidlink (qu,urlink,fldnm,val1,qv,rtext):
    oidlnk = "<a href={}{}?{}={}{}> {} </a>".format(qu,urlink,fldnm,val1,qv,rtext)        
    return oidlnk

def conflink (qu,urlink,fldnm,val1,qv,rtext):
    rtextid= "{} Object Id = {}".format(rtext,val1)
    oidlnk = "<a href={}{}?{}={}{}> {} </a> <b>Conflict Id = {}</b>".format(qu,urlink,fldnm,val1,qv,rtext,val1)        
    return oidlnk

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
def mergeometry(geompaths):
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

# generate single socrata line from an arcgis multiline shape geometry 
def socline2shp(socline,prjsr):
    slinetxt = ""
    if socline is not None:
        ltype = socline['type']
        mcoords = socline['coordinates']
        glen = len(mcoords) # rtepaths[0][len(rtepaths[0])-1] 
        if glen>0:
            shpgeom = []
            shpgeom.append(mcoords)
    else:
        shpgeom = ""
    shpgeom = Geometry({"paths" : shpgeom, "spatial_reference" : prjsr }) 
    print (" Geom before {} and After {} ".format(ltype,shpgeom.type ))
    return shpgeom

# convert degrees of lat long to miles
def deg2miles(darc1):
    r=6378 # radius in km
    ft2met = 3.280833333 
    mi1 = 5280 
    return darc1*r*1000/(2*math.pi*ft2met*mi1)

def routegeometrydef(lyr,keyfld,fldval,prjsr):  # query feature layer and return geometry
    arcpy.env.overwriteOutput = True
    geomrte = None
    defrte = '430'
    featcl = lyr.query(where = "{} in  ({}{}{}) ".format(keyfld," '",fldval,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
    if (len(featcl)>0):
        ftcl = featcl.features
        featgeo = ftcl[0].geometry
        geomrte = arcgis.geometry.Geometry(featgeo,sr=prjsr)
    else:
        geomrte = routegeometrydef(lyr,keyfld,defrte,prjsr)    
    return geomrte

# In[104]:
def remove_control_characters(s):
    rgx = re.compile('\r\n')
    #sx = re.compile(r'\%(.+?)\%',re.DOTALL).findall(s)
    sx = rgx.sub(" ",s)
    return sx #"".join(ch for ch in sx if unicodedata.category(ch)[0]!="C")

def geom2fsets(xsdf,shpcol1,srf):
    xsdfgac = gac(xsdf)
    xsdfgacgeo = xsdfgac.set_geometry(shpcol1, sr=srf)
    xsdf.spatial.set_geometry(col=shpcol1, sr=srf)
    xfset =  xsdf.spatial.to_featureset()
    return xfset



def conflictext (lts,rtext,dirtext,begdymon,endymon,begdynm,endynm,begtm="",endtm="",conflids="",fldnm="OBJECTID",val1=0,urlink="",emailink="",urlconflink='http://arcg.is/1qz8yT'):
    confltext = "" #lts + " on " + rtext + dirtext 
    qu = "\""
    conflhtml = ""
    conflids = list(dict.fromkeys(conflids))  # remove duplicate keys
    idp = 0
    for ix,id in enumerate(conflids,1):
        if idp != id:
            idp = id
            if ix==1:
                conflhtml = conflhtml + conflink (qu,urlconflink,fldnm,id,qu,rtext)
                idp = id
            else:     
                conflhtml = conflhtml + "<li>" + conflink (qu,urlconflink,fldnm,id,qu,rtext) + "\n" 
            
    endint=begint="" 
    if (begint==endint):
        begendint = "" #"In the vicinity of {}".format(begint)
    else:
        begendint = ""  #"Between intersections of {} and {}".format(begint,endint)
    rtextlnk = "<a href={}{}?{}={}{}> {} </a>".format(qu,urlink,fldnm,val1,qu,rtext)        
    if begdynm == endynm:
        confltext = "{} on {}  {} on {}, {}, {} to {}, {}, conflicts with {}".format(lts, rtextlnk, dirtext, begdynm, begdymon,begtm, endtm,begendint,conflhtml)
    else:    
        confltext = "{} on {}  {} from {}, {}, to {}, {}, {} to {}, {}, conflicts with : {}".format(lts, rtextlnk, dirtext, begdynm, begdymon,endynm, endymon,begtm, endtm,begendint,conflhtml) 
    return confltext


def recs2htmlbody(featsdf,htmltd="",urlinkx="",emlnk=''):
    # merge relationship records from the child table to the current header record
    qx="\""
    htmlby = "\n"  #htmltxtd.format(q1="\"",urlink=urlinkx,q2="\"",island=sdfrec.Island,route=sdfrec.Route,begindate=sdfrec.beginDate,endate=sdfrec.enDate,intersfrom=sdfrec.IntersFrom,intersto=sdfrec.IntersTo) + "\n"
    htmlwkday =  "\n" + "<tr><th> -- </th></tr>" + "\n"
    htmlwkend =  "\n" + "<tr><th> -- </th></tr>" + "\n"
    wkend =0
    wkday =0

    for ir,sdfrec in enumerate(featsdf.itertuples()):   # two points are given                                                                                                                                                                                                                                                                                                                                                                                       
    # add two sets of columns from the related data to the header data frame                                                                                                                                                                                                                                                                                                                                                                                             
        #htmlby = htmlby + htmltd.format(q1="\"",urldet=urlinkx,fldid="OBJECTID",fldval=sdfrec.OBJECTID,q2="\"",island=sdfrec.Island,route=sdfrec.Route,roadname=sdfrec.RoadName,intersfrom=sdfrec.IntersFrom,intersto=sdfrec.IntersTo,begindate=sdfrec.beginDate,endate=sdfrec.enDate) + "\n"
        if len(sdfrec.l1email)>0:
            emlnk = emlnk.format(q1=qx,email2=sdfrec.l1email,ln=sdfrec.CloseFact,rte=sdfrec.Route,isld=sdfrec.Island,q2=qx,q3=qx,q4=qx)
        elif len(sdfrec.l2email)>0:    
            emlnk = emlnk.format(q1=qx,email2=sdfrec.l2email,ln=sdfrec.CloseFact,rte=sdfrec.Route,isld=sdfrec.Island,q2=qx,q3=qx,q4=qx)
        else:
            emlnk=""    
        if sdfrec.wkEnd==1:
            if wkend==0:
                wkend=1
                htmlwkend = htmlwkend + "\n" + "<tr><th> Weekend </th></tr>" + "\n"
            htmlwkend = htmlwkend  + htmltd.format(fulltxt=sdfrec.FullText,eml=emlnk) + "\n"
        else:
            if wkday==0:
                wkday=1
                htmlwkday = htmlwkday + "\n" + "<tr><th> Weekday </th></tr>" + "\n"
            htmlwkday = htmlwkday  + htmltd.format(fulltxt=sdfrec.FullText,eml=emlnk) + "\n"
        htmlby = htmlby  + htmltd.format(fulltxt=sdfrec.FullText,eml=emlnk) + "\n"
    
    return [htmlwkday,htmlwkend,htmlby]


def recs2htmlbodyisldconf(featsdf,confsdf,htmltd="",urlink="",emlnk='',inpemail='gina.c.belleau@hawaii.gov',urlconflink='http://arcg.is/1qz8yT'):
    # merge relationship records from the child table to the current header record
    qx="\""
    htmlby = "\n"  #htmltxtd.format(q1="\"",urlink=urlinkx,q2="\"",island=sdfrec.Island,route=sdfrec.Route,begindate=sdfrec.beginDate,endate=sdfrec.enDate,intersfrom=sdfrec.IntersFrom,intersto=sdfrec.IntersTo) + "\n"
    htmltxt =  "\n" + "<tr><th> Islands </th></tr>" + "\n"
    htmlwkday =  "\n" + "<tr><th> -- </th></tr>" + "\n"
    htmlwkend =  "\n" + "<tr><th> -- </th></tr>" + "\n"
    wkend =0
    wkday =0
    ilist = featsdf['Island'].value_counts()
    for ile in ilist.items():
        isld = ile[0]
        ilsdf = featsdf.query("Island == '{}'".format(isld ))
        htmltxt =  "\n" + "<tr><th> {} </th></tr>".format(isld) + "\n"
        
        for ir,sdfrec in enumerate(ilsdf.itertuples()):   # two points are given                                                                                                                                                                                                                                                                                                                                                                                       
        # add two sets of columns from the related data to the header data frame
            oid = sdfrec.OBJECTID
            qoid = "ObjectIdM == {}".format(oid)                                                                                                                                                                                                                                                                                                                                                                                            
            confsdfoid = confsdf.query(qoid)
            cids = confsdfoid['ObjectidC'].value_counts() 
            cidlist = list(cids.to_dict().keys())
            coid = "ObjectIdC in  ({})".format(cidlist)                                                                                                                                                                                                                                                                                                                                                                                            
            confsdfcoid = confsdf.query(coid)
            conftxt = sdfrec.ConflicTxt + " conflicts with "
            for ix,confrec in enumerate(confsdfcoid.itertuples()):
                if ir == 0:
                    conftxt = conftxt + confrec.ConflicTxt
                else:
                    conftxt = conftxt + " and " + confrec.ConflicTxt
                            
            #htmlby = htmlby + htmltd.format(q1="\"",urldet=urlinkx,fldid="OBJECTID",fldval=sdfrec.OBJECTID,q2="\"",island=sdfrec.Island,route=sdfrec.Route,roadname=sdfrec.RoadName,intersfrom=sdfrec.IntersFrom,intersto=sdfrec.IntersTo,begindate=sdfrec.beginDate,endate=sdfrec.enDate) + "\n"
            if len(cidlist)>0:
                if len(inpemail)>0:
                    emlnk = emlnk.format(q1=qx,email2=inpemail,ln=sdfrec.CloseFact,rte=sdfrec.Route,isld=sdfrec.Island,q2=qx,q3=qx,q4=qx)
                elif len(sdfrec.l1email)>0:
                    emlnk = emlnk.format(q1=qx,email2=sdfrec.l1email,ln=sdfrec.CloseFact,rte=sdfrec.Route,isld=sdfrec.Island,q2=qx,q3=qx,q4=qx)
                elif len(sdfrec.l2email)>0:    
                    emlnk = emlnk.format(q1=qx,email2=sdfrec.l2email,ln=sdfrec.CloseFact,rte=sdfrec.Route,isld=sdfrec.Island,q2=qx,q3=qx,q4=qx)
                else:
                    emlnk=""    
                if sdfrec.wkEnd==1:
                    if wkend==0:
                        wkend=1
                        htmlwkend = htmlwkend + "\n" + "<tr><th> Weekend </th></tr>" + "\n"
                    htmlwkend = htmlwkend  + htmltd.format(conflicthtml=conftxt,eml=emlnk) + "\n"
                else:
                    if wkday==0:
                        wkday=1
                        htmlwkday = htmlwkday + "\n" + "<tr><th> Weekday </th></tr>" + "\n"
                    htmlwkday = htmlwkday  + htmltd.format(conflicthtml=conftxt,eml=emlnk) + "\n"
        htmlby = htmlby  + htmltd.format(conflicthtml=sdfrec.ConflicTxt,eml=emlnk) + "\n"
        htmltxt = htmltxt  + "\n" + htmlwkend + "\n" + htmlwkday + "\n"
    return [htmltxt,htmlby]



def recs2htmlbodyisld(featsdf,htmltd="",urlinkx="",emlnk='',inpemail='gina.c.belleau@hawaii.gov',urlconflink='http://arcg.is/1qz8yT'):
    # merge relationship records from the child table to the current header record
    qx="\""
    htmlby = "\n"  #htmltxtd.format(q1="\"",urlink=urlinkx,q2="\"",island=sdfrec.Island,route=sdfrec.Route,begindate=sdfrec.beginDate,endate=sdfrec.enDate,intersfrom=sdfrec.IntersFrom,intersto=sdfrec.IntersTo) + "\n"
    htmltxt =  "\n" + "<tr><th> Islands </th></tr>" + "\n"
    htmlwkday =  "\n" + "<tr><th> -- </th></tr>" + "\n"
    htmlwkend =  "\n" + "<tr><th> -- </th></tr>" + "\n"
    wkend =0
    wkday =0
    ilist = featsdf['Island'].value_counts()
    for ile in ilist.items():
        isld = ile[0]
        ilsdf = featsdf.query("Island == '{}'".format(isld ))
        htmltxt =  "\n" + "<tr><th> {} </th></tr>".format(isld) + "\n"
       
        for ir,sdfrec in enumerate(ilsdf.itertuples()):   # two points are given                                                                                                                                                                                                                                                                                                                                                                                       
        # add two sets of columns from the related data to the header data frame                                                                                                                                                                                                                                                                                                                                                                                             
            #htmlby = htmlby + htmltd.format(q1="\"",urldet=urlinkx,fldid="OBJECTID",fldval=sdfrec.OBJECTID,q2="\"",island=sdfrec.Island,route=sdfrec.Route,roadname=sdfrec.RoadName,intersfrom=sdfrec.IntersFrom,intersto=sdfrec.IntersTo,begindate=sdfrec.beginDate,endate=sdfrec.enDate) + "\n"
            if len(inpemail)>0:
                emlnk = emlnk.format(q1=qx,email2=inpemail,ln=sdfrec.CloseFact,rte=sdfrec.Route,isld=sdfrec.Island,q2=qx,q3=qx,q4=qx)
            elif len(sdfrec.l1email)>0:
                emlnk = emlnk.format(q1=qx,email2=sdfrec.l1email,ln=sdfrec.CloseFact,rte=sdfrec.Route,isld=sdfrec.Island,q2=qx,q3=qx,q4=qx)
            elif len(sdfrec.l2email)>0:    
                emlnk = emlnk.format(q1=qx,email2=sdfrec.l2email,ln=sdfrec.CloseFact,rte=sdfrec.Route,isld=sdfrec.Island,q2=qx,q3=qx,q4=qx)
            else:
                emlnk=""    
            if sdfrec.wkEnd==1:
                if wkend==0:
                    wkend=1
                    htmlwkend = htmlwkend + "\n" + "<tr><th> Weekend </th></tr>" + "\n"
                htmlwkend = htmlwkend  + htmltd.format(conflicthtml=sdfrec.ConflicTxt,eml=emlnk) + "\n"
            else:
                if wkday==0:
                    wkday=1
                    htmlwkday = htmlwkday + "\n" + "<tr><th> Weekday </th></tr>" + "\n"
                htmlwkday = htmlwkday  + htmltd.format(conflicthtml=sdfrec.ConflicTxt,eml=emlnk) + "\n"
        htmlby = htmlby  + htmltd.format(conflicthtml=sdfrec.ConflicTxt,eml=emlnk) + "\n"
        htmltxt = htmltxt  + "\n" + htmlwkend + "\n" + htmlwkday + "\n"
    return [htmltxt,htmlby]

def conflictids(sectsdfid,conflsdf):
    conflsdfids = []
    conflsdfids = [x.ObjectidC for x in conflsdf.itertuples() if x.ObjectIdM == sectsdfid and x.ObjectidC not in conflsdfids ]
    conflsdfids = list(dict.fromkeys(conflsdfids))
    return conflsdfids

def conflistids(sectsdfid,confeats):
    conflsdfids = "[" + ",".join(str(xfs.attributes['ObjectIdC']) for xfs in  confeats  if sectsdfid in xfs.attributes['ObjectIdM'] ) + "]"
#    conflncldelqry = "(ObjectIdM in ({}))".format(oids) # and beginDate<= '{}') or (enDate>= '{}' and enDate<= '{}')".format( begdt,endt,begdt,endt)
#    conflisdf = conflsdf.query()
#    conflsdfids = [x.ObjectIdC for x in conflsdf.itertupels() if x.ObjectIdM == sectsdfid ]
    return conflsdfids

def approverdefl1 (isld,creator,creationdate,approverl1,l1email,approverl2,l2email,globalid):
    defapp =  {'Maui' : 'robin.k.shishido@hawaii.gov', 'Lanai' : 'robin.k.shishido@hawaii.gov', 'Molokai' : 'robin.k.shishido@hawaii.gov', 'Kauai' : 'lawrence.j.dill@hawaii.gov', 'Oahu' : 'george.abcede@hawaii.gov', 'Hawaii' : 'harry.h.takiue@hawaii.gov' , 'HI' : 'gina.c.belleau@hawaii.gov'}
    if len(l1email)==0:
        if len(l2email)>0:
            l1email = l2email
        else:    
            if len(isld)>0:
                l1email = defapp[isld]
            else:
               l1email = defapp['HI']
    return l1email

# update user id and email when blank using x['Island'],x['ApproverL1'],x['l1email'],x['Creator'],x['CreationDate'],x['ApproverL2'],x['l2email'],x['globalid']
def approverdefl2 (isld,creator,creationdate,approverl1,l1email,approverl2,l2email,globalid):
    defapp =  {'Maui' : 'robin.k.shishido@hawaii.gov', 'Lanai' : 'robin.k.shishido@hawaii.gov', 'Molokai' : 'robin.k.shishido@hawaii.gov', 'Kauai' : 'lawrence.j.dill@hawaii.gov', 'Oahu' : 'george.abcede@hawaii.gov', 'Hawaii' : 'harry.h.takiue@hawaii.gov' , 'HI' : 'gina.c.belleau@hawaii.gov'}
    if len(l2email)==0:
        if len(isld)>0:
            l2email = defapp[isld]
        else:
            l2email = defapp['HI']
    return l2email

def strfwkdte(xt,h1=0):
    wkdte = 1
    if pd.notna(xt):
        wkdte = date.strftime(xt- timedelta(hours=h1),"%w") 
    
    return wkdte
    
    
def rtempt(lyrts,rtefc,lrte,bmpvalx,offs=0):
    if arcpy.Exists(mptbl):    
        if int(arcpy.GetCount_management(mptbl).getOutput(0)) > 0:
            arcpy.DeleteRows_management(mptbl)
    bmpval = bmpvalx
    rteFCSel = "RteSelected"
    rtevenTbl = "RteLinEvents"
    eveLinlyr = "lrtelyr" #os.path.join('in_memory','lrtelyr')
    arcpy.env.overwriteOutput = True
    if (len(rtefc)>0):
        flds = ['OBJECTID', 'SHAPE@JSON', 'ROUTE'] # selected fields in Route
        lrterows = arcpy.da.SearchCursor(lrte,flds)
        mpinscur.insertRow((rteid.upper(), bmpval,offs))
        dirnlbl = 'LEFT'
        arcpy.MakeRouteEventLayer_lr(lrte,fldrte,mptbl,eveProLines, eveLinlyr,ofFld.name,"ERROR_FIELD","ANGLE_FIELD",'NORMAL','ANGLE',dirnlbl)
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
                if insecgeo == None:
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
        print('Route {} not found using {} create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,bmpval,empval,offs ))
        logger.info('Route {} not found using {} to create section geometry layer {} , on Route {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(rteid,rteidx,lyrts,rteid,bmpvalx,bmpval,empval,offs ))
        featlnclrte = lyrts.query(where = "Route in  ({}{}{}) ".format(" '",rteidx,"' "),return_m=True,out_fields='*') #.sdf # + ,out_fields="globalid")
        ftlnclrte = featlnclrte.features
        if (len(ftlnclrte)>0):
            rtegeo = ftlnclrte[0].geometry
            geomrte = arcgis.geometry.Geometry(rtegeo)
            insecgeo = geomrte.project_as(sprefwgs84)
        else:
            insecgeo=None    
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
        if bmprte==None and emprte==None:
            insecgeo = three2twod(rtegeo)
            #insecgeo = Geometry({ "paths" : insecgeo , "spatialReference" : sprefwebaux })
            insecgeo =arcgis.geometry.Geometry({ "paths" : insecgeo , "spatialReference" : sprefwebaux }) #(insecgeo,sr=sprefwebaux)
            lengeo = insecgeo.length
            insecgeo = insecgeo.project_as(sprefwgs84 ) #sprefwebaux) #insecgeo.project_as(sprefwgs84)
            print('Blank value found for  Route {} ; Rte pre-geometry {} ; projected {} ; new {}  ; length : {} ; layer {} , rte {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format
                  (rteid,rtegeo,geomrte,insecgeo,lengeo,lyrname,rteid,bmpvalx,empvalx,bmprte,emprte,offs ))
            logger.error('Blank value found for Route {} ; Rte pre-geometry {} ; projected {} ; new {}  ; length : {} ; layer {} , rte {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format
                  (rteid,rtegeo,geomrte,insecgeo,lengeo,lyrname,rteid,bmpvalx,empvalx,bmprte,emprte,offs ))
        else:
            if bmprte==None:
                bmprte = emprte - 0.01
            if emprte==None:
                emprte = bmprte + 0.01
                
            bmprte = round(bmprte,3)
            emprte = round(emprte,3)
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
    print('Layer {} ; Route {} created section geometry {} ; original BMP : {} ; EMP : {} ; section BMP : {} ; EMP : {} ; offset {}.'.format(lyrname,rteid,insecgeo,bmpvalx,empvalx,bmpval,empval,offs ))
    return insecgeo





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
        rtegeox = [[ x for sublist in rtepaths for x in sublist]]
        rtegeo['paths'] =  rtegeox
        featlnclrte.features[0].geometry['paths'] = rtegeox
        print("Rte {} feature {}".format(rteid,ftlnclrte))
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
        # new addition 6/8/2020
        if (rtept1[2] == None):
            rtept1[2] = 0
        if (rtept2[2] == None):    
            rtept2[2] = round(rteleng*3.2808333/5280.0,3)  # assuming route length is in meters
        bmprte = round(rtept1[2],3)
        emprte = round(rtept2[2],3)

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



# In[6]:


def checkstrings(featdata):
    for flds in featdata.fields:
        if flds['type'] == 'esriFieldTypeString':
            fldname = flds['name']
            featt = featdata["attributes"][fldsname]
            if len(featt) > flds['length']:
                featdata["attributes"][fldsname] = featt[0:flds['length']]
    return featdata
            


# In[ ]:


cbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p") # curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S")

shorelineclosid = 'rh4f-u3x6' # Shoreline https://highways.hidot.hawaii.gov/dataset/Overall-shoreline-Rankings/wufu-nx84 
# "ykms-ifs3"  # https://highways.hidot.hawaii.gov/PSS-Official/PSS-Projects-Closed-within-Last-Two-Calendar-years/ykms-ifs3
Shorelocdata = socradata.views.lookup(shorelineclosid)
Shorelocdrev = Shorelocdata.revisions.create_replace_revision()
shorelineclosrc = Shorelocdrev.source_from_dataset()
shorelinerc = shorelineclosrc.load()
shorelinerc.wait_for_finish()
shorelineinpscm  = shorelinerc.get_latest_input_schema()
shorelineoutscm = shorelineinpscm.get_latest_output_schema()
# build a configuration using the same settings (file parsing and data transformation rules) that was used to get our output. The action
# It maybe "update" or "replace"
shorelineconame = "Shoreline_Locations_config"
actype = "replace"  # "update"
shorelinebldconfig = None
try:
    shorelinebldconfig = socradata.configs.lookup(shorelineconame) # socradata.configs.lookup(shorelineconame)
    print("Date - {} ; Shoreline Locations Output Record Schema {} ;\n Build Config List : {} ".format(cbeg,shorelineconame,shorelineconfig))
except Exception as e:
    print('Date : {} ;\nError : {} ;   id {} not found  '.format(cbeg,str(e),shorelineconame))
if shorelinebldconfig == None:
    shorelinebldconfig = shorelineoutscm.build_config(shorelineconame, actype)
    print("Shoreline Locations Output Record Schema {} ;\n Build Config : {} ".format(shorelineoutscm,shorelinebldconfig))
print("Shoreline Locations Output Record Schema {} ;\n Build Config : {} ".format(shorelineoutscm,shorelinebldconfig))

shorelinerows = shorelineoutscm.rows(offset=0,limit=10000)
revdisc = Shorelocdrev.discard()
print("Shoreline Locations {}  Num records : {}".format(shorelineclosid,len(shorelinerows)))
#print("{}".format(projrows[0]))
shorelinesdf = pd.DataFrame.from_records(shorelinerows)
print("Shoreline Locations {}  SDF records : {}".format(shorelineclosid,len(shorelinesdf)))
shorelinesdflds = (shorelinesdf.columns)
shorelinesdf1 = shorelinesdf.head(1)
print ("Date : {} ; fields : {} \n first record {} ".format(cbeg,(shorelinesdflds),[shorelinesdf1[fld] for fld in shorelinesdf1]))



# In[ ]:


# In[13]:

cbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p") # curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S")

#print("In Schema : {} ; out Schema : {} ".format(shorelineinpscm,shorelineoutscm))
shorelinesdflds = (shorelinesdf.columns)
print("type {} Shoreline Locations {}  SDF  cols : {} and records : {}".format(type(shorelinesdf),shorelineclosid,shorelinesdflds ,len(shorelinesdf)))
for flds in shorelinesdf.columns:
       shorelinesdf[flds] = shorelinesdf.apply(lambda x : stripjson(x[flds]),axis=1)
shorelinesdflds = (shorelinesdf.columns)
print("{} - Shoreline Locations {}  SDF  cols : {} and num records : {}".format(cbeg,shorelineclosid,shorelinesdflds ,len(shorelinesdf)))



# In[ ]:


# Use data from Pandas Dataframe diShorelocRoutespdfcop
tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p") # curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S")
Shorelocsdf = deepcopy(shorelinesdf)
print (" PDF Columns : {} ; with columns  : {} . ".format( Shorelocsdf.columns , len(Shorelocsdf.columns)) )
shorelinegrpby = Shorelocsdf.groupby(['island','rte'])
print("Date :  {} ; Grp Data : {} ; Grp Count : {} ; Raw data : {}  ".format(tbeg,shorelinegrpby,shorelinegrpby.count(),Shorelocsdf))


# In[ ]:


tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p") # curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S")
shorelocflds = ['ranking', 'island', 'location', 'rte', 'mp', 'cresi',
       'remediation_alternative']
bmpcol = 'mp'
empcol = 'mp'
rteid = 'rte'
qrycol = rteid
rtelyrid = 'HiDOTRoutes'
offs = 0
qrykey = ''
#print("{}".format(Shorelocsdf[qrycol].head(1)))
qrystr = "{} != '{}'".format(qrycol,qrykey)
#Shorelocsdf = deepcopy(Shorelocsdf) #.query(qrystr)
listrtes = Shorelocsdf[rteid].value_counts()
print ("Date : {} ; number of Shoreloc Routes entered with {} = {} ; Routes : {} ; Counts : {}".format(tbeg,qrystr,len(Shorelocsdf),list(listrtes.keys()),list(listrtes.values)))
logger.info ("Date : {} ; number of Shoreloc Routes entered with {} = {} ; Routes : {} ; Counts : {}".format(tbeg,qrystr,len(Shorelocsdf),list(listrtes.keys()),list(listrtes.values)))
l=0
fldstring = [rteid,'island', 'location', 'rte', 'cresi', 'remediation_alternative']
fldfloat = [ 'ranking']
Shorelocsdf = Shorelocsdf.astype({col:float for col in fldfloat},errors='ignore')
Shorelocsdf = Shorelocsdf.astype({col:str for col in fldstring},errors='ignore')
listrtes = Shorelocsdf[rteid].value_counts()
    
print ("Date : {} ; number of Shoreloc Routes entered after transfromation ; Routes : {} ; Counts : {} ; Values : {} \n Data : {}".format(tbeg,len(Shorelocsdf),list(listrtes.keys()),list(listrtes.values),Shorelocsdf))
#logger.info ("number of Shoreloc Routes entered after transfromation ; Routes : {} ; Counts : {} ; Values : {} \n Data : {}".format(len(Shorelocsdf),list(listrtes.keys()),list(listrtes.values),Shorelocsdf))


# In[ ]:


# convert wkt to arcgis shape format
#shorelinesdf['mgeom'].apply(lambda x : print(x))
#Shorelocsdf['SHAPE'] = Shorelocsdf['mgeom'].apply(lambda x : wkt2arcgeom(x,sprefwgs84) ) # if len(str(x)) > 0 else None )
tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p") # curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S")
shorelocflds = Shorelocsdf.columns # ['ranking', 'island', 'location', 'rte', 'mp', 'cresi','remediation_alternative']
print("Date : {} ; Shoreline fields : {} ; \n Data Frame : {}".format(tbeg,shorelocflds,Shorelocsdf))
      
"""{
  "paths" : [[[-97.06138,32.837],[-97.06133,32.836],[-97.06124,32.834],[-97.06127,32.832]],
             [[-97.06326,32.759],[-97.06298,32.755]]],
  "spatialReference" : {"wkid" : 4326}
} """


# In[42]:


#CHECK FOR BLANKS 
#blncat = [["PM : " + x.responsibleperson + " ; FedId : "  + x.federalid + " ; Proj Id: "  + x.projectid + " ; " + x.projectnumber + " ; Design Office : " + x.design_office_design  + " ; County Project? "  +x.iscountyproject + " ; " + x.projecttitle]  for x in shorelinesdf.itertuples() if x.projectcategory not in ('syst presrv', 'safety', 'other', 'congest', 'capacity','compliance','modern')]
#print("Projects without categroy are {}".format(blncat)) 
#logger.info("Projects without categroy are {}".format(blncat)) 
#shorelinesdf['projectcategory'] = shorelinesdf['projectcategory'].apply(lambda x : 'syst presrv' if x in ('') else x) # 'syst presrv', 'safety', 'other', 'congest', 'capacity','compliance','modern')] ) # if len(str(x)) > 0 else None )
#blncat = [["PM : " + x.responsibleperson + " ; FedId : "  + x.federalid + " ; Proj Id: "  + x.projectid + " ; " + x.projectnumber + " ; Design Office : " + x.design_office_design  + " ; County Project? "  +x.iscountyproject + " ; " + x.projecttitle]  for x in shorelinesdf.itertuples() if x.projectcategory not in ('syst presrv', 'safety', 'other', 'congest', 'capacity','compliance','modern')]
#print("Projects without categroy are {}".format(blncat)) 
#logger.info("Projects without categroy are {}".format(blncat)) 
      


# In[ ]:


tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p") # curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S")
#qgis = GIS(profile="hisagolprof")
numfs = 5000 # number of items to query
#    sdItem = qgis.content.get(lcwebmapid)
ekOrg = False
hirtsTitle = 'HIDOTRoutes' # arcpy.GetParameter(0) #  'e9a9bcb9fad34f8280321e946e207378'
itypelrts="Feature Service" # "Feature Layer" # "Service Definition"
wmlrtsnm = 'HIDOTRoutes'
rteFCSelNm = 'rtesel'
tempPath = sys.path[0]
arcpy.env.overwriteOutput = True


# access the route feature layer , search for route source data
itypeHIShorelocsrc= "Feature Service" # "Feature Layer" #   # "Service Definition"

print("Date : {} ; Searching for route source {} from {} item for Service Title {} on AGOL...".format(tbeg,itypeHIShorelocsrc,portal_url,hirtsTitle))
fsroutesrc = webexsearch(qgis, hirtsTitle, userName, itypeHIShorelocsrc,numfs,ekOrg)
#qgis.content.search(query="title:{} AND owner:{}".format(ShorelocFSTitle, userName), item_type=itypeHIShorelocsrc,outside_org=False,max_items=numfs) #[0]
print (" Feature URL: {} ; Title : {} ; Id : {} ".format(fsroutesrc.url,fsroutesrc.title,fsroutesrc.id))
lyroutesrc = fsroutesrc.layers
# header layer
rtelyr = lyrsearch(lyroutesrc, wmlrtsnm)
print (" Feature : {} ; name : {} ; Id : {} ".format(wmlrtsnm,rtelyr.properties.name,rtelyr))


# In[ ]:


def rtelist(rtelyr,xRte,xBMPList,EMPList,offs,rtelyrid,fldrte='Route',i1=-999):
    bmplist = xBMPList.split(sep=',')
    emplist = xBMPList.split(sep=',')
    gx=[]
    print('Layer {} :  Route {} ; BMP : {} ; offset  : {} ; layer id {}.'.format(rtelyr,xRte,bmplist,offs,rtelyrid ))
    gxpath=''
    for i1,xBMP in enumerate(bmplist):
        try:
            xBMPf = float(xBMP)
        except Exception as e:
            xBMPF = xBMP
        
        sx = rtesectline(rtelyr,xRte,xBMPf-0.1,xBMPf+0.01,offs,fldrte)
        if len(sx)>0:
            gxpath = sx['paths'][0]
            gx.append(gxpath)
        print("Rte : {} ; MP : {} ; \n generated Geometry- {} ; \n Paths : {} ; \n Accum : {}".format(xRte,xBMP,sx,gxpath,gx))
    if len(gxpath)>0:
        sx['paths'] = gx
    else:
        sx = gx
    print("Rte : {} ; MP : {} ; \n Final generated Geometry- {} ; \n Paths : {} ; \n Accum : {}".format(xRte,xBMP,sx,gxpath,gx))
    return sx    

#print("{}".format(routesdf[qrycol].head(1)))
tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p") # curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S")
bmpcol = 'mp'
empcol = 'mp'
rteid = 'Route'
rteidpdf = 'rte'
qrycol = rteid

rtelyrid = 'HIDOTRoutes'
offs = 0
qrykey = ''
qrystr = "{} != '{}'".format(qrycol,qrykey)
Shorelocsdfy = deepcopy(Shorelocsdf)
print ("Date : {} ; number of Shoreline Routes with {} = {} and routes{} ".format(tbeg,qrystr,len(Shorelocsdf),Shorelocsdf[rteidpdf].to_list()))
#logger.info ("number of Routes entered with {} = {} and routes{} ".format(qrystr,len(Shorelocsdf),Shorelocsdf[rteidpdf].to_list()))
Shorelocsdf['SHAPE']= Shorelocsdf.apply(lambda x : rtelist(rtelyr,str(x[rteidpdf]),x[bmpcol],x[empcol],offs,rtelyrid),axis=1)

#Shorelocsdf['SHAPE']= Shorelocsdf.apply(lambda x : rtesectline(rtelyr,x[rteidpdf],x[bmpcol]-0.01,x[empcol]+0.01,offs),axis=1) #(rtelyr,rte,xBMP,xEMP,offs,fldrte)
print ("SDF coumns {} and total count {}".format(Shorelocsdf.columns,len(Shorelocsdf.columns),Shorelocsdf['SHAPE'].head(1)))

print(Shorelocsdf[rteidpdf].value_counts(rteidpdf))
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
Shoreloccsvnm = r'HiDOT_shoreline_Project_Limits.csv'
Shorelocsdfile = os.path.join(inpath,Shoreloccsvnm)
Shorelocsdf.to_csv(Shorelocsdfile)
print("{} datatypes -  {}".format(Shorelocsdfile , Shorelocsdf.dtypes))


# In[ ]:


# In[43]:
tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p") # curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S")

# Create the route geoemtry data

#shorelinesdf['categoshel'] = shorelinesdf['projectsubcategory'].apply(lambda x : shelgroup(x) ) # if len(str(x)) > 0 else None )
print("Df type {} ; Shape head : {} ".format(type(Shorelocsdf),Shorelocsdf['SHAPE'].head(5)))
Shorelocsdf.fillna('',inplace=True)
punidist = Shorelocsdf['island'].value_counts()
punihwy = Shorelocsdf['rte'].value_counts()
dfpunidist = punidist.keys().to_list()
dfpunihwy = punihwy.keys().to_list()
punidistjson = ({x : punidist[x] for x in list(punidist.keys())})    
punihwyjson = ({x : punihwy[x] for x in list(punihwy.keys())})    
print(" Pre-update Islands : {} ; Routes : {} ".format(punidistjson,punihwyjson))
#shorelinesdf['district'] = shorelinesdf['projectcategory'].apply(lambda x : shelgroup(x) ) # if len(str(x)) > 0 else None ) (catfld):
#shorelinesdf['hwydist'] = shorelinesdf['district'].apply(lambda x : shelgroup(x) ) # if len(str(x)) > 0 else None )
#shorelineshp= shorelinesdf.drop(['mgeom', 'lgeom'], axis=1)
lunidist = Shorelocsdf['island'].value_counts()
dflunidist = lunidist.keys().to_list()
lunicatjson = ({x : lunidist[x] for x in list(lunidist.keys())})    
print("Date : {} ; Pre Update category : {} ; Post update Category : {} ".format(tbeg,punidistjson,lunicatjson))    
logger.info("Date : {} ; Pre Update category : {} ; Post update Category : {} ".format(tbeg,punidistjson,lunicatjson))    


# In[ ]:


# In[47]:


idx = pd.Index(Shorelocsdf)
#idx.set_names(['OBJECTID'],inplace=True) 
#Shorelocsdf['SHAPE'].apply(lambda x : print((x)))
print("Columns : {} ; num feats = {}".format(Shorelocsdf.columns,len(Shorelocsdf)))
csvfilenm = r"Shorelocprojects.csv"
csvfile = os.path.join(rptpath,csvfilenm) 
Shorelocsdf.to_csv(csvfile)
print("Path Output  : {} ;  file : {} ".format(rptpath,csvfile))    


# In[ ]:



tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p") # curDate = datetime.strftime(datetime.today(),"%Y%m%d%H%M%S")

# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print ("Date : {} ;  dataframe records  : {}  ".format(tbeg,len(shorelinesdf)))
#idx= pd.Index(shorelinesdf) #(ignore_index=True)  for concat
projgeoac = gac(Shorelocsdf)
projswgs84 =  projgeoac.set_geometry('SHAPE',sr=sprefwgs84)
Shorelocsdfx = gac.from_df(Shorelocsdf,  sr=sprefwgs84, geometry_column='SHAPE')
Shorelocgacx = gac(Shorelocsdfx)
profeats = Shorelocgacx.to_featureset()
print (" sdf features  : {} ; {} geoemtry ; fields {}  ".format(len(profeats),profeats.geometry_type,profeats.fields))
logger.info (" sdf features  : {} ; {} geoemtry ; fields {}  ".format(len(profeats),profeats.geometry_type,profeats.fields))


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
ShorelocFSTitle = 'HIDOT Shoreline Mitigations Projects' # 'Shoreline Mitigation Limits' # 'HIDOT Shoreline Mitigations Limits' # arcpy.GetParameter(0) 
itypeHIShorelocsrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
HIShorelocnm = 'Shoreline Mitigation Limits' # 'HIDOT Shoreline Projects Limits'
HIShorelocLyrnm = 'Shoreline Mitigation Limits'

hirtsTitle = 'HIDOTRoutes' # arcpy.GetParameter(0) #  'e9a9bcb9fad34f8280321e946e207378'
itypelrts="Feature Service" # "Feature Layer" # "Service Definition"
wmlrtsnm = 'HIDOTRoutes'
rteFCSelNm = 'rtesel'
servicename =  ShorelocFSTitle # "HiDOT_Fatal_HIShoreloch_Entry" # 
tempPath = sys.path[0]
arcpy.env.overwriteOutput = True

logger.info(" Title : {} Geometry Processing begins at {} ".format(ShorelocFSTitle,tbeg))                                                                                                                                                                                                                                                                                                                                                                                   
print("Title : {}  Geometry Processing begins at {} ".format(ShorelocFSTitle,tbeg))                                                                                                                                                                                                                                                                                                                                                                                   

#print("Temp path : {}".format(tempPath))
# ArcGIS user credentials to authenticate against the portal
credentials = { 'userName' : 'dot_mmekuria', 'passWord' : '********'}
userName = credentials['userName'] # arcpy.GetParameter(2) # 
passWord = credentials['passWord'] # # arcpy.GetParameter(3) # "ChrisMaz"
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
print (" Query if {} layer exists as {}. ".format (ShorelocFSTitle,itype))
logger.info (" Query if {} layer exists as {}. ".format (ShorelocFSTitle,itype))
prjlyrdelist = "['{}']".format(ShorelocFSTitle)
#    sdItem = qgis.content.get(lcwebmapid)
# search for maintenance source data
print("Searching for feature source {} from {} item for user {} and Service Title {} on AGOL...".format(itype,portal_url,userName,servicename))
logger.info("Searching for lane closure source {} from {} item for user {} and Service Title {} on AGOL...".format(itype,portal_url,userName,servicename))
HIShorelocsrc = webexsearch(qgis, servicename, userName, itype,numfs,ekOrg)
#qgis.content.search(query="title:{} AND owner:{}".format(prjstSrcFSTitle, userName), item_type=itype,outside_org=False,max_items=numfs) #[0]
#print (" Content search result : {} ; ".format(HIShorelocsrc))
if HIShorelocsrc != None:
    print (" Feature URL: {} ; Title : {} ; Id : {} ".format(HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id))
    logger.info (" Feature URL: {} ; Title : {} ; Id : {} ".format(HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id))
else:
    print (" Feature : {} ; with layer  : {} does not exist. ".format(servicename ,HIShorelocnm))
    logger.info (" Feature : {} ; with layer  : {} does not exist. ".format(servicename,HIShorelocnm))
    


# In[ ]:


tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p")
#tlocal = datetime.fromtimestamp(x1/1e3 , tzlocal.get_localzone())
# if layer data does not exist import fresh data into ArcGIS from excel
itypeHIShorelocsrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
ShorelocFSTitle = 'HIDOT Shoreline Mitigation Projects' # arcpy.GetParameter(0) 
itypeHIShorelocsrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
HIShorelocnm = 'HIDOT Shoreline Mitigation Limits' #'HiDOTShorelocORTP2045 Project Limits'
HIShorelocLyrnm = 'Shoreline Mitigation Limits'

try:
    #curDate = strftime("%Y%m%d%H%M%S") 
    userName= "dot_mmekuria"
    if HIShorelocsrc != None:
        print ("Date : {} ; Feature URL: {} ; Title : {} ; Id : {} ".format(tbeg,HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id))
        logger.info ("Date : {} ; Feature URL: {} ; Title : {} ; Id : {} ".format(tbeg,HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id))
        # ID or Title of the feature service to update
        #print (" Content search result : {} ; ".format(fsprjstsrc))
        Shoreloclyrs = HIShorelocsrc.layers
        lyrnamelist = [ x.properties.name for i1,x in enumerate(Shoreloclyrs,1)]
        # header layer
        fs = len(Shoreloclyrs) #len(lyrtefs)
        if (fs>0):
            Shoreloclyr = lyrsearch(Shoreloclyrs, HIShorelocnm)
        else:
            print ("Date : {} ; No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(tbeg,HIShorelocnm,HIShorelocsrc.title,HIShorelocsrc.id,lyrnamelist))
            logger.info ("Date : {} ; No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(tbeg,HIShorelocnm,HIShorelocsrc.title,HIShorelocsrc.id,lyrnamelist))
            
    else:
        print ("Date : {} ; Feature : {} ; with layer  : {} does not exist. ".format(tbeg,servicename ,HIShorelocnm))
        #logger.info (" Feature : {} ; with layer  : {} does not exist. ".format(servicename,HIShorelocnm))
        Shoreloclyr = Shorelocgacx.to_featurelayer(title=HIShorelocnm, gis=qgis, tags='Projects, HDOT,shoreline, Routes', folder=None)
        print(" layer : {} created on Date : {} ; ".format(Shoreloclyr,tbeg))
        emergefcol = Shorelocgacx.to_feature_collection(name="{}_col".format(HIShorelocnm), drawing_info=None, extent=None, global_id_field=None)
        
    print ("Date : {} ; Feature URL: {} ; Shorelocgacx Title : {} ; Id : {} \n Layers - {}  ".format(tbeg,HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id,lyrnamelist))
    #logger.info ("Date : {} ; Feature URL: {} ; Title : {} ; Id : {} \n Layers - {} ".format(tbeg,HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id,lyrnamelist))
except Exception as e:
    print(' Date : {} ;Error : {} ;   layer {} Project status script '.format(tbeg,str(e),HIShorelocnm))
    #logger.error('Date : {} ; Error : {} ;  layer {} Project status script '.format(tbeg,str(e),HIShorelocnm ))


# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, os
plt.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#import arcgis
#from arcgis.gis import GIS
tbeg = datetime.today().strftime("%A, %B %d, %Y at %H:%M:%S %p")
#tlocal = datetime.fromtimestamp(x1/1e3 , tzlocal.get_localzone())

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
ShorelocFSTitle = 'Shoreline Mitigation Limits' # arcpy.GetParameter(0) 
itypeHIShorelocsrc= "Feature Service" #  "Feature Layer" # "Feature Service" #   # "Service Definition"
HIShorelocnm = 'Shoreline Mitigation Limits'
HIShorelocLyrnm = 'Shoreline Mitigation Limits'
inoutside = False
max_items_value= 1000
#equsgsmap = qgis.content.get("31cfc5b138e24dee866c457948773ac4")
#print("Title : {} - type : {} ; created  : {} - {} ; Modified : {} - {} ".format(equsgsmap.title,equsgsmap.type,equsgsmap.created,datetime.fromtimestamp(equsgsmap.created/1e3),equsgsmap.modified,datetime.fromtimestamp(equsgsmap.modified/1e3)))
#for item in equsgsmap:
#    print("Item : {}".format(item))
search_result = qgis.content.search(query= "title:{} AND owner:{}".format(ShorelocFSTitle,userName), 
                                          item_type=itypeHIShorelocsrc, max_items=max_items_value, outside_org=inoutside)
print("Date : {} ; Title : {} - type : {} ; found   : {} ".format(tbeg,ShorelocFSTitle,itypeHIShorelocsrc,search_result))


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
ShorelocFSTitle = 'Shoreline Mitigation Limits' # arcpy.GetParameter(0) 
itypeHIShorelocsrc= "Feature Service" #  "Feature Layer" # "Feature Service" #   # "Service Definition"
HIShorelocnm = 'Shoreline Mitigation Limits'
HIShorelocLyrnm = 'Shoreline Mitigation Limits'

hirtsTitle = 'HIDOTRoutes' # arcpy.GetParameter(0) #  'e9a9bcb9fad34f8280321e946e207378'
itypelrts="Feature Service" # "Feature Layer" # "Service Definition"
wmlrtsnm = 'HIDOTRoutes'
rteFCSelNm = 'rtesel'
servicename =  ShorelocFSTitle # "HiDOT_Fatal_HIShoreloch_Entry" # 
tempPath = sys.path[0]
arcpy.env.overwriteOutput = True

logger.info("Date : {} ; Title : {} Geometry Processing begins at {} ".format(tbeg,ShorelocFSTitle,tbeg))                                                                                                                                                                                                                                                                                                                                                                                   
print("Date : {} ; Title : {}  Geometry Processing begins at {} ".format(tbeg, ShorelocFSTitle,tbeg))                                                                                                                                                                                                                                                                                                                                                                                   

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
print (" Query if {} layer exists as {}. ".format (ShorelocFSTitle,itype))
logger.info (" Query if {} layer exists as {}. ".format (ShorelocFSTitle,itype))
prjlyrdelist = "['{}']".format(ShorelocFSTitle)
#    sdItem = qgis.content.get(lcwebmapid)
# search for maintenance source data
print("Searching for feature source {} from {} item for user {} and Service Title {} on AGOL...".format(itype,portal_url,userName,servicename))
logger.info("Searching for lane closure source {} from {} item for user {} and Service Title {} on AGOL...".format(itype,portal_url,userName,servicename))
HIShorelocsrc = webexsearch(qgis, servicename, userName, itype,numfs,ekOrg)
#qgis.content.search(query="title:{} AND owner:{}".format(prjstSrcFSTitle, userName), item_type=itype,outside_org=False,max_items=numfs) #[0]
#print (" Content search result : {} ; ".format(HIShorelocsrc))
if HIShorelocsrc != None:
    print ("Date: {} ; Feature URL: {} ; Title : {} ; Id : {} ".format(tbeg,HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id))
    logger.info ("Date: {} ; Feature URL: {} ; Title : {} ; Id : {} ".format(tbeg,HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id))
else:
    print (" Date : {} ; Feature : {} ; with layer  : {} does not exist. ".format(tbeg,servicename ,HIShorelocnm))
    logger.info ("Date : {} ; Feature : {} ; with layer  : {} does not exist. ".format(tbeg,servicename,HIShorelocnm))
    


# In[ ]:


def regsub(x,cmpx=r'[?\n+]'):
    if x is None:
        return x
    return re.sub(cmpx, '|',x)

rteidpdf = 'rte'
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
Shorelocsdfx[rteidpdf] = Shorelocsdf[rteidpdf].apply(lambda x : regsub(x,cmpy)) 
listrtes = Shorelocsdfx[rteidpdf].value_counts()
print ("date : {} , number of HiDOT Shoreloc Routes entered with {} = {} ; Routes : {} ; Counts : {}".format(tbeg,cmpy,len(Shorelocsdfx),list(listrtes.keys()),list(listrtes.values)))
#logger.info ("number of HiDOT Shoreloc Routes entered with {} = {} ; Routes : {} ; Counts : {}".format(cmpy,len(Shorelocsdfx),list(listrtes.keys()),list(listrtes.values)))


# In[ ]:


fldrte='highway'
offset=0
# Process geometry
# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print (" dataframe type  : {}  ".format(type(Shorelocsdf)))
#idx= pd.Index(shorelinesdf) #(ignore_index=True)  for concat
# delete existing data first
#Shorelocrenamecols = {'Route' : 'Route'}
Shorelocsdf = deepcopy(Shorelocsdf)
#Shorelocsdf.rename (columns=Shorelocrenamecols,inplace=True)
Shorelocgeoac = gac(Shorelocsdf)
Shorelocwgs84 =  Shorelocgeoac.set_geometry('SHAPE',sr=sprefwgs84)
#Shorelocwgs84 =  Shorelocgeoac.project(sprefwgs84)

#Shorelocsw2ysdfx = gac.from_df(routesdf,  sr=sprefwgs84, geometry_column='SHAPE')
#Shorelocgeoacx = gac(Shorelocsw2ysdfx)
Shorelocfeats = Shorelocgeoac.to_featureset()
print ("Date : {} ; features length : {} ; feature {} ".format(tbeg,len(Shorelocfeats),Shorelocfeats))


# In[ ]:


# if layer data does not exist import fresh data into ArcGIS from excel
itypeHIShorelocsrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
ShorelocFSTitle = 'Shoreline Mitigation Limits' # 'HiDOT Shoreline Project Limits' # arcpy.GetParameter(0) 
itypeHIShorelocsrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
HIShorelocnm = 'Shoreline Mitigation Limits' # 'Shoreline Mitigation Limits' #'HiDOTShorelocORTP2045 Project Limits'
HIShorelocLyrnm = 'Shoreline Mitigation Limits'

try:
    #curDate = strftime("%Y%m%d%H%M%S") 
    userName= "dot_mmekuria"
    if HIShorelocsrc != None:
        print (" Feature URL: {} ; Title : {} ; Id : {} ".format(HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id))
        logger.info (" Feature URL: {} ; Title : {} ; Id : {} ".format(HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id))
        # ID or Title of the feature service to update
        #print (" Content search result : {} ; ".format(fsprjstsrc))
        Shoreloclyrs = HIShorelocsrc.layers
        lyrnamelist = [ x.properties.name for i1,x in enumerate(Shoreloclyrs,1)]
        # header layer
        fs = len(Shoreloclyrs) #len(lyrtefs)
        if (fs>0):
            Shoreloclyr = lyrsearch(Shoreloclyrs, HIShorelocnm)
        else:
            print (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(HIShorelocnm,HIShorelocsrc.title,HIShorelocsrc.id,lyrnamelist))
            logger.info (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(HIShorelocnm,HIShorelocsrc.title,HIShorelocsrc.id,lyrnamelist))
            
    else:
        print (" Feature : {} ; with layer  : {} does not exist. ".format(servicename ,HIShorelocnm))
        logger.info (" Feature : {} ; with layer  : {} does not exist. ".format(servicename,HIShorelocnm))
        Shoreloclyr = Shorelocgeoac.to_featurelayer(title=HIShorelocnm, gis=qgis, tags='Projects, HDOT,shoreline, Routes', folder=None)
        print(" layer : {} created ".format(Shoreloclyr))
        emergefcol = Shorelocgeoac.to_feature_collection(name="{}_col".format(HIShorelocnm), drawing_info=None, extent=None, global_id_field=None)
        
    print (" Feature URL: {} ; Title : {} ; Id : {} \n Layers - {}  ".format(HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id,lyrnamelist))
    logger.info (" Feature URL: {} ; Title : {} ; Id : {} \n Layers - {} ".format(HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id,lyrnamelist))
except Exception as e:
    print(' Error : {} ;   layer {} Project status script '.format(str(e),HIShorelocnm))
    logger.error(' Error : {} ;  layer {} Project status script '.format(str(e),HIShorelocnm ))


# In[ ]:


import ipywidgets as widgets

def calc_dist(moahu, g):
    print("Computing length of drawn polyline...")
    length = lengths(g['spatialReference'], [g], "", "geodesic")
    print("Length: " + str(length[0]) + " m.")
    return g


#Shoreloclyr = Shorelocgeoac.to_featurelayer(title=(Shorelocintnm+'_test'), gis=qgis, tags='projects, pss, HDOT, maintenance, repair', folder=None)

# text box widget
emap = qgis.map("Oahu,Hawaii")
#emap.extent = Shoreloclyr.properties.extent
#emap
emap.add_layer(Shoreloclyr)


# In[ ]:


print( Shoreloclyr.properties.extent)
print( [ Shoreloclyr.properties.extent['xmin'],Shoreloclyr.properties.extent['ymin'],Shoreloclyr.properties.extent['xmax'],Shoreloclyr.properties.extent['ymax']])
emap.extent = [ Shoreloclyr.properties.extent['xmin'],Shoreloclyr.properties.extent['ymin'],Shoreloclyr.properties.extent['xmax'],Shoreloclyr.properties.extent['ymax']]


# In[ ]:


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
itypeHIShorelocsrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
ShorelocFSTitle = 'Shoreline Mitigation Limits' # 'HiDOT  Shoreline Project Limits' # arcpy.GetParameter(0) 
itypeHIShorelocsrc= "Feature Service" # "Feature Layer" #   # "Service Definition"
HIShorelocnm = ' Shoreline Mitigation Limits' #'HiDOTShorelocORTP2045 Project Limits'
HIShorelocLyrnm = ' Shoreline Mitigation Limits'


if HIShorelocsrc != None:

    # process the mile post data into geometry 
    # HIShoreloc layers
    fHIShorelocnm = HIShorelocnm
    HIShoreloclyr = lyrsearch(HIShorelocsrc, HIShorelocnm)
    if HIShoreloclyr != None:
        HIShorelocdf = HIShoreloclyr.query(as_df=True)
        HIShorelocflds = [fd.name for fd in HIShoreloclyr.properties.fields]

    #'msgbox tdate
        datesectqry = "{} {}".format(HIShorelocnm, HIShorelocflds)

        print ("Shoreloc Query {} ; {} number of Shoreloc Routes {} ".format(datesectqry,HIShorelocdf['rte'].value_counts(),len(HIShorelocdf)))

        qrycol = 'Route'

        qrykey = ''
        qrystr = "{} != '{}'".format(qrycol,qrykey)
        milepostdf = HIShorelocdf.query(qrystr)
        print ("number of Shoreloc Routes entered with {} = {}".format(qrystr,len(milepostdf)))
    #logpath = r"D:\MyFiles\HWYAP\HIShoreloces\logs"
    #rptpath = r"D:\MyFiles\HWYAP\HIShoreloces\reports"

        rptname = "HIShorelocDataMilePost.csv"
        csvfile = os.path.join(rptpath, rptname)
        milepostdf.to_csv(csvfile)
    else:
        print ("Shoreloc Source {} ; does not contain layer named {} ; Query Result  {} ".format(HIShorelocsrc, HIShorelocnm,HIShoreloclyr))
        
    #for srow in  milepostdf:
    


# In[ ]:


print(routesdf[rteid].value_counts())
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
print("{}".format(routesdf.dtypes))

print(routesdf['Route'].value_counts())
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
print(Shorelocsdf['Route'].value_counts())
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
Shoreloccsvnm = r'HiDOT Shoreline Project Limits.csv'
Shorelocsdfile = os.path.join(inpath,Shoreloccsvnm)
routesdf.to_csv(Shorelocsdfile)
print("{}".format((routesdf.dtypes)))


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
#Shorelocsdf = deepcopy(routesdf)
print ("number of Shoreline Routes with {} = {} and routes{} ".format(qrystr,len(Shorelocsdf),Shorelocsdf[rteid].to_list()))
logger.info ("number of Routes entered with {} = {} and routes{} ".format(qrystr,len(Shorelocsdf),Shorelocsdf[rteid].to_list()))
Shorelocsdf['SHAPE']= Shorelocsdf.apply(lambda x : multirtes(rtelyr,str(x[rteid]),x[bmpcol],x[empcol],offs,rtelyrid),axis=1)
print ("SDF coumns {} and total count {}".format(Shorelocsdf.columns,len(Shorelocsdf.columns),Shorelocsdf['SHAPE'].head(1)))

print(Shorelocsdf[rteid].value_counts(rteid))
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
Shoreloccsvnm = r'HiDOT Shoreline Project Limitsy.csv'
Shorelocsdfile = os.path.join(inpath,Shoreloccsvnm)
Shorelocsdf.to_csv(Shorelocsdfile)
print("{}".format((Shorelocsdf.dtypes)))


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
#Shorelocsdf = deepcopy(routesdf)
print ("number of Shoreline Routes with {} = {} and routes{} ".format(qrystr,len(Shorelocsdf),Shorelocsdf[rteid].to_list()))
logger.info ("number of Routes entered with {} = {} and routes{} ".format(qrystr,len(Shorelocsdf),Shorelocsdf[rteid].to_list()))
Shorelocsdf['SHAPE']= Shorelocsdf.apply(lambda x : multirtes(rtelyr,str(x[rteid]),x[bmpcol],x[empcol],offs,rtelyrid),axis=1)
print ("SDF coumns {} and total count {}".format(Shorelocsdf.columns,len(Shorelocsdf.columns),Shorelocsdf['SHAPE'].head(1)))

print(Shorelocsdf[rteid].value_counts(rteid))
#routesdf['Event_Approx_End_Date'] = pd.to_datetime(routesdf['Event_Approx_End_Date'],format="%Y-%m-%d %H:%M:%S", errors='coerce')
Shoreloccsvnm = r'HiDOT Shoreline Project Limitsy.csv'
Shorelocsdfile = os.path.join(inpath,Shoreloccsvnm)
Shorelocsdf.to_csv(Shorelocsdfile)
print("{}".format((Shorelocsdf.dtypes)))


# In[ ]:


try:
    #curDate = strftime("%Y%m%d%H%M%S") 
    userName= "dot_mmekuria"
    if HIShorelocsrc != None:
        print (" Feature URL: {} ; Title : {} ; Id : {} ".format(HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id))
        logger.info (" Feature URL: {} ; Title : {} ; Id : {} ".format(HIShorelocsrc.url,HIShorelocsrc.title,HIShorelocsrc.id))
        # ID or Title of the feature service to update
        #print (" Content search result : {} ; ".format(fsprjstsrc))
        Shoreloclyrs = HIShorelocsrc.layers
        lyrnamelist = [ x.properties.name for i1,x in enumerate(Shoreloclyrs,1)]
        # header layer
        fs = len(Shoreloclyrs) #len(lyrtefs)
        if (fs>0):
            Shoreloclyr = lyrsearch(Shoreloclyrs, HIShorelocnm)
            print (" Found {} Layer {} with  id : {} ; Layer {}   ".format(HIShorelocnm,HIShorelocsrc.title,HIShorelocsrc.id,Shoreloclyr))
            logger.info (" Found {} Layer {} with  id : {} ; Layer {}   ".format(HIShorelocnm,HIShorelocsrc.title,HIShorelocsrc.id,Shoreloclyr))
        else:
            print (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(HIShorelocnm,HIShorelocsrc.title,HIShorelocsrc.id,lyrnamelist))
            logger.info (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(HIShorelocnm,HIShorelocsrc.title,HIShorelocsrc.id,lyrnamelist))
    else:
        print (" No  Layer {} with  Title  {} Found ".format(HIShorelocnm,HIShorelocsrc))
        logger.info (" No  Layer {} with  Title {} found  ".format(HIShorelocnm,HIShorelocsrc))
except Exception as e:
    print(' Error : {} ;   layer {} Project status script '.format(str(e),HIShorelocnm))
    logger.error(' Error : {} ;  layer {} Project status script '.format(str(e),HIShorelocnm ))


# In[ ]:


fldrte='Route'
offset=0
# Process geometry
# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print (" dataframe type  : {}  ".format(type(routexdf)))
#idx= pd.Index(shorelinesdf) #(ignore_index=True)  for concat
# delete existing data first
#Shorelocrenamecols = {'Route' : 'Route'}
Shorelocsdf = deepcopy(Shorelocsdf)
#Shorelocsdf.rename (columns=Shorelocrenamecols,inplace=True)
Shorelocgeoac = gac(Shorelocsdf)
Shorelocwgs84 =  Shorelocgeoac.set_geometry('SHAPE',sr=sprefwgs84)
#Shorelocwgs84 =  Shorelocgeoac.project(sprefwgs84)

#Shorelocsw2ysdfx = gac.from_df(routesdf,  sr=sprefwgs84, geometry_column='SHAPE')
#Shorelocgeoacx = gac(Shorelocsw2ysdfx)
Shorelocfeats = Shorelocgeoac.to_featureset()
print (" features length : {} ; feature {} ".format(len(Shorelocfeats),Shorelocfeats))


# In[ ]:


Shoreloclyrs = HIShorelocsrc.layers
Shoreloclyr = lyrsearch(Shoreloclyrs, HIShorelocnm)
fldrte='Route'
offset=0
print("type : {} ; recordset : {} ".format(Shoreloclyrs,Shoreloclyr))
print("Query Features : {} ".format(Shoreloclyr.query()))
# Process geometry
# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print (" dataframe type  : {}  ".format(type(routexdf)))
#idx= pd.Index(shorelinesdf) #(ignore_index=True)  for concat
# delete existing data first
delayerfeatures(Shoreloclyr)
Shorelocrenamecols = {'Route' : 'Route'}
Shorelocsdf = deepcopy(Shorelocsdf)
Shorelocsdf.rename (columns=Shorelocrenamecols,inplace=True)
Shorelocgeoac = gac(Shorelocsdf)
Shorelocwgs84 =  Shorelocgeoac.set_geometry('SHAPE',sr=sprefwgs84)
#Shorelocwgs84 =  Shorelocgeoac.project(sprefwgs84)

#Shorelocsw2ysdfx = gac.from_df(routesdf,  sr=sprefwgs84, geometry_column='SHAPE')
#Shorelocgeoacx = gac(Shorelocsw2ysdfx)
Shorelocfeats = Shorelocgeoac.to_featureset()
print (" features length : {} ; feature {} ".format(len(Shorelocfeats),Shorelocfeats))
# add to existing  layer 
resadd  = assyncadds(Shoreloclyr,Shorelocfeats)
print (" sdf features  : {} ; result {} ".format(len(Shorelocfeats),resadd))


# In[ ]:


print (" features length : {} ; feature {} ".format(len(Shorelocfeats),Shorelocfeats))


# In[ ]:


Shoreloclyrs = HIShorelocsrc.layers
Shoreloclyr = lyrsearch(Shoreloclyrs, HIShorelocnm)
fldrte='Route'
offset=0
print("type : {} ; recordset : {} ".format(Shoreloclyrs,Shoreloclyr))
print("Query Features : {} ".format(Shoreloclyr.query()))
# Process geometry
# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print (" dataframe type  : {}  ".format(type(routexdf)))
#idx= pd.Index(shorelinesdf) #(ignore_index=True)  for concat

Shorelocsdf = deepcopy(Shorelocsdf)
Shorelocgeoac = gac(Shorelocsdf)
Shorelocwgs84 =  Shorelocgeoac.set_geometry('SHAPE',sr=sprefwgs84)
#Shorelocwgs84 =  Shorelocgeoac.project(sprefwgs84)

#Shorelocsw2ysdfx = gac.from_df(routesdf,  sr=sprefwgs84, geometry_column='SHAPE')
#Shorelocgeoacx = gac(Shorelocsw2ysdfx)
Shorelocfeats = Shorelocgeoac.to_featureset()
# add to existing  layer 
resadd  = assyncaddspt(Shoreloclyr,Shorelocfeats)
print (" sdf features  : {} ; result {} ".format(len(Shorelocfeats),resadd))

def rtefeat(x,Shoreloclyr,rtelyr,offset,fldrte='Route'):
    print ("{}".format(frow))
    idx = x.index
    rteid = x.Route_Num
    bmpvalx = x.BMP
    empvalx = x.EMP
    gx = rtesectmp(rtelyr,rteid,bmpvalx,empvalx,offset,fldrte) # rtempt(rtelyr,rteFCSelNm,rteid,bmpvalx,offset,fldrte)
    resupdate = assyncadds(Shorelocintlyr,newfset) 
    
    print("type : {} ; recordset : {} \n - type {} - geom : {} \n\n ".format(type(frow),frow.SHAPE,type(gx),gx))
    sdfrow = geomilepostdf.query("globalid=='{}'".format(frow.globalid))
    print("type : {} ; updated geometry : {} \n - shape col : {} \n\n ".format(type(sdfrow),sdfrow.index[0],sdfrow['SHAPE']))
    sdfrow.loc[sdfrow.index[0],'SHAPE'] = [gx]  # sdfrow.apply(lambda x : gx , axis=1 ) # gx # sdfrow.apply(lambda x : gx,axis=1 ) .loc[0,'SHAPE']
    print("type : {} ; updated geometry : {} \n - shape col : {} \n\n ".format(type(sdfrow),sdfrow,sdfrow['SHAPE']))
    newfset = gac(sdfrow).to_featureset()
    print ("updated : {} \n\n".format(newfset.to_dict()))
    resupdate = assyncedits(Shorelocintlyr,newfset) 
    print("result : {}".format(resupdate))    

def addsdfeats(x,Shoreloclyr,rtelyr,offset,fldrte='Route'):
    print ("{}".format(frow))
    idx = x.index
    rteid = x.Route_Num
    bmpvalx = x.BMP
    empvalx = x.EMP
    gx = rtesectmp(rtelyr,rteid,bmpvalx,empvalx,offset,fldrte) # rtempt(rtelyr,rteFCSelNm,rteid,bmpvalx,offset,fldrte)
    resupdate = assyncadds(Shorelocintlyr,newfset) 
    
    print("type : {} ; recordset : {} \n - type {} - geom : {} \n\n ".format(type(frow),frow.SHAPE,type(gx),gx))
    sdfrow = geomilepostdf.query("globalid=='{}'".format(frow.globalid))
    print("type : {} ; updated geometry : {} \n - shape col : {} \n\n ".format(type(sdfrow),sdfrow.index[0],sdfrow['SHAPE']))
    sdfrow.loc[sdfrow.index[0],'SHAPE'] = [gx]  # sdfrow.apply(lambda x : gx , axis=1 ) # gx # sdfrow.apply(lambda x : gx,axis=1 ) .loc[0,'SHAPE']
    print("type : {} ; updated geometry : {} \n - shape col : {} \n\n ".format(type(sdfrow),sdfrow,sdfrow['SHAPE']))
    newfset = gac(sdfrow).to_featureset()
    print ("updated : {} \n\n".format(newfset.to_dict()))
    resupdate = assyncedits(Shorelocintlyr,newfset) 
    print("result : {}".format(resupdate))    
    
    
bmpcol = 'BMP'  # 'MP_Start'
empcol = 'EMP' # 'MP_End'
offset = 0
# delete existing data first
delayerfeatures(Shoreloclyr)
geomilepostdf = deepcopy(Shorelocsdf) 
geomilepostdf['SHAPE']=geomilepostdf.apply(lambda x : rtefeat(x,Shoreloclyr,rtelyr,offset,fldrte))


# In[ ]:


# assign geometry field and generate the arcgis features from the dataframe
sprefwgs84 = {'wkid' : 4326 , 'latestWkid' : 4326 }
sprefwebaux = {'wkid' : 102100 , 'latestWkid' : 3857 }
print (" dataframe type  : {}  ".format(type(routexdf)))
#idx= pd.Index(shorelinesdf) #(ignore_index=True)  for concat

Shorelocsdf = deepcopy(Shorelocsdf)
Shorelocgeoac = gac(Shorelocsdf)
Shorelocwgs84 =  Shorelocgeoac.set_geometry('SHAPE',sr=sprefwgs84)
#Shorelocwgs84 =  Shorelocgeoac.project(sprefwgs84)

#Shorelocsw2ysdfx = gac.from_df(routesdf,  sr=sprefwgs84, geometry_column='SHAPE')
#Shorelocgeoacx = gac(Shorelocsw2ysdfx)
Shorelocfeats = Shorelocgeoac.to_featureset()
# add to existing  layer 
print (" sdf features  : {}  ".format(len(Shorelocfeats)))
# shape file creation
Shorelocshpnm = r'HiDOT Shoreline Project Limits.shp'
Shorelocshpfile = os.path.join(inpath,Shorelocshpnm)
Shoreloclyr = Shorelocfeats.save(inpath,Shorelocshpnm, encoding="utf8")
# shape file creation
Shorelocfgbnm = r'HiDOT Shoreline Project Limits.fgb'
Shorelocfgbfile = os.path.join(inpath,Shorelocshpnm)
Shorelocfgb = Shorelocfeats.save(inpath,Shorelocfgbnm, encoding="utf8")

print(" Feature Class layer : {} created ".format(Shorelocfgb,Shorelocfgbfile))

Shorelocfeatsdf = Shorelocfeats.sdf
#progfl = qgis.content.import_data(Shorelocfeatsdf,title='Projects Closed within 2 Years',tags='projects,pss,closed',target_sr=4326)
#Shorelocfeatjson = Shorelocfeats.to_json
Shorelocfeatgeojson = Shorelocfeats.to_geojson
Shorelocintgeojsoname = "Shoreloclan.geojson"
Shorelocintgeojsonpath = os.path.join(rptpath, Shorelocintgeojsoname)
#Shorelocintfcname = "ShorelocintData.fgb"
#Shorelocintfcpath = os.path.join(rptpath, Shorelocintfcname)
gjfile = open(Shorelocintgeojsonpath, 'w')
gjfile.write(Shorelocfeatgeojson)
gjfile.close()
print(" Geojson data written to : {}  ".format(Shorelocintgeojsonpath))


# In[ ]:


print (" sdf features  : {}  ".format(len(Shorelocfeats)))
Shorelocintnm = 'HiDOT Shoreline Project Limits'

valires = Shorelocgeoac.validate(strict=True)
print(" Feature validation : {} created ".format(valires))
# feature layer creation
Shoreloclyr = Shorelocgeoac.to_featurelayer(title=Shorelocintnm, gis=qgis, tags='projects, STIP, HDOT, Shoreloc, routes', folder=None)
print(" Feature Class layer : {} created ".format(Shoreloclyr))
sdfeats = Shorelocfeats.sdf
#sdfeats['SHAPE']

# shape file creation
#Shorelocshpnm = r'Repair_Recon_Sites_20201217sdfv2.shp'
#Shorelocshpfile = os.path.join(inpath,Shorelocshpnm)
#Shoreloclyr = Shorelocgeoac.to_featureclass(Shorelocshpfile, overwrite=True, has_z=None, has_m=False)
print(" Feature Class layer : {} created ".format(Shoreloclyr))


# In[ ]:



Shoreloclayer= 'HiDOT Shoreline Project Limits'
Shorelocfeatfcol = Shorelocgeoac.to_feature_collection(name=Shoreloclayer, drawing_info=None, extent=None, global_id_field=None)
Shorelocinfcdict = dict(Shorelocfeatfcol.properties)
Shorelocinjson = json.dumps({"featureCollection": {"layers": [Shorelocinfcdict]}})
#print (" JSON feature collection  : {}  ".format(Shorelocinjson)) 
Shorelocinitem_properties = {'title': Shoreloclayer ,
                        'description':'HDOT Shoreline Repair and Maintenance projects ' + \
                         'Using HWY-L Excel data ',
                        'tags': 'projects, pss, HDOT, repair, status, maintenance ',
                        'text':Shorelocinjson,
                        'type':'Feature Collection'}
Shorelocinitem = qgis.content.add(Shorelocinitem_properties)


#Shorelocinitem
#qgis.content.add(type='featureLayer')
#Shorelocfeatfcol = arcgis.features.FeatureCollection(Shorelocfeats,name='Projects Closed within 2 Years')

#Shoreloclyr = Shorelocgeoac.to_featurelayer(title='Emergency Repair and Maintenance projects', gis=qgis, tags='projects, pss, HDOT, emergency, repair', folder=None)
#print(" layer : {}  ".format(Shoreloclyr))

#dfcsv = pd.read_csv(csvfile)
#print (" csv sdf features head : {}  ".format(dfcsv.head(1)))


#tmp_file = tempfile.mkstemp(suffix='.geojson')
#with open(Shorelocintgeojsonpath, 'w') as outfile:
#    geojson.dump(Shorelocinjson, outfile)
print (" Geojson file  : {}  output ".format(Shorelocintgeojsonpath))
#fcfile = Shorelocgeoac.to_featureclass(Shorelocintfcpath, overwrite=True, has_z=None, has_m=True)


# In[ ]:


# if layer data does not exist import fresh data into ArcGIS from excel 
try:
    #curDate = strftime("%Y%m%d%H%M%S") 
    userName= "dot_mmekuria"
    # ID or Title of the feature service to update
    if Shorelocintsrc != None:
    #print (" Content search result : {} ; ".format(fsprjstsrc))
        Shoreloclyrs = Shorelocintsrc.layers
        lyrnamelist = [ x.properties.name for i1,x in enumerate(Shoreloclyrs,1)]
        # header layer
        fs = len(Shoreloclyrs) #len(lyrtefs)
        if (fs>0):
            Shoreloclyr = lyrsearch(Shoreloclyrs, Shorelocintnm)
        else:
            print (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(Shorelocintnm,Shorelocintsrc.title,Shorelocintsrc.id,lyrnamelist))
            logger.info (" No {} Layer {} with  Title : {} ; id {} in layer list {}  ".format(Shorelocintnm,Shorelocintsrc.title,Shorelocintsrc.id,lyrnamelist))
            
    else:
        Shoreloclyr = Shorelocgeoac.to_featurelayer(title="HiDOT Emergency Maintenance and Repair Projects", gis=qgis, tags='projects, pss, HDOT, maintenance, repair', folder=None)
        print(" layer : {} created ".format(Shoreloclyr))
        Shorelocgeoacx = Shorelocgeoac.to_feature_collection(name=Shorelocintnm, drawing_info=None, extent=None, global_id_field=None)
        
    print (" Feature URL: {} ; Title : {} ; Id : {} \n Layers - {}  ".format(Shorelocintsrc.url,Shorelocintsrc.title,Shorelocintsrc.id,lyrnamelist))
    logger.info (" Feature URL: {} ; Title : {} ; Id : {} \n Layers - {} ".format(Shorelocintsrc.url,Shorelocintsrc.title,Shorelocintsrc.id,lyrnamelist))
except Exception as e:
    print(' Error : {} ;  fetching layer {}  script '.format(str(e),Shorelocintnm ))
    logger.error(' Error : {} ;  fetching layer {}  script '.format(str(e),Shorelocintnm ))


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
    resupdate = assyncedits(Shorelocintlyr,newfset) 
    print("result : {}".format(resupdate))


# In[ ]:


# update the coordinates using the newly generated coordinates 

#equsgsmap = qgis.content.search("31cfc5b138e24dee866c457948773ac4")

equsgsmap = qgis.content.get("31cfc5b138e24dee866c457948773ac4")
print("{}".format(equsgsmap) )

equsgsmap.get_data(try_json=True)


# In[ ]:


# Export ArcGIS Dataframe to .CSV

logpath = r"D:\MyFiles\HWYAP\Shorelocintes\logs"
rptpath = r"D:\MyFiles\HWYAP\Shorelocintes\reports"
# Shorelocint layers
Shorelocintnm = 'HiDOT Shoreline Project Limits'
Shorelocintentrysrc = Shorelocintsrc.layers
Shorelocintentrylyr = lyrsearch(Shorelocintentrysrc, Shorelocintnm)
Shorelocintfeatset = Shorelocintentrylyr.query(where='1=1', out_fields='*')
Shorelocintfeats = Shorelocintfeatset.features
#Shorelocintdf = Shorelocintfeats.sdf
Shorelocintrpath =r"D:\MyFiles\HWYAP\Shorelocintes\reports" # r"C:\Work Database Data\Shorelocint\Data"
Shorelocintcsvname = "ShorelocintData.csv"
Shorelocintcsvpath = os.path.join(Shorelocintrpath, Shorelocintcsvname)
Shorelocintcsv = Shorelocintdf.to_csv(Shorelocintcsvpath)
Shorelocintjsoname = "ShorelocintData.geojson"
Shorelocintjsonpath = os.path.join(Shorelocintrpath, Shorelocintjsoname)
Shorelocintdf = Shorelocintfeatset.df #Shorelocintentrylyr.query(where='1=1', out_fields='*',as_df=True)
#Shorelocintgeojson =Shorelocintfeats.to_geojson() #Shorelocintjsonpath) # 
#arcgis.features.FeatureLayerCollection.upload(Shorelocintgeojson,description="Fatal Shorelocint Dataset")
#Shorelocintgeojson = Shorelocintfeats.save(rptpath,Shorelocintjsonname)
Shorelocintpname = "ShorelocintData.shp"
Shorelocintpath = os.path.join(Shorelocintrpath, Shorelocintpname)
#Shorelocintp = Shorelocintdf.save(Shorelocintpath)
Shorelocintpfile = Shorelocintfeatset.save(Shorelocintrpath, Shorelocintpname, encoding='utf8') # eatlnclrte.save('in_memory','rtesel')
print ("GeoJson : {} ; Feats : {}".format(Shorelocintpfile,len(Shorelocintfeats)))


# In[ ]:


#Using ArcGIS GeoJSON data replace could not use the multiline data in GeoJSON? needs testing
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
view = socrata.views.lookup('vdwy-2c9e')

with open('Shoreline_Mitigation.geojson', 'rb') as my_file:
  (revision, job) = socrata.using_config('Shoreline_Mitigation_12-21-2021_5fc6', view).geojson(my_file)
  # These next 2 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  job = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
  sys.exit(0 if job.attributes['status'] == 'successful' else 1)


# In[ ]:


#Using ArcGIS GeoJSON data upsert   could not use the multiline data in GeoJSON? needs testing
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
view = socrata.views.lookup('vdwy-2c9e')

with open('Shoreline_Mitigation.geojson', 'rb') as my_file:
  (revision, job) = socrata.using_config('Shoreline_Mitigation_12-21-2021_01b9', view).geojson(my_file)
  # These next 2 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  job = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
  sys.exit(0 if job.attributes['status'] == 'successful' else 1)


# In[ ]:


# use alreadt Authenticated link and replace Socrata Using .shp file

"""
from socrata.authorization import Authorization
from socrata import Socrata
import os
import sys

auth = Authorization(
  'highways.hidot.hawaii.gov',
  os.environ['MY_SOCRATA_USERNAME'],
  os.environ['MY_SOCRATA_PASSWORD']
)
"""
inpath = r"E:\docs\shoreline"
iname = r'Shoreline_Mitigation_Limits_Shape.zip'
infilename = os.path.join(inpath,iname)
#socrata = Socrata(auth)
vwshore = 'vdwy-2c9e'
viewshoreline = socradata.views.lookup(vwshore)
vwconfig = 'Shoreline_Mitigation_Limits_Shape_12-21-2021_8938'
with open(infilename, 'rb') as my_file:
  (revision, job) = socradata.using_config(vwconfig, viewshoreline).shapefile(my_file)
  # These next 2 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  job = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
 #sys.exit(0 if job.attributes['status'] == 'successful' else 1)


# In[ ]:


# append Shoreline data using shape file from ArcGIS 
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
view = socrata.views.lookup('vdwy-2c9e')

with open('Shoreline_Mitigation_Limits_Shape.zip', 'rb') as my_file:
  (revision, job) = socrata.using_config('Shoreline_Mitigation_Limits_Shape_12-21-2021_78df', view).shapefile(my_file)
  # These next 2 lines are optional - once the job is started from the previous line, the
  # script can exit; these next lines just block until the job completes
  job = job.wait_for_finish(progress = lambda job: print('Job progress:', job.attributes['status']))
  sys.exit(0 if job.attributes['status'] == 'successful' else 1)

