# Available parameters:
#  fields  = HTTP request form fields as key value pairs
#  request = The current HTTP request. 
#            Access fields by request.form["myfieldname"]
#  ploneformgen = PloneFormGen object
# 
# Return value is not processed

#import logging

lines = fields['new-account-records']
pr = context.portal_registration
pg = context.portal_groups
for line in lines:
  tokens = line.split(',')
  if len(tokens) == 3:
    fullname,email,groupId = tokens
    id = (email.split('@'))[0]
  elif len(tokens) == 4:
    fullname,email,groupId,id = tokens
  else:
    raise ValueError, 'Each line should contain: fullname,email,groupId[,id]. The offending line is: ''%s''' % line
  email = email.strip()
  properties = { 'username' : id, 'fullname' : fullname, 'email' : email }
  password=pr.generatePassword()
  pr.addMember(id,password,properties=properties)
  context.plone_log("create-user-accounts","Created username %s, full name %s, email %s" % (id, fullname, email))
  pr.registeredNotify(id)
  #pr.mailPassword(id, request)
  context.plone_log("create-user-accounts","Sent email notification to email %s" % (email))
  if groupId:
    group = pg.getGroupById(groupId)
    group.addMember(id)
    context.plone_log("create-user-accounts","Added username %s to group %s" % (id, groupId))
