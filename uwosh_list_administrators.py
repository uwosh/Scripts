# Script to place in Zope root that shows who is in the Administrators
# group in all the contained Plone sites.

uniqueDict = {}

for itemTuple in context.items():
 (item, itemType) = itemTuple
 if str(itemType).startswith('<PloneSite at '):
   site = getattr(context, item)
   print "Plone site '%s':" % item
   adminMembers = site.portal_groups.getGroupById('Administrators').getAllGroupMembers()
   print "    ", [m.getProperty('email', None) for m in adminMembers]
   for m in adminMembers:
       email = m.getProperty('email', None)
       if email:
           uniqueDict[email] = 1
 elif str(itemType).startswith('<Folder at '):
   folder = getattr(context, item)
   for folderItemTuple in folder.items():
     (folderItem, folderItemType) = folderItemTuple
     if str(folderItemType).startswith('<PloneSite at '):
       site = getattr(folder, folderItem)
       print "Plone site '%s':" % item
       adminMembers = site.portal_groups.getGroupById('Administrators').getAllGroupMembers()
       print "    ", [m.getProperty('email', None) for m in adminMembers]
       for m in adminMembers:
           email = m.getProperty('email', None)
           if email:
               uniqueDict[email] = 1
    
print "uniqueDict: %s" % uniqueDict.keys()

return printed
