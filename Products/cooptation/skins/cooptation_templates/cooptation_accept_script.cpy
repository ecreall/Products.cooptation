## Script (Python) "cooptation_accept_script"
##title=Edit content 
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id=''
##
from Products.CMFCore.utils import getToolByName

#Save changes normal way
state = context.content_edit_impl(state, id)
context = state.getContext()

context.REQUEST.set('fullname', context.Title())

portal_workflow = getToolByName(context, 'portal_workflow')
if portal_workflow.getInfoFor(context, 'review_state') == 'pending':
    portal_workflow.doActionFor(context, 'accept', comment=context.REQUEST['comment'])

state.setNextAction('traverse_to:string:cooptation_register')
return state
