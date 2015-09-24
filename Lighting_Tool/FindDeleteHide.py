import maya.cmds as cmds
'''Unlocks geo and user types in name of geo 
	and then invisi or deletes it
	references Eat3D and DT Scripting'''
import logging
import os


class FindGeo():

	def __init__(self):
		'''
		creates a  instance of a window every time its called
		'''


		#creates the window
		self.current_index=-1
		self.matches=[]
		self.search_string =""
		


		window_name = "LightingTools"
		window_title = "Lighting Tools v1.02"

		if cmds.window(window_name, q=True, exists=True):
			cmds.deleteUI(window_name)

		my_window = cmds.window(window_name, title=window_title, sizeable=False, resizeToFitChildren=True)

		main_layout = cmds.columnLayout(adj=True)
		
   
		#creates the buttons
		cmds.separator()

		cmds.text("Unlock Or Lock All Geo", bgc = (0.980, 0.502, 0.477))

		cmds.separator()
		
		self.lock = cmds.button(label="Unlock/Lock_ALL_GEO", command = self._unlock_geo)

		cmds.separator()

		cmds.text("Type Name of GEO", bgc = (1, 0.627, 0.478))

		cmds.separator()
		
		self.find_box = cmds.textFieldButtonGrp(label="Find", text="", adj=2, buttonLabel="Select", bc=self.find, cw=[1,50])
		
		cmds.separator()
		
		cmds.text("EX: :kelp, :SHELF, :tree ", bgc = (.6, 0.2, 1.0))

		cmds.separator()
		
		cmds.button(label="Invisi", command = self._hide_geo)
		
		cmds.button(label="Visible", command = self._unhide_geo)
	
		cmds.button(label="Delete", command = self._delete_geo)

		cmds.button(label="Unlock/Lock_Sel_GEO", command = self._unlock_single_geo)
		
		cmds.separator()

		cmds.text("V_Tools", bgc = (.678, 0.847, 0.902))

		cmds.separator()
		

		cmds.button(label="Connect Env. to IBL", command = self.connectIBLNode)
		cmds.button(label="DisConnect Env. to IBL", command = self.disconIBLNode)

		cmds.showWindow(my_window)

	

	def _unlock_geo(self, allObjects):
		'''
		unlock geo objects when selected
		'''		
		#unlocks objects
		
		allObjects = cmds.ls(typ = 'mesh')
		cmds.pickWalk(direction='down')

		cmds.select(allObjects)
		for geo in allObjects:
			print geo

			on = cmds.getAttr(geo + ".overrideEnabled")
			print on
			cmds.setAttr(geo +".overrideEnabled", not on)


			
			#sets objects to reference
			refer = cmds.getAttr(geo + ".overrideDisplayType")
			if refer == 2:
				print refer
				cmds.setAttr(geo + ".overrideDisplayType",0)
			else:
				cmds.setAttr(geo + ".overrideDisplayType", 2)

				
	def _get_matches(self):
		'''
		finds what the user typed in
		'''
		find_string = cmds.textFieldButtonGrp(self.find_box, q=True, text=True)
		matches = cmds.ls("*" +  find_string + "*", type="transform")

		return matches
	

	 
	def find(self):
		'''
		selects what the user typed in
		'''

		matches = self._get_matches()
		cmds.select(matches, r=True)
			
	


	def _hide_geo(self, myGroup):

		

		myGroup =  cmds.ls(sl=True)
		cmds.select(myGroup)
		#looks at all the kids inside group
		children = cmds.listRelatives(myGroup, allDescendents=True, noIntermediate=True, fullPath=True)

		lights = cmds.ls(children, type="light")
		meshes = cmds.ls(children, type="mesh")

		#hides and unhides based off the children
		for sel in meshes:
			cmds.getAttr(sel + ".visibility")
			cmds.setAttr(sel + ".visibility", 0)


		#hides based off group selection
		for sel in myGroup:
			cmds.getAttr(sel + ".visibility")
			cmds.setAttr(sel + ".visibility", 0)
		print visible


	def _unhide_geo(self, myGroup):

		myGroup = cmds.ls(sl=True)
		cmds.select(myGroup)

		children = cmds.listRelatives(myGroup, allDescendents=True, noIntermediate=True, fullPath=True)

		meshes = cmds.ls(children, type="mesh")

		for sel in meshes:
			cmds.getAttr(sel + ".visibility")
			cmds.setAttr(sel + ".visibility" ,1)

		for sel in myGroup:
			cmds.getAttr(sel + ".visibility")
			cmds.setAttr(sel + ".visibility",1)


	def _delete_geo(self, geoDel):
		
		#deletes geo
		geoDel = cmds.delete()

	def _unlock_single_geo(self, transforms):

		geometry = cmds.ls(sl=True)
		transforms = cmds.listRelatives(geometry, f=True)
		cmds.pickWalk(direction = 'down')

		print transforms
		for geo in transforms:
			on = cmds.getAttr(geo + ".overrideEnabled")
			print on
			cmds.setAttr(geo + ".overrideEnabled", not on)

			refer=cmds.getAttr(geo + ".overrideDisplayType")
			if refer == 2:
				print ".overrideEnabled", refer
				cmds.setAttr(geo + ".overrideDisplayType", 0)
			else:
				pass
	

	

	def connectIBLNode(self, connect):

		# connects with name spaces
		connect=cmds.connectAttr("*:env_lightShape.msg","mentalrayGlobals.imageBasedLighting")

	def disconIBLNode(self, discon):

		discon=cmds.disconnectAttr("*:env_lightShape.msg","mentalrayGlobals.imageBasedLighting")

		



FindGeo()