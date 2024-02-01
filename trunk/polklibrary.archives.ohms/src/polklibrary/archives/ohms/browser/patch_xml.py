from plone import api
from plone.namedfile.utils import stream_data,set_headers
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
from plone.namedfile.file import NamedBlobFile
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
import random, time, transaction


PATCH_XML_MAP = {
'Dick Gregory 1972':'1_9g5vqcuo',
'uwocs_Abigail_Martin_04252017_uc':'1_mqck0qhj',
'uwocs_Alan_Christian_11292016_uc':'1_rpmz5ivm',
'uwocs_Alison_Fett_05042017_uc':'1_yt2f23oh',
'uwocs_Alison_Fett_05042017_uc.mp3':'1_daewycc7',
'uwocs_Amanda_Betts_04222016_uc':'1_kech9zvc',
'uwocs_Amanda_Sunila_04242016_uc':'1_ny1d244p',
'uwocs_Amy_Anaya_04302016_uc':'1_zlvsojra',
'uwocs_Andrew_Delponte_04232016_uc':'1_kwjx84tf',
'uwocs_Angel_Liddle_04232018_uc':'1_eqxoqp1d',
'uwocs_Ann_KunkleJones_04262016_uc':'1_lm60bcli',
'uwocs_Bill_Bartlett_04232018_uc':'1_hy8s2k7j',
'uwocs_Brett_Goodman_11302016_uc':'1_j7hesstb',
'uwocs_Brian_Schaefer_05012017_uc':'1_jxii3bgw',
'uwocs_Caitlin_Kling_11202016_uc':'1_3itk4op9',
'uwocs_Chantel_Mitchell_04132018_uc':'1_hanhtwws',
'uwocs_Christopher_Welch_04272017_uc':'1_w4vfgu8s',
'uwocs_Cindy_Fruhwirth_04192016_uc':'1_i4nva0s6',
'uwocs_Connie_Weiss_05062016_uc':'1_r5vo179e',
'uwocs_Corinne_Kiedrowski_12022016_uc':'1_u0uacdwd',
'uwocs_Courtney_Rinka_04302016_uc':'1_85h78zay',
'uwocs_Craig_Cady_04262018_uc':'1_th10pnp8',
'uwocs_Cynthia_Huebschen_04212016_uc':'1_ecx2y637',
'uwocs_Cynthia_Thorpe_04222016_uc':'1_njvbmsel',
'uwocs_Dan_Vandenberg_05022016_uc':'1_ddoh1n21',
'uwocs_David_Miles_11292016_uc':'1_r1ct9ah9',
'uwocs_David_VanLieshout_04262017_uc':'1_ibfe8gyh',
'uwocs_David_Weidemann_05022016_uc':'1_5xo1r0m3',
'uwocs_Dean_Moede_04272017_uc':'1_4xykfxdo',
'uwocs_Debra_Daubert_04292016_uc':'1_hey5oeez',
'uwocs_Denise_CornerSciano_04242017_uc':'1_95rwh0qi',
'uwocs_Denise_CornerSciano_04242017_uc':'1_9edhk1rw',
'uwocs_Denise_Roseland_04252018_uc':'1_aoqdvddv',
'uwocs_Diane_Wetherbee_04182018_uc':'1_h2hhx81m',
'uwocs_Donald_Becker_04202018_uc':'1_k9pfvb3e',
'uwocs_Donald_Wolter_04262018_uc':'1_4z5xayyk',
'uwocs_Dot_Ruta_04042018_uc':'1_9quo0q0j',
'uwocs_Eamon_Mckenna_04262016_uc':'1_smgno1nu',
'uwocs_Eileen_Housfeld_uc':'1_5dasr0r3',
'uwocs_Ellen_Becker_12012016_uc':'1_gygpvufr',
'uwocs_Ellen_Eisch_12012016_uc':'1_4r1fehnn',
'uwocs_Erica_Spicer_04262016_uc':'1_4na2fe3u',
'uwocs_Erik_Ernst_04252018_uc':'1_ea1yczyf',
'uwocs_Eugene_Winkler_04302018_uc':'1_fwhu75c3',
'uwocs_Gerald_Carpenter_12062016_uc':'1_eu3zkbpv',
'uwocs_Gerry_Gonyo_05042018_uc':'1_it6fk2k0',
'uwocs_Gretchen_Herrmann_12062016_uc':'1_m8d6jdkx',
'uwocs_Heather_Cambray_11292016_uc':'1_o91wetta',
'uwocs_Jake_Timm_04272017_uc':'1_ubev4wy8',
'uwocs_James_Fischer_11232016_uc':'1_bjhrfey2',
'uwocs_James_Trantow_05022016_uc':'1_kb34cqh0',
'uwocs_JamesM_Chitwood_05022016_uc':'1_fke7xo38',
'uwocs_Jamie_Cowling_04162017_uc':'1_xej6ibm0',
'uwocs_Jane_Wypiszynski_04262016_uc':'1_ghxzhc13',
'uwocs_Janet_Alley_04232017.mp3':'1_j565rog8',
'uwocs_Jason_Hubbard_04222016_uc':'1_x4clq9ut',
'uwocs_Jay_Jones_04192017_uc':'1_a4cgtr5z',
'uwocs_JeanL_Kobin_04212016_uc':'1_3wo0tpsy',
'uwocs_Jeffery_Babiarz_04272016_uc':'1_7mmp7ksk',
'uwocs_Jennifer_Mihalick_04282016_uc':'1_laotjpy4',
'uwocs_Jessica_King_04242018_uc':'1_qkumtffk',
'uwocs_Jim_Rath_04262017_uc':'1_rnrr7vnp',
'uwocs_Jim_Simmons_05032016_uc':'1_5bifb1s0',
'uwocs_John_Marx_04262018_uc':'1_kax60syq',
'uwocs_John_Strous_05032017_uc':'1_lvqycmji',
'uwocs_Joni_Ledzian_04292017_uc.mp3':'1_zrcdjb7x',
'uwocs_Joseph_Aronson_04272017_uc':'1_4hgntmtz',
'uwocs_Joseph_Peters_11302016':'1_wz8q8rqn',
'uwocs_JudithA_BuettnerShwonek_04212016_uc':'1_elo81zsy',
'uwocs_Juliana_Flavin_11302016_uc':'1_8ffi02t6',
'uwocs_Julie_Vandehey_04192018_uc':'1_pshklaxn',
'uwocs_Karen_Miller_03302018_uc':'1_3cgd1m58',
'uwocs_Karen_Reiter_04182018_uc':'1_3tzc3vqc',
'uwocs_Karen_Sykes_04242018_uc':'1_avtcmgqr',
'uwocs_Kelsey_Hartman_11272016_uc':'1_k5ddytnk',
"uwocs_Kevin_O'Brien_05022017_uc":'1_q7xnzg0w',
'uwocs_Lin_Schrottky_05012017_uc':'1_40i6wrzs',
'uwocs_Linda_Rondeau_04262018_uc':'1_nmx2blml',
'uwocs_Linda_Weyers_04232018_uc':'1_3r9uupv0',
'uwocs_Linda_Weyers_04232018_uc':'1_rrg6bn5i',
'uwocs_Liz_Sangbusch_04202018_uc':'1_hvt3fp9v',
'uwocs_Louis_Marohn_04192018_uc':'1_umm39wpl',
'uwocs_Luke_Venne_11232016_uc':'1_iilttkcf',
'uwocs_Lynn_Allar_11302016_uc':'1_drkurkes',
'uwocs_Mallory_Janquart_12062016_uc':'1_k37bfxkb',
'uwocs_Marc_Nylen_04202018_uc':'1_aube8o7n',
'uwocs_Mariah_Haberman_04272017_uc':'1_q56j4njb',
'uwocs_Mark_Faby_04282017_uc':'1_ovay163f',
'uwocs_MaryJo_Rasmussen_11252016_uc':'1_o6jpg9vl',
'uwocs_Matthew_Eldred_05022017_uc':'1_exagmh0r',
'uwocs_Melissa_Hunt_04202017_uc':'1_9mslwxy5',
'uwocs_Michael_Brady_04252018_uc.mp3':'1_1huj3lt5',
'uwocs_Michael_Flanagan_12012016':'1_5l7go68r',
'uwocs_Michael_Lizotte_04282016_uc':'1_y4u4wxhz',
'uwocs_Michael_Utek_04252018_uc':'1_yrprhdct',
'uwocs_Michelle_Kampa_05032017_uc':'1_ysl2h3ze',
'uwocs_Michelle_Muetzel_12012016':'1_x09vlo3z',
'uwocs_Mike_Elter_04192018_uc':'1_24l4ep63',
'uwocs_Mohsen_Rad_11302016':'1_f2ltkm0a',
'uwocs_Myles_Teteak_uc':'1_sz591cj4',
'uwocs_Norbert_Hill_05052016_uc':'1_weshnk5i',
'uwocs_Oscar_Mireles_04242017_uc':'1_x7j377r1',
'uwocs_Paul_Westrick_04262017_uc':'1_6hnfh5b0',
'uwocs_Paulette_Feld_04292016_uc':'1_zuw2qusc',
'uwocs_Pete_Greeninger_11272016_uc':'1_v8q0j04y',
'uwocs_Philip_Aggen_11222016_uc':'1_hrr0s66m',
'uwocs_Randy_Hedge_11302016_uc':'1_5gws4j9u',
'uwocs_Rebecca_Hart_11302016_uc':'1_p4btwe9j',
'uwocs_Rebecca_Kollmann_04291016_uc':'1_67m4kwkv',
'uwocs_Rob_Richardson_04242018_uc.mp3':'1_iditwy89',
'uwocs_Rob_Rudolph_04262018_uc.mp3':'1_ugkoo0w9',
'uwocs_RobertJ_Snyder_04282016_uc':'1_a9997ig6',
'uwocs_Ron_Hermes_12022016_uc':'1_5p5i9e7f',
'uwocs_Scott_Barr_05022017_uc':'1_cmk3s333',
'uwocs_Sharon_Radley_04222016_uc':'1_7fm5kpv1',
'uwocs_Sharon_Rhode_04262018_uc':'1_8jznqx7n',
'uwocs_Steven_Karges_12022016_uc':'1_0023m5sq',
'uwocs_Susan_Stansbury_04242018_uc.mp3':'1_qwrhz5l3',
'uwocs_Tabitha_Zehms_04262018_uc.mp3':'1_miy0dzgk',
'uwocs_Tamara_Dever_04192018_uc':'1_xf89521z',
'uwocs_Ted_Conrardy_04202018_uc.mp3':'1_6ttq8cst',
'uwocs_Terry_Backmann_04242018_uc.mp3':'1_p2xwqy0r',
'uwocs_Terry_Schneider_11272016_uc':'1_a9q34b9k',
'uwocs_Tiffany_Taticek_04242018_uc':'1_znnxs4i4',
'uwocs_Tim_Duex_05022017_uc':'1_e3du2w9r',
'uwocs_Timber_Smith_uc':'1_580iq2dy',
'uwocs_Timothy_VanAsten_04292016_uc':'1_hgmjidid',
'uwocs_Tom_Fojtik_05022017_uc':'1_ekiv8xpm',
'uwocs_Tonya_Peotter_11212016_uc':'1_26s9mwk9',
'uwocs_Trevor_Uitenbroek_04302018_uc.mp3':'1_o95xdw52',
'uwocs_Victor_Alatorre_04272018_uc':'1_pfpt8vo5',
'uwocs_Virginia_Kruse_04282016_uc':'1_x8dlm7av',
'uwocs_Walt_Busalacchi_04192016_uc':'1_2e04nfur',
'uwocs_William_Kitz_05042016_uc.mp3':'1_e1pl8lly',
'uwocs_William_Urbrock_04232018_uc':'1_8xnmu162',

}


