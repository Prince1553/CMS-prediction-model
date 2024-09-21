# -*- coding: utf-8 -*-
""" Importing Required Libraries """


import os
import re
import joblib
import pandas as pd


""" CMS Patterns Dictionary"""


cms_patterns = {
    "Jekyll": {
        "meta": ["meta name='generator' content='Jekyll'","meta name='jekyll-theme' content=''", "meta name='jekyll-version' content=''", 'jekyll'],
        "links": ["/feed.xml","/jekyll/","/jekyll/js/", 'jekyll.css', 'jekyll'],
        "scripts": ["jekyll-seo-tag.js","/jekyll-","jekyll.js"],
         "html_structure":["class='jekyll-'","id='jekyll-'",]

    },
    "Concrete CMS": {
        "meta": ["meta name='generator' content='concrete5'", "meta name='concrete-cms' content=''","meta name='concrete-version' content=''"],
        "links": ["/concrete/","cdn.concretecms.com",],
        "scripts": ["ccm.app.js", "ccm.base.js", "ccm.forms.js","ccm.dashboard.js","ccm.notifications.js",],
        # "directories": ["/dashboard", "/index.php/dashboard/"],
        "html_structure": ["id='ccm-'", "class='ccm-'"],
    },
    "Joomla": {
        "meta": ["meta name='generator' content='Joomla'","meta name='joomla-version' content=''", "meta name='joomla-cms' content=''","meta name='joomla-template' content=''",'joomla'],
        "links": ["/media/jui/css/", "/joomla/","cdn.joomla.org"],
        "scripts": ["joomla.javascript.js","jui.js", "jquery.min.js","joomla.js","joomla.core.js"],
        # "admin_pages": ["/administrator/", "/index.php?option=com_"],
        "html_structure": ["class='com-'","id='joomla-'",],
    },
    "Ghost": {
        "meta": ["meta name='generator' content='Ghost'", "meta name='ghost-version' content=''","meta name='ghost-theme' content=''","meta name='ghost-publisher' content=''",'ghost'],
        "links": [ "/ghost/","ghost.css","cdn.ghost.org","ghost.org","/ghost/ghost.css",'ghost'],
        "scripts": ["ghost.min.js","ghost.js","ghost-"],
        "admin_pages": ["/ghost/"],
        "html_structure": ["id='ghost-"],
    },
    "Shopify": {
        "meta": ["meta name='generator' content='Shopify'","meta name='shopify-' content=''",'Shopify'],
        "links": ["cdn.shopify.com", "/shopify/","shopify.css","shopifycdn.com","shopifyapp.com",'Shopify'],
        "scripts": ["shopify_", "shopify_checkout.js","shopify-",],
        "html_structure": ["class='shopify-'","id='shopify-'"],
        "admin_pages": ["/checkout.shopify.com","/shopify/"],
    },
    "Hubspot": {
        "meta": ["meta name='generator' content='HubSpot'", "meta name='hubspot-site-id' ",'hubspot'],
        "links": ["hs-scripts.com", "hsforms.net","/hubspot/","hubspotcdn.com","/hs-",'hubspot','hs-scripts', 'hs-internal',],
        "scripts": ["hs-analytics.js", "hs-banner.js","hs-scripts",'hubspot'],
        "html_structure": ["hs-form","class='/hs-'",'hubspot'],
        "headers": ["__hs_do_not_track_cookie","__hs_do_not_track_cookie", "__hs_opt_out_cookie", "__hs_session_id", "__hs_first_visit", "__hs_page_id"],
         "admin_pages": [ "/hubspot/",]
    },
    "BigCommerce": {
        "meta": ["meta name='generator' content='BigCommerce'","meta property='og:site_name' content='BigCommerce'",],
        "links": ["/cdn11.bigcommerce.com/","/bigcommerce/"],
        "scripts": ["stencil-utils.js", "bigcommerce.analytics.js","stencil.js"],

    },
    "Magento": {
        "meta": ["meta name='generator' content='Magento'","meta property='og:site_name' content='Magento'"],
        "links": ["-mage/","/mega.css"],
        "scripts": ["requirejs/require.js", "/mage/app.js","/mage/","mage/mage.js"],

    },
    "Blogger": {
        "meta": ["meta name='generator' content='Blogger'","meta property='og:site_name' content='Blogger'", "meta content='blogger' name='generator'"],
        "links": [".blogspot.com/", "blogger.com","blogger.googleusercontent.com","bp.blogspot.com", "widget.blogger",],
        "scripts": ["blogger.js","blogspot.js",],
        # "html_structure": ["<article class='post-outer'>", "<div class='post-body entry-content'>"],
        "admin_pages": ["/feeds/posts/default", "/blogger.g",],
    },
    "Drupal": {
        "meta": ["meta name='generator' content='Drupal'","meta name='X-Drupal-Cache'","meta name='X-Generator' content='Drupal'", "meta property='og:site_name' content='Drupal'"],
        "links": ["/core/misc/drupal.js",'/drupal/', 'drupal.css'],
        "scripts": ["drupal.js", "drupalSettings","drupal.init.js","/misc/jquery.js","/core/modules/system/js/drupal.js"],
        "html_structure": [ "id='block-system-main'", "id='drupal-page'"],
        "admin_pages": ["/user/login", "/admin/config"],
    },

    'WordPress': {
        'meta': ['wp-', 'generator="WordPress"',"meta name='generator' content='WordPress'","meta name='X-Pingback'", "meta name='og:site_name' content='WordPress'"],
        'scripts': ['wp-', 'wp-content', 'wp-includes'],
        'links': ['wp-', 'wp-content', 'wp-includes', 'wp-json', 'wp-config.php', 'wp-cron.php'],
        'unique_pages': ['wp-login.php', 'wp-admin'],
        'plugins': ['/wp-content/plugins/'],
        'themes': ['/wp-content/themes/'],
    },
    "Typo3": {
        "meta": ["meta name='generator' content='TYPO3'","meta name='X-TYPO3-'",],
        "links": ["/typo3/", "/typo3_src/","/typo3conf/","/typo3temp/"],
        "scripts": ["typo3/init.js", "typo3/cms.js", "/typo3/"],
        "html_structure": ["class='tx-","id='typo3-'",],
        "admin_pages": ["/typo3/login", "/typo3/index.php","/typo3/"],
    },
    "1-C Bitrix": {
        "meta": ["meta name='generator' content='1C-Bitrix'","meta name='X-Bitrix'", "meta name='Bitrix SM'",],
        "links": ["/bitrix/", "/bitrix24/"],
        "scripts": ["bitrix/js/main/core/core.js", "bitrix24", "/bitrix/"],
        "html_structure": ["bitrix-", "<bx-html>"],
        "admin_pages": ["/bitrix/"],
    },
    "Adobe Experience Manager": {
        "meta": ["meta name='generator' content='AEM'","Adobe CQ","meta name='AEM-Caching'"],
        "links": ["content/dam/", "/etc/designs/",'etc.clientlibs', 'etc/designs'],
        "scripts": ["granite.min.js", "clientlibs/granite.js",'etc.clientlibs', 'cq.wcm.foundation', 'granite/ui'],
        "html_structure": ["cq:Page", "cq:content"],
        "admin_pages": ["/libs/granite/core/content/login"],
    },
    "Butter CMS": {
        "meta": ["meta name='generator' content='ButterCMS'","meta property='og:site_name' content='ButterCMS'","buttercms",],
        "links": ["/buttercms/","buttercms.css"],
        "scripts": ["buttercms.js"],
        "json": ["buttercms.pages", "buttercms.posts", "buttercms.categories", "buttercms.authors"],  # JSON keys found in API responses or HTML data
        "iframes": ["<iframe src='https://buttercms.com/embed'"],
        "html_structure": ["class='buttercms-'", "id='buttercms-'", "-buttercms-"],
    },
    "CMS Made Simple": {
        "meta": ["meta name='generator' content='CMS Made Simple'","meta name='cms_version'"],
        "links": ["cmsms.css","/cmsms/"],
        "scripts": ["cmsms.js","jquery.cmsms.js","/cmsms/"],
        "html_structure": ["id='cms-'","class='cmsms_'", "class='cms-'", "-cmsms-",]
    },
    "Contao": {
        "meta": ["meta name='generator' content='Contao'",'Contao'],
        "links": ["/contao/", "contao.css",'Contao'],
        "scripts": ["contao.js", "/assets/js/contao.min.js","/contao/",'Contao'],
        "html_structure": ["class='contao-'","id='contao-'","-contao-", "data-contao-widget"],
        "admin_pages": ["/contao/"],
    },
    "Contentful": {
        "meta": ["meta name='generator' content='Contentful'","meta name='x-contentful-space-id'", "meta name='x-contentful-environment'",'Contentful/','Contentful'],
        "links": ["cdn.contentful.com","images.ctfassets.net", "assets.ctfassets.net","contentful"],
        "scripts": ["contentful.js", "contentful-management.js", "cdn.contentful.com/assets/js/contentful.min.js","contentful"],
        "html_structure": ["class='contentful-'", "class='ctf_'", "-contentful-",],
        'unique_pages': ['/contentful/']
    },
    "CraftCMS": {
        "meta": ["meta name='generator' content='CraftCMS'","meta name='generator' content='Craft CMS'","meta name='craft-csrf-token'", 'craftcms'],
        "links": ["/craftcms.com", "/craft/", 'craftcms'],
        "scripts": ["craftcms.min.js", "craft.js","jquery.craft.js","/cpresources/craft.min.js",'craftcms'],
        "html_structure": ["class='craft-'","id='craft-'","-craft-", 'craftcms'],
        # "admin_pages": ["/admin/", "/login"],
    },
    "Directus": {
        "meta": ["meta name='generator' content='Directus'","meta name='directus-version'", "meta name='x-powered-by' content='Directus'",],
        "links": ["/directus/","directus.css"],
        "scripts": ["directus.js","directus.min.js","directus.bundle.js"],
        "html_structure": ["class='directus-'","id='directus-'","-directus-",],
        "admin_pages": ["/directus/","directus.json"],
    },
    "dotCMS": {
        "meta": ["meta name='generator' content='dotCMS'","meta name='x-powered-by' content='dotCMS'",'dotCMS'],
        "links": ["/dotcms/","dotcms.css","dotcms"],
        "scripts": ["dotcms.js","dotcms.min.js", "dotcms-admin.js","dotcms"],
        "html_structure": ["class='dotcms-'","id='dotcms-'","-dotcms-"],
        "admin_pages": ["/dotcms/login","/dotAdmin/","/dotcms/controlpanel/","/dotcms/"],
    },
    "ExpressionEngine": {
        "meta": ["meta name='generator' content='ExpressionEngine'","meta name='x-powered-by' content='ExpressionEngine'",],
        # "links": ["/themes/", "/system/"],
        "scripts": ["expressionengine.js", "ee.min.js","/themes/ee/js/",],
        "html_structure": ["class='ee-'","id='ee-'","-ee-","ee_session_id",],
        "admin_pages": ["expressionengine-config.php",],
    },
    "Godaddy Website Builder": {
        "meta": ["meta name='generator' content='GoDaddy Website Builder'","meta name='x-powered-by' content='GoDaddy Website Builder'",'GoDaddy Website Builder','godaddy'],
        "links": ["/godaddy/",'godaddy','godaddy.css'],
        "scripts": ["godaddy.js","godaddy.min.js","go-builder.js","/godaddy/js/main.js",'godaddy/'],
        "html_structure": ["class='godaddy-'","id='godaddy-'",'/godaddy/'],
        "admin_pages": ["/godaddy/",],
    },
    "Grav CMS": {
        "meta": ["meta name='generator' content='Grav'", "meta name='x-powered-by' content='Grav CMS'",'grav'],
        "links": ['grav.css' ],
        "scripts": ["grav.js","grav.min.js",'/grav/'],
        "html_structure": ["class='grav-'", "id='grav-'",],
        "admin_pages": ["/admin/"],
    },
    "Hugo": {
        "meta": ["meta name='generator' content='Hugo'","meta name='x-powered-by' content='Hugo'",'hugo'],
        "links": ["/hugo/",'hugo'],
        "scripts": ["hugo.js","hugo.min.js",'/hugo/'],
        "html_structure": ["class='hugo-'","id='hugo-'",],
    },
    "Jimdo": {
        "meta": ["meta name='generator' content='Jimdo'","meta name='x-powered-by' content='Jimdo'",],
        "links": ["jimdo.com", "/jimdo/", "jimdo.css"],
        "scripts": ["jimdo.js","jimdo.min.js",],
        "html_structure": ["class='jimdo-'","id='jimdo-'"],
    },
    "Kentico": {
        "meta": ["meta name='generator' content='Kentico'","meta name='x-powered-by' content='Kentico'",'Kentico'],
        "links": ["/kentico/",],
        "scripts": ["kentico.js","kentico.min.js","kentico-admin.js",],
        "html_structure": ["class='kentico-'","id='kentico-'",],
        "admin_pages": ["/CMSPages/"],
    },
    "Liferay": {
        "meta": ["meta name='generator' content='Liferay'", "meta name='x-powered-by' content='Liferay'",],
        "links": ["/liferay/"],
        "scripts": ["liferay.js","liferay-"],
        "html_structure": ["class='liferay-'","id='liferay-'",],
        "admin_pages": ["/group/control_panel/"],
    },
    "Lithium": {
        "meta": ["meta name='generator' content='Lithium'", "meta name='x-powered-by' content='Lithium'",],
        "links": ["/lithium/"],
        "scripts": ["lithium.js","lithium.min.js","lithium-admin.js",],
        "html_structure": ["class='lithium-'","id='lithium-'",],
    },
    "Magnolia": {
        "meta": ["meta name='generator' content='Magnolia'","meta name='x-powered-by' content='Magnolia'","meta name='magnolia-version' content=''",],
        "links": ["/magnolia/"],
        "scripts": ["magnolia.js", "magnolia-"],
        "html_structure": ["class='magnolia-'","id='magnolia-'",],
        "admin_pages": ["/magnolia/"],
    },
    "NeosCMS": {
        "meta": ["meta name='generator' content='Neos'","meta name='x-powered-by' content='NeosCMS'", "meta name='neos-version'",],
        "links": ["/neos/"],
        "scripts": ["neos.js","neos-"],
        "html_structure": ["class='neos-'","id='neos-'",],
        "admin_pages": ["/neos/"],
    },
    "October CMS": {
        "meta": ["meta name='generator' content='October CMS'",  "meta name='x-powered-by' content='OctoberCMS'","meta name='october-version'",'octoberCMS'],
        "links": ['octoberCMS'],
        "scripts": ["october.js","octoberCMS-",'octoberCMS'],
        "html_structure": ["class='octoberCMS-'","id='octoberCMS-"],
        # "admin_pages": ["/backend/"],
    },
    "PhpBB": {
        "meta": ["meta name='generator' content='phpBB'","meta name='x-powered-by' content='phpBB'","meta name='phpbb-version' ",'phpBB'],
        "links": ["/phpbb/",'phpBB'],
        "scripts": ["phpbb.js","phpbb-",'phpBB'],
        "html_structure": ["class='forum-'", "id='phpbb-'"],
        "admin_pages": ["/adm/","phpbb-config.php","phpbb-settings.php","phpbb-session.php",'phpBB'],
    },
    "Piwigo": {
        "meta": ["meta name='generator' content='Piwigo'","meta name='x-powered-by' content='Piwigo'", "meta name='piwigo-version' ",'piwigo'],
        "links": ["/piwigo/",'piwigo'],
        "scripts": ["piwigo.js","piwigo-",'piwigo'],
        "html_structure": ["class='piwigo-'","id='piwigo-'",],
        # "admin_pages": ["/admin.php"],
    },
    "Plone": {
        "meta": ["meta name='generator' content='Plone'" "meta name='x-powered-by' content='Plone'","meta name='plone-version' ",],
        "links": ["/plone/"],
        "scripts": ["plone.js","plone-"],
        "html_structure": ["class='plone-'","id='plone-'",],
        "admin_pages": ["/manage_main"],
    },
    "Prismic": {
        "meta": ["meta name='generator' content='Prismic'","meta name='prismic-version' ","meta name='prismic-api' "],
        "links": ["cdn.prismic.io","/prismic/","prismic.css",],
        "scripts": ["prismic.js","prismic-"],
        "html_structure": ["class='prismic-'","id='prismic-",],
        "admin_pages": ["/prismic/",]
    },
    "Process Wire": {
        "meta": ["meta name='generator' content='ProcessWire'","meta name='processwire-version' ",'ProcessWire','processwire'],
        "links": ["/processwire/",'processwire',],
        "scripts": ["processwire.js",'processwire'],
        "html_structure": ["class='processwire-'","id='processwire-"],
        "admin_pages": ["/processwire/"],
    },
    "Progress Sitefinity": {
        "meta": ["meta name='generator' content='Sitefinity'","meta name='sitefinity-version' ", "meta name='sitefinity-cms' ",'Sitefinity'],
        "links": ["/sitefinity/","sitefinity.css",'Sitefinity'],
        "scripts": ["sitefinity.js","sitefinity-",'Sitefinity'],
        "html_structure": ["class='sitefinity-'","id='sitefinity-"],
        "admin_pages": ["/sitefinity/"],
    },
    "Sanity": {
        "meta": ["meta name='generator' content='Sanity'","meta name='sanity-version'", "meta name='sanity-cms' "],
        "links": ["cdn.sanity.io","/sanity/",'sanity'],
        "scripts": ["sanity.js","sanity-",'sanity'],
        "html_structure": ["class='sanity-'","id='sanity-'",],
         "admin_pages": [ "/sanity/" ],
    },
    "Silverstripe": {
        "meta": ["meta name='generator' content='SilverStripe'","meta name='silverstripe-version'", "meta name='silverstripe-cms'",'SilverStripe' ],
        "links": ["/silverstripe/","silverstripe.css",'SilverStripe'],
        "scripts": ["silverstripe.js","/silverstripe-",'SilverStripe'],
        "html_structure": ["class='silverstripe-'","id='silverstripe-"],
        # "admin_pages": ["/admin/"],
    },
    "Sitecore": {
        "meta": ["meta name='generator' content='Sitecore'","meta name='sitecore-version'", "meta name='sitecore-cms' ", "meta name='sitecore-web'",'Sitecore'],
        "links": ["/sitecore/","sitecore.css",'Sitecore'],
        "scripts": ["sitecore.js","sitecore-",'Sitecore'],
        "html_structure": ["class='sitecore-'","id='sitecore-"],
        "admin_pages": ["/sitecore/"],
    },
    "SMF": {
        "meta": ["meta name='generator' content='SMF'","meta name='smf-version'","meta name='smf-forum' "],
        "links": ["/smf/","smf.css"],
        "scripts": ["smf.js","/smf-"],
        "html_structure": ["class='smf-'","id='smf-"],
         "admin_pages": ["/smf/",]
    },
    "Squarespace": {
        "meta": ["meta name='generator' content='Squarespace'", "meta name='squarespace-version'","meta name='squarespace-site'"],
        "links": ["/static.squarespace.com/", "squarespace-cdn.com","/squarespace/","squarespace.css",],
        "scripts": ["squarespace-analytics.js","squarespace.js","/squarespace-"],
        "html_structure": ["class='sqs-'","id='sqs-'"],
        # "admin_pages": ["/config/"],
    },
    "Squiz Suite": {
        "meta": ["meta name='generator' content='Squiz Suite'", "meta name='squiz-version'", "meta name='squiz-site' "],
        "links": ["/squiz/","squiz.css"],
        "scripts": ["squiz.js","/squiz-"],
        "html_structure": ["class='squiz-'","id='squiz-'"],
        # "admin_pages": ["/admin/"],
    },
    "Statamic": {
        "meta": ["meta name='generator' content='Statamic'","meta name='statamic-version'","meta name='statamic-site' ",'Statamic'],
        "links": ["/statamic/","statamic.css",'Statamic'],
        "scripts": ["statamic.js","/statamic-",'Statamic'],
        "html_structure": ["class='statamic-'","id='statamic-'"],
        "admin_pages": ["/cp/"],
    },
    "Storyblok": {
        "meta": ["meta name='generator' content='Storyblok'", "meta name='storyblok-version'", "meta name='storyblok-site' ",'Storyblok'],
        "links": ["cdn.storyblok.com","/storyblok/",'Storyblok'],
        "scripts": ["storyblok.js",],
        "html_structure": ["class='storyblok-'","id='storyblok-"],
    },
    "Strapi": {
        "meta": ["meta name='generator' content='Strapi'", "meta name='strapi-version'","meta name='strapi-site' ",'Strapi'],
        "links": ["/strapi/",'Strapi'],
        "scripts": ["strapi.js","/strapi-",'Strapi'],
        "html_structure": ["class='strapi-'","id='strapi-'"],
        # "admin_pages": ["/admin/"],
    },
    "Tilda": {
        "meta": ["meta name='generator' content='Tilda'","meta name='tilda-version'","meta name='tilda-site' ",'tilda'],
        "links": ["/tilda/",'tilda'],
        "scripts": ["tilda.js","/tilda/",'tilda'],
        "html_structure": ["class='tilda-'","id='tilda-'"],
    },
    "Umbraco": {
        "meta": ["meta name='generator' content='Umbraco'", "meta name='umbraco-version'","meta name='umbraco-site' "],
        "links": ["/umbraco/","umbraco.css"],
        "scripts": ["umbraco.js","/umbraco/"],
        "html_structure": ["class='umbraco-'","id='umbraco-'"],
        "admin_pages": ["/umbraco/"],
    },
    "vBulletin": {
        "meta": ["meta name='generator' content='vBulletin'", "meta name='vbulletin-version'","meta name='vbulletin-forum'",'vBulletin'],
        "links": ["/vbulletin/","vbulletin-cdn.com","vbulletin.css",'vBulletin'],
        "scripts": ["vbulletin-core.js", "ajax_vbulletin.js","vbulletin.js","/vbulletin/",'vBulletin'],
        "html_structure": ["class='postbit'","class='vb-'","id='vb-'",],
        "admin_pages": ["/admincp/", "/moderator.php"],
    },
    "Webflow": {
        "meta": ["meta name='generator' content='Webflow'","meta name='webflow-version'",'Webflow'],
        "links": ["webflow.com","/webflow/","webflow.css",'Webflow'],
        "scripts": ["webflow.js", "webflow-analytics.js", "webflow-",'Webflow'],
        "html_structure": ["class='webflow-'","id='wf-'","class='wf-'",],
    },
    "Weebly": {
        "meta": ["meta name='generator' content='Weebly'", "meta name='weebly-version'"],
        "links": ["/weeblycloud/", "weebly.com","weebly.css","/weebly/"],
        "scripts": ["weebly.min.js","weebly.js"],
        "html_structure": ["class='wsite-'","class='Weebly-'"],
        # "admin_pages": ["/account/login", "/dashboard"],
    },
    "Wix": {
        "meta": ["meta name='generator' content='Wix'","meta name='wix-version'","meta name='wix-site-id'"],
        "links": ["static.parastorage.com", "wixsite.com","/wix/","/wixapps/"],
        "scripts": ["wixcode.js", "wixapps.js" "/wix-",],
        "html_structure": ["class='comp-","class='wix-'", "id='wix-'",],
        # "admin_pages": ["/home", "/contact-us"],
    },
    "XenForo": {
        "meta": ["meta name='generator' content='XenForo'", "meta name='xenforo-version'","meta name='xenforo-application'",'XenForo'],
        "links": ["/xenforo/","xenforo.com", "static.xenforo.com" ,"xenforo.css"],
        "scripts": ["xf.js", "xenforo-overlay.js","/xenforo-",],
        "html_structure": [ "class='xenforo-'","id='xenforo-'",],
    },
    "Plesk": {
        "meta": ["meta name='generator' content='Plesk'","meta name='plesk-version'", "meta name='plesk-admin'"],
        "links": ["/plesk/","plesk.com","static.plesk.com","plesk.css",'plesk'],
        "scripts": ["plesk.js","/plesk-/",'plesk'],
        "html_structure": ["class='plesk-'","id='plesk-'"],
    },
    "OpenCMS": {
        "meta": ["meta name='generator' content='OpenCMS'", "meta name='opencms-version'", "meta name='opencms-author'",'OpenCMS'],
        "links": ["/opencms/","opencms.com","static.opencms.com",'OpenCMS'],
        "scripts": ["opencms.js","/opencms-",'OpenCMS'],
        "html_structure": ["class='opencms-'", "id='opencms-'",],
        "admin_pages": ["/opencms/"]
    }
}


