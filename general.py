# -*- coding: utf-8 -*-
# @Time    : 5/16/2021 4:35 PM
# @Author  : Mingdian Liu
# @Email   : mingdian@iastate.edu lmdvigor@gmail.com
# @File    : hfssGeneral.py
# @Software: PyCharm


# -------------------------------------------------------------------------- #
# function hfssNewProject(fid)
#
# Description :
# -------------
# This function creates the necessary VBScript to create a new HFSS project
# file, set it as the active project.
#
# Parameters:
# -----------
# fid         - file identifier of the VBScript File.
# -------------------------------------------------------------------------- #

# ----------------------------------------------------------------------------
# This file is part of HFSS-MATLAB-API.
#
# HFSS-MATLAB-API is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# HFSS-MATLAB-API is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with
# Foobar; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
# Copyright 2004, Vijay Ramasami (rvc@ku.edu)
# ----------------------------------------------------------------------------

def hfssNewProject(fid):
    # Preamble.
    fid.write('Dim oHfssApp\n')
    fid.write('Dim oDesktop\n')
    fid.write('Dim oProject\n')
    fid.write('Dim oDesign\n')
    fid.write('Dim oEditor\n')
    fid.write('Dim oModule\n')
    fid.write('\n')

    # Create a New Project.
    fid.write('Set oHfssApp  = CreateObject("AnsoftHfss.HfssScriptInterface")\n')
    fid.write('Set oDesktop = oHfssApp.GetAppDesktop()\n')
    fid.write('oDesktop.RestoreWindow\n')
    fid.write('oDesktop.NewProject\n')

    # The new project created is the active project.
    fid.write('Set oProject = oDesktop.GetActiveProject\n')


# ----------------------------------------------------------------------------
# function hfssInsertDesign(fid, designName, [designType = 'driven modal'])
#
# Description :
# -------------
# Create the necessary VB Script to insert an HFSS Design into the Project
# and set it as the active design.
#
# Parameters :
# ------------
# fid        - file identifier of the HFSS script file.
# designName - name of the new design to be inserted.
# designType - (Optional String) choose from the following:
#              1. 'driven modal' (default)
#              2. 'driven terminal'
#              3. 'eigenmode'
#
# Note :
# ------
# This function is usually called after a call to either hfssNewProject()
# or hfssOpenProject(), but this is not necessary.
#
# Example :
# ---------
# fid = fopen('myantenna.vbs', 'wt');
# ...
# hfssInsertDesign(fid, 'Dipole_SingleElement');
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# This file is part of HFSS-MATLAB-API.
#
# HFSS-MATLAB-API is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# HFSS-MATLAB-API is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with
# Foobar; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
# Copyright 2004, Vijay Ramasami (rvc@ku.edu)
# ----------------------------------------------------------------------------
def hfssInsertDesign(fid, designName, designType='driven modal'):
    # create the necessary script.
    fid.write('\n')
    fid.write('oProject.InsertDesign "HFSS", "')
    fid.write(designName+'", ')

    if designType.lower() == 'driven terminal':
        fid.write('"DrivenTerminal", ""\n')
    elif designType.lower() == 'driven modal':
        fid.write('"DrivenModal", ""\n')
    elif designType.lower() == 'eigenmode':
        fid.write('"Eigenmode", ""\n')

    fid.write('Set oDesign = oProject.SetActiveDesign("{0}")\n'.format(designName))
    fid.write('Set oEditor = oDesign.SetActiveEditor("3D Modeler")\n')