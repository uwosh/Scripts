from Products.CMFPlone.Portal import PloneSite
from OFS.Folder import Folder

OLD_SMTP = 'smtp.uwosh.edu'
NEW_SMTP = 'out.mail.uwosh.edu'
USE_HTML = True


def do_site(site, item, change, out):
    mh = site.MailHost
    smtp = getattr(mh, 'smtp_host', None)
    if USE_HTML:
        if smtp != NEW_SMTP:
            out.append("<b>Plone site '%s' has <a href='%s'>smtp %s</a></b>" % (item, mh.absolute_url()+'/manage_main', smtp))
        else:
            out.append("Plone site '%s' has smtp %s" % (item, smtp))
    else:
        out.append("Plone site '%s' has smtp %s" % (item, smtp))
    if change == '1' and smtp and smtp != NEW_SMTP:
        mh.smtp_host = NEW_SMTP
        smtp_new = getattr(mh, 'smtp_host', None)
        out.append("   changed to smtp %s" % (smtp_new))
    return out


def change_smtp_servers(self, change=0):
    """ Changes the SMTP server of all the contained Plone sites. """
    out = []
    if USE_HTML:
        out.append('<html><body>')
    if change == 0:
        out.append('To change the SMTP server to %s, specify ?change=1 in the URL' % NEW_SMTP)
    for itemTuple in self.items():
        (item, itemType) = itemTuple
        if isinstance(itemType, PloneSite):
            site = getattr(self, item)
            out = do_site(site, item, change, out)
        elif isinstance(itemType, Folder):
            folder = getattr(self, item)
            for folderItemTuple in folder.items():
                (folderItem, folderItemType) = folderItemTuple
                if isinstance(folderItemType, PloneSite):
                    site = getattr(folder, folderItem)
                    out = do_site(site, folderItem, change, out)
    if USE_HTML:
        out.append('</body></html>')
    if USE_HTML:
        return "<br>".join(out)
    else:
        return "\n".join(out)
