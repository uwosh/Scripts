## Script (Python) "exportTitanServicesLinks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFCore.utils import getToolByName

if not context.REQUEST.REMOTE_ADDR.startswith('141.233.'):
  return

portal_actions = getToolByName(context, 'portal_actions', None)

if hasattr(portal_actions, 'titan_services'):
  titan_services = portal_actions['titan_services']

  for (id, obj) in titan_services.objectItems():
    title = obj.title
    urlExpr = obj.url_expr
    print '%s,,,,,,,%s,,,,,,,%s' % (id, title, urlExpr)

  return printed

else:
  return ' '
