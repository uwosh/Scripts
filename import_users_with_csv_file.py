# Create new members with properties supplied from a CSV file.
# The script expects a File object with id `users.csv` in the same folder
# it resides.
#
# The format of the CSV needs to be:
#
# group \t user
#
# created 2006-11-03 by Tom Lazar <tom@tomster.org>, http://tomster.org/
# under a BSD-style licence (i.e. use as you wish but don't sue me)

from Products.CMFCore.utils import getToolByName

def get_group_or_create(name, groups):
    pg = context.portal_groups
    if pg.addGroup(id=name):
        groups.append(name)
        return pg.getGroupById(name)
    else:
        return pg.getGroupById(name)

def fill_groups(file):
    users = context[file].data.split('***')
    regtool = getToolByName(context, 'portal_registration')
    groups_added = []
    index = 1
    imported_count = 0

    for user in users:
        tokens = user.split(':::')
        if len(tokens) == 2:
            group = tokens[0].strip()
            user = tokens[1].strip().lower()

            try:
                group = get_group_or_create(group, groups_added)
                group.addMember(user)
                print "Successfully added %s to group %s" % (user, group)
                imported_count += 1
            except ValueError, e:
                print "Couldn't add %s to group %s : %s" % (user, group, e)
        else:
            print "Could not parse line %d because it had the following contents: '%s'" % (index, user)
        index += 1

    print "Imported %d users (from %d lines of CSV)" % (imported_count, index)
    print "\nAdded these groups.."

    for group in groups_added:
        print group

    return printed

#set to 'users.csv' when you want to run
#file = None

if file is None:
    print "You must specify file to use..."
    return printed
else:
    return fill_groups(file)