def download_blob(context, request, file):
    if file == None:
        raise NotFound(context, '', request)

    filename = getattr(file, 'filename', context.id + "_download")
    set_headers(file, request.response)

    cd = 'inline; filename=%s' % filename
    request.response.setHeader("Content-Disposition", cd)

    return stream_data(file)



class PatchXMLView(BrowserView):

    
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        
        output = ""
        _all = self.request.form.get('all','')
        id = self.request.form.get('id','')
        view_id = self.request.form.get('view_id','')
    
        if id:
            output = "Patch: Single \n" 
            brains = api.content.find(context=self.context,
                                      id=id,
                                      portal_type='polklibrary.archives.ohms.models.ohmsfile', 
                                      sort_on="sortable_title")
        elif _all:
            output = "Patch: All \n" 
            brains = api.content.find(context=self.context,
                                      portal_type='polklibrary.archives.ohms.models.ohmsfile', 
                                      sort_on="sortable_title")
        elif view_id:
            brains = api.content.find(context=self.context,
                                      id=view_id,
                                      portal_type='polklibrary.archives.ohms.models.ohmsfile', 
                                      sort_on="sortable_title")
            obj = brains[0].getObject()
            s = stream_data(obj.file)
            self.request.response.setHeader("Content-type", "text/xml")
            return s.read()
        else:
            output = "Patch: Nothing \n"
            brains = []
                     
        output += "Total: " + str(len(brains)) + "\n\n"
        for brain in brains:
            obj = brain.getObject()
            s = stream_data(obj.file)
            raw_xml = s.read()
            
            # OLD ID TO NEW ID
            old_media_url = self.find_between(raw_xml, '<media_url>', '</media_url>')
            url_parts = old_media_url.split('/')
            old_id = url_parts.pop()
            old_path = url_parts.pop()
            new_id = PATCH_XML_MAP.get(old_path,'PATHXMLERROR')
            raw_xml = raw_xml.replace(old_id,new_id)
            
            #WID
            old_wid = self.find_between(raw_xml, '&amp;wid=', '&quot; width=')
            purge_wid_target = '&amp;&amp;wid=' + old_wid
            raw_xml = raw_xml.replace(purge_wid_target, '')
            
            
            # SWAP CONSTANTS
            raw_xml = raw_xml.replace('1660922','2370711')
            raw_xml = raw_xml.replace('21845981','42909941')
            raw_xml = raw_xml.replace('mymedia.uwosh.edu','mediaspace.wisconsin.edu')
            
            
            # SAVE XML
            filename = obj.file.filename
            contentType = obj.file.contentType
            obj.file = NamedBlobFile(data=bytes(raw_xml),
                                     contentType=contentType,
                                     filename=filename
                                     )
            obj.reindexObject()
            
            
            new_media_url = self.find_between(raw_xml, '<media_url>', '</media_url>')
            output += old_path + ' | ' + old_id + ' ==> ' + new_id + ' | URL: ' + new_media_url + "\n"
            
        return output

    def find_between(self, s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""
            
    @property
    def portal(self):
        return api.portal.get()
        
        