plone_site_search_depth = 3 # depth it will search, from the zope root, for plone sites

if not context.REQUEST.REMOTE_ADDR.startswith('141.233.'):
  return

def find_honking_files(plone):
    """
    Steps:
    1. look at Plone content types
    2. look in portal skins
    """

    pc = plone.portal_catalog
    brains = pc.searchResults({'portal_type' : ('Image', 'File', 'News Item') })
    brains = list(brains)

    #brains.filter(lambda x : "MB" not in x.getObjSize)
    #brains.sort(lambda x, y : x.getObjSize > y.getObjSize)

    for b in brains:
        size = b.getObjSize
        if "MB" in size or "GB" in size:
            url = b.getURL()
            print "%s <a href='%s'>%s</a><br>" % (size, url, url)

    ps = plone.portal_skins
    
    def find_big_ones(current):
        found = []
        
        for x in current.objectIds():
            obj = current[x]
        
            if hasattr(obj, 'getContentType') and str(obj.getContentType()).strip().startswith('image'):
                size = (float(obj.get_size())/1024.0)/1024.0
                if size > 1.0:
                    print "%s MB : %s<br/>" % (str(size)[:4], obj.id())
        
            if hasattr(obj, 'objectIds'):
                print find_big_ones(obj)
                
        return printed

    print find_big_ones(ps)

    return printed

def get_plone_sites():
    
    def find_it(current_context, depth):
        if depth == 0:
            return []
        else:
            sites = []
            for obj in current_context.objectIds():
                site = current_context[obj]
                if hasattr(site, 'portal_type') and site.portal_type == 'Plone Site':
                    sites.append(site)
                elif hasattr(site, 'objectIds'):
                    sites.extend(find_it(site, depth - 1))
                    
            return sites
    
    return find_it(context, plone_site_search_depth)
            
sites = get_plone_sites()

for site in sites:
    print "Plone Site: %s<br/>" % site.title
    print find_honking_files(site)

return printed
