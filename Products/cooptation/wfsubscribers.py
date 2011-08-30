# -*- coding: utf-8 -*-
#
# File: wfsubscribers.py
#
# Copyright (c) 2011 by Ecreall
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Vincent Fretin and Michael Launay <development@ecreall.com>"""
__docformat__ = 'plaintext'


##code-section module-header #fill in your manual code here
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
##/code-section module-header


def notifyCooptationPending(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition \
       or event.transition.id not in ['submit'] \
       or obj != event.object:
        return
    ##code-section notifyCooptationPending #fill in your manual code here
    mtool = getToolByName(obj, 'portal_membership')
    prm = getToolByName(obj, 'acl_users').portal_role_manager
    # We don't manage groups!
    managers = [mtool.getMemberById(manager_id) for manager_id, dontcare in prm.listAssignedPrincipals('Manager')]
    notifyCooptation(obj, "cooptation_pending_notification", receipts=managers)
    ##/code-section notifyCooptationPending


def notifyCooptationRejected(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition \
       or event.transition.id not in ['reject'] \
       or obj != event.object:
        return
    ##code-section notifyCooptationRejected #fill in your manual code here
    notifyCooptation(obj, "cooptation_rejected_notification")
    ##/code-section notifyCooptationRejected


def doCooptationAcceptation(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition \
       or event.transition.id not in ['accept'] \
       or obj != event.object:
        return
    ##code-section doCooptationAcceptation #fill in your manual code here
    notifyCooptation(obj, "cooptation_accepted_notification")
    ##/code-section doCooptationAcceptation


def notifyCooptation(obj, template_name, actor=None, receipts=None, **kwargs):
    """if not actor use AUTHENTICATED_USER
       if not receipts use obj.getOwner()
    """
    mtool = getToolByName(obj, 'portal_membership')
    MailHost = getToolByName(obj, 'MailHost')
    if not actor:
        actor = obj.REQUEST.AUTHENTICATED_USER
    actor_fullname = actor.getProperty('fullname', actor.getId())
    actor_email = actor.getProperty('email', None)
    encoding = getUtility(ISiteRoot).getProperty('email_charset')
    template = getattr(obj, template_name)
    if not receipts:
        receipts = [obj.getOwner()]
    for receipt in receipts:
        if receipt is not None:
            receipt_email = receipt.getProperty('email', None)
            receipt_fullname = receipt.getProperty('fullname', receipt.getId())
            if receipt_email:
                message = template(obj,
                                   obj.REQUEST,
                                   actor_fullname=actor_fullname,
                                   actor_email=actor_email,
                                   receipt_to_email=receipt_email,
                                   receipt_to_name=receipt_fullname,
                                   **kwargs)

                MailHost.send(message.encode(encoding))


##code-section module-footer #fill in your manual code here
##/code-section module-footer

