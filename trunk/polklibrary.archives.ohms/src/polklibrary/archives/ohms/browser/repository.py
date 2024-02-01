from plone import api
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
from zope.security import checkPermission
import random, time, transaction

class RepositoryView(BrowserView):

    template = ViewPageTemplateFile("templates/repository.pt")
    
    def __call__(self):
        return self.template()

        
    def get_subject_headings(self):
        results = []
        subjects = self.context.subject_headings.split('\n')
        for subject in subjects:
            csubject = subject.replace('\r','').strip()
            results.append(csubject)
        return results
        
    def hasPermission(self):
        return checkPermission('cmf.ModifyPortalContent', self.context) or checkPermission('cmf.AddPortalContent', self.context) or checkPermission('cmf.ManagePortal ', self.context)
        
        
    
    def get_files_brains(self):
        results = []
        brains = api.content.find(context=self.context,
                                  portal_type='polklibrary.archives.ohms.models.ohmsfile', 
                                  sort_on="sortable_title")
                                  
        for brain in brains:
            subjects = brain.subject_headings
            obj = brain.getObject()
            
            last_name_initial = 'a'
            if ',' in brain.Title:
                last_name_initial = brain.Title[0].lower()
            else:
                names = brain.Title.split(' ')
                last_name_initial = names.pop()[0].lower()
            
            results.append({
                'Title': brain.Title,
                'Description': brain.Description,
                'Subjects': subjects,
                'getURL': brain.getURL(),
                'has_image': obj.image != None,
                'xmlPath': brain.getPath().replace('/archives/','').replace('/arch/','') + '?file=1',
                'last_name_initial': last_name_initial,
            })
                                  
        return results
        

        
        
    @property
    def portal(self):
        return api.portal.get()
        
        