""" Feature Extraction Function """


def extract_features(html_content):
    """
    Extracts features (presence of patterns) for each CMS and returns a feature vector.
    """
    feature_vector = {}
    for cms, patterns in cms_patterns.items():

        feature_vector[cms] = 0

        for category, patterns_list in patterns.items():
            for pattern in patterns_list:
                if re.search(pattern, html_content, re.IGNORECASE):
                    feature_vector[cms] = 1
                    break
    return feature_vector


""" Loading the Saved Model and Training Columns """


model = joblib.load('/content/random_forest_cms_model.pkl')

training_columns = joblib.load('/content/training_columns.pkl')


"""Reading HTML Files and Making Predictions """


def read_html_file(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Path to the folder containing .html files
folder_path = "/content/drive/MyDrive/ CMS/cms_files/Jekyll "

results = []

for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        html_file_path = os.path.join(folder_path, filename)

        html_content = read_html_file(html_file_path)

        new_features = extract_features(html_content)

        df_new_features = pd.DataFrame([new_features])

        df_new_features = df_new_features.reindex(columns=training_columns, fill_value=0)

        # Predict the CMS
        predicted_cms = model.predict(df_new_features)

        results.append({
            'Filename': filename,
            'CMS': predicted_cms[0]
        })

df_results = pd.DataFrame(results)

# Save the results to a CSV file
csv_output_path = 'predictions1.csv'
df_results.to_csv(csv_output_path, index=False)

print("Predictions have been saved to:", csv_output_path)
