from plone import api
from plone.namedfile.utils import stream_data,set_headers
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import random, time, transaction


def download_blob(context, request, file):
    if file == None:
        raise NotFound(context, '', request)

    filename = getattr(file, 'filename', context.id + "_download")
    set_headers(file, request.response)

    cd = 'inline; filename=%s' % filename
    request.response.setHeader("Content-Disposition", cd)

    return stream_data(file)



class OHMSFileView(BrowserView):

    template = ViewPageTemplateFile("templates/ohmsfile.pt")
    viewer_path = ""
    
    def __call__(self):
        if self.request.form.get('file', ''):
            return download_blob(self.context, self.request, self.context.file)
            
            
        self.viewer_path = 'http://polk.uwosh.edu/ohms/viewer.php?cachefile=' + self.context.absolute_url_path().replace('/archives/','').replace('/arch/','') + '?file=1'
        return self.template()

        
    @property
    def portal(self):
        return api.portal.get()
        
        