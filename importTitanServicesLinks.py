
# This external method pulls in a list of titanServicesLinks from the given url
# the format of the list should be: "%id,,,,,,,%title,,,,,,,%url_expr" with one entry per line
# it then iterates through all the plone sites in the container it is run on (should be the root zope instance)
# and using the list of links, it clears and rebuilds the portal_actions.titan_services category for each site

import urllib2
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.ActionInformation import Action

URL = 'https://site/exportTitanServicesLinks'
ALLOWED_HOSTS = ['127.0.0.1']

def importTitanServicesLinks(self):
    if self.REQUEST.REMOTE_ADDR not in ALLOWED_HOSTS and 'Manager' not in self.REQUEST.AUTHENTICATED_USER.getRoles():
        return 'You do not have sufficent permissions to access this object\n'

    resultString = ''

    stream = urllib2.urlopen(URL)
    string = stream.read()
    listOfActions = map(lambda x: tuple(x.split(',,,,,,,')), string.splitlines())

    if len(listOfActions) == 0 or len(listOfActions[0]) != 3 or len(listOfActions[-1]) != 3:
        resultString += 'No importable titan_services links from: %s\n\n' % URL

    else:
        resultString += 'Importing from: %s\n\n' % URL

        ploneSites = [obj for (id, obj) in self.objectItems() if (hasattr(obj, 'Type') and obj.Type() == 'Plone Site') and 
                                                                 (not hasattr(obj, 'titanservices_master_site') or not obj.titanservices_master_site)]

        if len(ploneSites) == 0:
            resultString += 'No eligible plone sites were found in this container\n'

        for ploneSite in ploneSites:
            resultString += '%s:\n' % ploneSite.id
            resultString += ('-' * 20) + '\n'

            portal_actions = getToolByName(ploneSite, 'portal_actions', default=None)          
  
            if hasattr(portal_actions, 'titan_services'):
                titan_services = portal_actions['titan_services']

                titan_services.manage_delObjects(titan_services.objectIds())
                
                for (id, title, urlExpr) in listOfActions:
                    action = Action(id=id, title=title, url_expr=urlExpr, i18n_domain='plone', permissions=('View',))
                    titan_services._setObject(id, action)
                    titan_services[id].indexObject()
                    
                    resultString += 'Created: %s, %s, %s\n' % (id, title, urlExpr)

            else:
                resultString += 'No titan_services action category exists\n'

            resultString += '\n'

    return resultString
