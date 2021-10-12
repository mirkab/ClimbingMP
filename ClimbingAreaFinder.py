import arcpy
from arcpy.sa import *


#Get Layers
elevationfc = arcpy.GetParameterAsText(0)
stateshapefc = arcpy.GetParameterAsText(1)
geologyshapefc = arcpy.GetParameterAsText(2)
landshapefc = arcpy.GetParameterAsText(3)
outputfc = arcpy.GetParameterAsText(4)


tempData = arcpy.CreateScratchName(workspace=arcpy.env.scratchGDB)


try:
    if arcpy.CheckOutExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        arcpy.AddMessage("Checked out Spatial Extension")
except LicenseError:
    print "Spatial Analyst license is unavailable"
except:
    print arcpy.GetMessages(2)

arcpy.AddMessage("Finding Primary Rock Type...")
#Polygon to Raster Geology 1
gFeatures = geologyshapefc
gvalField = "ROCKTYPE1"
gassignmentType = "MAXIMUM_AREA"
Geology1 = arcpy.PolygonToRaster_conversion(gFeatures, gvalField, tempData, gassignmentType, "",  0.00083333333)

#Geology 1 Mask
Geology1Mask = ExtractByMask(Geology1, stateshapefc)

#Raster Reclass Geology 1
g1inRaster = Geology1Mask
g1reclassField = "ROCKTYPE1"
g1remap = RemapValue([["basalt", 2], ["coal", 0], ["fine-grainedmixedclastic", 0],["sandstone", 2], ["alluvium", 0], ["medium-grainedmixedclastic", 0], ["shale", 0], ["clayormud", 0], ["plutonicrock(phaneritic)", 2], ["clastic", 0], ["landslide", 0], ["limestone", 2],["andesite", 2], ["coarse-grainedmixedclastic", 0], ["maficmetavocanicrock", 0], ["tuff", 2], ["conconsolidateddeposite", 0], ["pyroclastic", 0], ["volcanicrock(aphanitic)", 0], ["indeterminate", 0], ["felsicvolcanicrock", 0], ["felsicmetavolcanicrock", 0], ["metasedimentaryrock",0], ["metamorphicrock", 0], ["till", 0], ["sedimentaryrock", 2], ["eolian", -1], ["water", -1], ["rhyolite", 2], ["lakeormarinedeposit(non-glacial)", -1], ["mudstone", 0], ["carbonate", 2], ["playa", 0], ["evaporite", 0], ["conglomerate", 0], ["lavaflow", 0], ["quartzmonzonite", 0], ["granodiorite", 2], ["shale", 0], ["solostone(dolomite)", 1]])

Geolog1Reclass = Reclassify(g1inRaster, g1reclassField, g1remap, "NODATA")


arcpy.AddMessage("Finding Secondary Rock Type...")
#Polygon to Raster Geology 2
g2Features = geologyshapefc
g2valField = "ROCKTYPE2"
g2assignmentType = "MAXIMUM_AREA"

Geology2 = arcpy.PolygonToRaster_conversion(g2Features, g2valField, tempData, g2assignmentType, "", 0.00083333333)
Geology2Mask = ExtractByMask(Geology2, stateshapefc)

g2inRaster = Geology2Mask
g2reclassField = "ROCKTYPE2"
g2remap = RemapValue([["basalt", 1], ["coal", 0], ["fine-grainedmixedclastic", 0],["sandstone", 1], ["alluvium", 0], ["medium-grainedmixedclastic", 0], ["shale", 0], ["clayormud", 0], ["plutonicrock(phaneritic)", 1], ["clastic", 0], ["landslide", 0], ["limestone", 1],["andesite", 1], ["coarse-grainedmixedclastic", 0], ["maficmetavocanicrock", 0], ["tuff", 1], ["conconsolidateddeposite", 0], ["pyroclastic", 0], ["volcanicrock(aphanitic)", 0], ["indeterminate", 0], ["felsicvolcanicrock", 0], ["felsicmetavolcanicrock", 0], ["metasedimentaryrock",0], ["metamorphicrock", 0], ["till", 0], ["sedimentaryrock", 1], ["eolian", 0], ["water", 0], ["rhyolite", 1], ["lakeormarinedeposit(non-glacial)", 0], ["mudstone", 0], ["carbonate", 1], ["playa", 0], ["evaporite", 0], ["conglomerate", 0], ["lavaflow", 0], ["quartzmonzonite", 0], ["granodiorite", 1], ["shale", 0], ["solostone(dolomite)", 1]])
Geolog2Reclass = Reclassify(g2inRaster, g2reclassField, g2remap, "NODATA")


arcpy.AddMessage("Finding Public Lands...")
#Polygon to Raster Public Lands
LFeatures = landshapefc
LassignmentType = "MAXIMUM_AREA"
PublicLands = arcpy.PolygonToRaster_conversion(LFeatures, "Access", tempData, LassignmentType)
PublicLandsMask = ExtractByMask(PublicLands, stateshapefc)
LandReclass = Reclassify (PublicLandsMask, "Access", RemapValue([["UK", 0], ["XA", 0], ["RA", 0], ["OA", 1]]))

ElevationMask = ExtractByMask(elevationfc, stateshapefc)

arcpy.AddMessage("Finding Crags...")
#Find Slope of areas
outSlope = Slope(ElevationMask, "DEGREE")

#Find optimal Slope Variables
SlopeReclass = Reclassify (outSlope, "Value", RemapRange([[0,10,0], [10, 70, 1]]))

#Find Public Lands

arcpy.AddMessage("Adding it all up...")
#Add Types together (+1)
GeologyTotal = Geolog1Reclass + Geolog2Reclass + 1

#Raster Calculator
FinalRaster = GeologyTotal * LandReclass * SlopeReclass
FinalRaster.save(outputfc)
arcpy.CheckInExtension("Spatial")

arcpy.AddMessage("Potential Climbing Areas Complete")
