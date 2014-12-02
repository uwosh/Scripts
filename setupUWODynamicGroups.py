
from Products.PluggableAuthService.plugins.DynamicGroupsPlugin import addDynamicGroupsPlugin
from Products.CMFCore.utils import getToolByName

uwoGroups = [('Staff', "python: 'staff' in (principal.getProperty('eduPersonAffiliation') or [])"),
             ('Students', "python: 'student' in (principal.getProperty('eduPersonAffiliation') or [])"),
             ('Faculty', "python: 'faculty' in (principal.getProperty('eduPersonAffiliation') or [])")]

def isPloneSite(obj):
    return hasattr(obj, 'meta_type') and obj.meta_type == 'Plone Site'

def setupUWODynamicGroups(self):
    if 'Manager' not in self.REQUEST.AUTHENTICATED_USER.getRoles():
        return 'if you were a manager then you could run this script'

    if isPloneSite(self):
        ploneSites = [self]
    elif hasattr(self, 'objectItems'):
        ploneSites = [obj for (id, obj) in self.objectItems() if isPloneSite(obj)]
    else:
        ploneSites = []

    if len(ploneSites) == 0:
        return 'no valid plone sites were found; you have accomplished nothing'

    results = []
    for ploneSite in ploneSites:
        results.append(ploneSite.id)
        results.append('-' * 40)
        
        portal_groups = getToolByName(ploneSite, 'portal_groups')
        acl_users = getToolByName(ploneSite, 'acl_users')

        if hasattr(acl_users, 'dynamic_groups_provider'):
            results.append('dynamic_groups_provider already exists')
        else:
            addDynamicGroupsPlugin(acl_users, 'dynamic_groups_provider', 'Dynamic Groups Provider')
            results.append('created dynamic_groups_provider')

        dynamicGroupsProvider = acl_users.dynamic_groups_provider
        
        for (name, predicate) in uwoGroups:
            if hasattr(dynamicGroupsProvider, name):
                results.append('dynamic group: %s already exists' % name)
            elif portal_groups.getGroupById(name) is not None:
                results.append('a static group named: %s already exists' % name)
            else:
                dynamicGroupsProvider.addGroup(name, predicate, title=name)
                results.append('created dynamic group: %s' % name)
        
        dynamicGroupsProvider.manage_activateInterfaces(['IGroupsPlugin', 'IGroupEnumerationPlugin'])
        results.append('dynamic_groups_provider activated')

        if hasattr(acl_users, 'ldap_authentication'):
            ldap_acl_users = acl_users.ldap_authentication.acl_users
            
            if 'eduPersonAffiliation' in ldap_acl_users.getSchemaConfig():
                results.append('eduPersonAffiliation ldap schema item already exists')
            else:
                ldap_acl_users.manage_addLDAPSchemaItem('eduPersonAffiliation', friendly_name='eduPersonAffiliation',
                                                        multivalued=True, public_name='eduPersonAffiliation')
                results.append('added eduPersonAffiliation ldap schema item')
        else:
            results.append('ldap does not seem to be set-up on this plone site; no ldap schema item was added')

        results.append('')
        
    return '\n'.join(results)
