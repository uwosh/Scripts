# Script to place in Zope root that shows which non-standard products
# are installed in all the contained Plone sites.

from Products.CMFCore.utils import getToolByName

productsToSkip = [ 'ATContentTypes', 'ATReferenceBrowserWidget', 'Archetypes', 'CMFActionIcons', 'CMFCalendar', 'CMFFormController', 'CMFPlacefulWorkflow', 'GroupUserFolder', 'MimetypesRegistry', 'PasswordResetTool', 'PlonePAS', 'PortalTransforms', 'ResourceRegistries', 'kupu', 'CMFSquidTool', 'Products.CMFSquidTool', 'CacheSetup']

for itemTuple in context.items():
 (item, itemType) = itemTuple
 if str(itemType).startswith('<PloneSite at '):
   site = getattr(context, item)
   pq = getToolByName(site, "portal_quickinstaller")
   print "Plone site '%s'" % item
   for product in pq.listInstalledProducts():
     pid = product['id']
     if pid not in productsToSkip:
       print "    Has installed product '%s'" % pid
 if str(itemType).startswith('<Folder at '):
   folder = getattr(context, item)
   for folderItemTuple in folder.items():
     (folderItem, folderItemType) = folderItemTuple
     if str(folderItemType).startswith('<PloneSite at '):
       site = getattr(folder, folderItem)
       pq = getToolByName(site, "portal_quickinstaller")
       print "Plone site '%s'" % folderItem
       for product in pq.listInstalledProducts():
         pid = product['id']
         if pid not in productsToSkip:
           print "    Has installed product '%s'" % pid

return printed
