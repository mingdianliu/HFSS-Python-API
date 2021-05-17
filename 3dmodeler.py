# -*- coding: utf-8 -*-
# @Time    : 5/16/2021 5:17 PM
# @Author  : Mingdian Liu
# @Email   : mingdian@iastate.edu lmdvigor@gmail.com
# @File    : 3dmodeler.py
# @Software: PyCharm

# ----------------------------------------------------------------------------
# function hfssDipole(fid, Name, Axis, Center, Length, Size, gapLen, ...
#                     Units, [Type], [StrpNrmlAxis])
#
# Description :
# -------------
# Creates the VB Script necessary to model a dipole antenna in HFSS. The
# dipole can be either a cylinder, a strip or a cuboid.
#
# Parameters :
# ------------
# fid     - file identifier of the HFSS script file.
# Name    - name of the dipole (the actual names will appears Name1 and Name2
#           in the 3D Modeller).
# Axis    - specify as either 'X', 'Y' or 'Z' - the axis of the dipole.
# Center  - center of the dipole antenna.
# Length  - total length of the dipole antenna (including the center gap).
# Size    - if the dipole is cylindrical (default), this represents the dipole
#           diameter. Similarly, for a cuboid, Size represents the
#           cross-section dimension, and for a strip, Size represents the
#           strip width.
# gapLen  - the length of the dipole gap.
# Units   - can be specified as 'in', 'mm', 'meter' or anything else defined
#           in HFSS.
# [Type]  - (optional) type of the dipole. Specify as:
#           'c' - cylinder (default).
#           'r' - cuboid.
#           's' - strip.
# [StrpNrmlAxis] - (optional) if the dipole type is a strip, then this
#                  specifies the axis that is normal to the strip. By default,
#                  the axis next to 'Axis' in the right-hand sense is taken.
#                  (i.e., 'X' for 'Z', 'Y' for 'X', ...)
#
# Note :
# ------
# Each arm of the dipole will be (Length - gapLen)/2 long.
#
# ----------------------------------------------------------------------------

def hfssDipole(fid, Name, Axis, Center, Length, Size, gapLen, Units, Type='c', StrpAxis=''):
    if StrpAxis == '':
        if Axis == 'X':
            StrpAxis = 'Y'
        elif Axis == 'Y':
            StrpAxis = 'Z'
        elif Axis == 'Z':
            StrpAxis = 'X'

    if StrpAxis == Axis:
        raise Exception('The Strip Axis and the Antenna Axis cannot be the same !!')

    Name1 = Name + '1'
    Name2 = Name + '2'

    if Axis == 'X':
        Start1c = Center + [gapLen / 2, 0, 0]
        Start2c = Center - [gapLen / 2, 0, 0]
        Start1b = Center + [gapLen / 2, -Size / 2, -Size / 2]
        Start2b = Center - [gapLen / 2, +Size / 2, +Size / 2]
        bSize1 = [+(Length - gapLen) / 2, Size, Size]
        bSize2 = [-(Length - gapLen) / 2, Size, Size]
    elif Axis == 'Y':
        Start1c = Center + [0, gapLen / 2, 0]
        Start2c = Center - [0, gapLen / 2, 0]
        Start1b = Center + [-Size / 2, gapLen / 2, -Size / 2]
        Start2b = Center - [+Size / 2, gapLen / 2, +Size / 2]
        bSize1 = [Size, +(Length - gapLen) / 2, Size]
        bSize2 = [Size, -(Length - gapLen) / 2, Size]
    elif Axis == 'Z':
        Start1c = Center + [0, 0, gapLen / 2]
        Start2c = Center - [0, 0, gapLen / 2]
        Start1b = Center + [-Size / 2, -Size / 2, -gapLen / 2]
        Start2b = Center - [+Size / 2, +Size / 2, -gapLen / 2]
        bSize1 = [Size, Size, +(Length - gapLen) / 2]
        bSize2 = [Size, Size, -(Length - gapLen) / 2]

    if Type == 'c':

        hfssCylinder(fid, Name1, Axis, Start1c, Size / 2,
                     (Length - gapLen) / 2, Units)
        hfssCylinder(fid, Name2, Axis, Start2c, Size / 2,
                     -(Length - gapLen) / 2, Units)

    elif Type == 'r':
        hfssBox(fid, Name1, Start1b, bSize1, Units)
        hfssBox(fid, Name2, Start2b, bSize2, Units)

    elif Type == 's':
        if Axis == 'X':
            if StrpAxis == 'Y':
                sStart1 = Center + [gapLen / 2, 0, -Size / 2]
                sStart2 = Center - [gapLen / 2, 0, +Size / 2]
                Width1 = Size
                Width2 = Size
                Height1 = Length - gapLen / 2
                Height2 = -Height1
            elif StrpAxis == 'Z':
                sStart1 = Center + [gapLen / 2, -Size / 2, 0]
                sStart2 = Center - [gapLen / 2, +Size / 2, 0]
                Width1 = Length - gapLen / 2
                Width2 = - Width1
                Height1 = Size
                Height2 = Size
        elif Axis == 'Y':
            if StrpAxis == 'Z':
                sStart1 = Center + [-Size / 2, gapLen / 2, 0]
                sStart2 = Center - [+Size / 2, gapLen / 2, 0]
                Width1 = Size
                Width2 = Size
                Height1 = Length - gapLen / 2
                Height2 = -Height1
            elif StrpAxis == 'X':
                sStart1 = Center + [0, gapLen / 2, -Size / 2]
                sStart2 = Center - [0, gapLen / 2, +Size / 2]
                Width1 = Length - gapLen / 2
                Width2 = -Width1
                Height1 = Size
                Height2 = Size
        elif Axis == 'Z':
            if StrpAxis == 'Y':
                sStart1 = Center + [-Size / 2, 0, gapLen / 2]
                sStart2 = Center - [+Size / 2, 0, gapLen / 2]
                Width1 = Length - gapLen / 2
                Width2 = - Width1
                Height1 = Size
                Height2 = Size
            elif StrpAxis == 'X':
                sStart1 = Center + [0, -Size / 2, gapLen / 2]
                sStart2 = Center - [0, +Size / 2, gapLen / 2]
                Width1 = Size
                Width2 = Size
                Height1 = Length - gapLen / 2
                Height2 = - Height1

        hfssRectangle(fid, Name1, StrpAxis, sStart1, Width1, Height1, Units)
        hfssRectangle(fid, Name2, StrpAxis, sStart2, Width2, Height2, Units)


# ----------------------------------------------------------------------------
# function hfssCylinder(fid, Name, Axis, Center, Radius, Height, Units)
#
# Description :
# -------------
# Creates the VB script necessary to model a cylinder in HFSS.
#
# Parameters :
# ------------
# fid     - file identifier of the HFSS script file.
# Name    - name of the cylinder (in HFSS).
# Center  - center of the cylinder (specify as [x, y, z]). This is also the
#           starting point of the cylinder.
# Axis    - axis of the cylinder (specify as 'X', 'Y', or 'Z').
# Radius  - radius of the cylinder (scalar).
# Height  - height of the cylidner (from the point specified by Center).
# Units   - specify as 'in', 'mm', 'meter' or anything else defined in HFSS.
#
# Note :
# ------
#
# Example :
# ---------
# fid = fopen('myantenna.vbs', 'wt');
# ...
# hfssCylinder(fid, 'Cyl1', 'Z', [0, 0, 0], 0.1, 10, 'in');
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
def hfssCylinder(fid, Name, Axis, Center, Radius, Height, Units):
    # Cylinder Parameters.
    fid.write('\n')
    fid.write('oEditor.CreateCylinder _\n')
    fid.write('Array("NAME:CylinderParameters", _\n')
    fid.write('"XCenter:=", "{0}{1}", _\n'.format(Center[1], Units))
    fid.write('"YCenter:=", "{0}{1}", _\n'.format(Center[2], Units))
    fid.write('"ZCenter:=", "{0}{1}", _\n'.format(Center[3], Units))
    fid.write('"Radius:=", "{0}{1}", _\n'.format(Radius, Units))
    fid.write('"Height:=", "{0}{1}", _\n'.format(Height, Units))
    fid.write('"WhichAxis:=", "{0}"), _\n'.format(Axis.upper()))

    # Cylinder Properties.
    fid.write('Array("NAME:Attributes", _\n')
    fid.write('"Name:=", "{0}", _\n'.format(Name))
    fid.write('"Flags:=", "", _\n')
    fid.write('"Color:=", "(132 132 193)", _\n')
    fid.write('"Transparency:=", 0, _\n')
    fid.write('"PartCoordinateSystem:=", "Global", _\n')
    fid.write('"MaterialName:=", "vacuum", _\n')
    fid.write('"SolveInside:=", true)\n')
    fid.write('\n')


# ----------------------------------------------------------------------------
# function hfssBox(fid, Name, Start, Size, Units, [Center1], [Radius1], ...
#                  [Axis1], [Center2], [Radius2], [Axis2], ...)
#
# Description :
# -------------
# Create the VB Script necessary to create a Box (or Cuboid) in HFSS. This
# function also provides for optional holes (specified by their Center,
# Radii and Axes) in the box. This feature is useful to allow things like
# vias, cables etc., to penetrate the box without intersection violations.
#
# Parameters :
# ------------
# fid     - file identifier of the HFSS script file.
# Name    - name of the box (appears in HFSS).
# Start   - starting location of the box (specify as [x, y, z]).
# Size    - size of the box (specify as [sx, sy, sz]).
# Units   - units of the box (specify using either 'in', 'mm', 'meter' or
#           anything else defined in HFSS).
# Center  - (Optional) center of the hole to be punched through the box.
#           It can lie anywhere within or on the surface of the box.
# Radius  - (Optional) radius of the hole to be punched through the box.
# Axis    - (Optional) axis of the hole to be punched through the box.
#
# Note :
# ------
# If you happen to specify a hole that lies outside the box, it will have
# no effect. The script will run without interruption.
#
# Example :
# ---------
# fid = fopen('myantenna.vbs', 'wt');
# ...
# # a Box with 2 holes punched thro' it.
# hfssBox(fid, 'FR4_Base', [-bpHeight/2, -baseLength/2, 0], [bpHeight, ...
#         baseLength, -baseThick], 'in', [cX1, cY1, cZ1], R1, 'Z',...
#         [cX2, cY2, cZ2], R2, 'X');
#
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
def hfssBox(fid, Name, Start, Size, Units, varargin):
    # Preamble.
    fid.write('\n');
    fid.write('oEditor.CreateBox _\n');

    # Box Parameters.
    fid.write('Array("NAME:BoxParameters", _\n');
    fid.write('"XPosition:=", "{0}{1}", _\n'.format(Start(1), Units));
    fid.write('"YPosition:=", "{0}{1}", _\n'.format(Start(2), Units));
    fid.write('"ZPosition:=", "{0}{1}", _\n'.format(Start(3), Units));
    fid.write('"XSize:=", "{0}{1}", _\n'.format(Size(1), Units));
    fid.write('"YSize:=", "{0}{1}", _\n'.format(Size(2), Units));
    fid.write('"ZSize:=", "{0}{1}"), _\n'.format(Size(3), Units));

    # Box Attributes.
    fid.write('Array("NAME:Attributes", _\n');
    fid.write('"Name:=", "{0}", _\n'.format(Name));
    fid.write('"Flags:=", "", _\n');
    fid.write('"Color:=", "(132 132 193)", _\n');
    fid.write('"Transparency:=", 0.75, _\n');
    fid.write('"PartCoordinateSystem:=", "Global", _\n');
    fid.write('"MaterialName:=", "vacuum", _\n');
    fid.write('"SolveInside:=", true)\n');

    # Add Holes.
    nHoles = len(varargin) / 3;

    # For each Hole Request create cylinder that satisfies the request and then
    # subtract it from the Box.

    for iH in range(1, nHoles + 1):
        Center = varargin[3 * (iH - 1) + 0]
        Radius = varargin[3 * (iH - 1) + 1]
        Axis = (varargin[3 * (iH - 1) + 2]).upper()

        if Axis == 'X':
            Center[0] = Start[0]
            Length = Size[0]
        elif Axis == 'Y':
            Center[1] = Start[1]
            Length = Size[1]
        elif Axis == 'Z':
            Center[2] = Start[2]
            Length = Size[2]

        hfssCylinder(fid, Name + '_subhole' + str(iH), Axis, Center, Radius, Length, Units)
        hfssSubtract(fid, Name, Name + '_subhole' + str(iH))


# ----------------------------------------------------------------------------
# function hfssRectangle(fid, Name, Axis, Start, Width, Height, Units)
#
# Description :
# -------------
# Create the VB Script necessary to construct a rectangle using the HFSS
# 3D Modeler.
#
# Parameters :
# ------------
# fid     - file identifier of the HFSS script file.
# Name    - name of the rectangle object (appears in the HFSS objects tree).
# Axis    - axis that is normal to the rectangle object.
# Start   - starting location of the rectangle (one of its corners). Specify
#           as [sx, sy, sz].
# Width   - (scalar) the width of the rectangle. If the axis is 'X' then this
#           represents the Y-axis size of the rectangle, and so on.
# Height  - (scalar) the height of the rectangle. If the axis is 'X', then
#           this represents the Z-axis size of the rectangle, and so on.
# Units   - specify as 'in', 'meter', 'mm', ... or anything else defined in
#           HFSS.
#
# Note :
# ------
# Todo: a feature to add automatic holes in the rectangle object.
#
# Example :
# ---------
# fid = fopen('myantenna.vbs', 'wt');
# ...
# # in this example, Y-axis size is 10in and Z-axis size is 20in.
# hfssRectangle(fid, 'Rect1', 'X', [0,0,0], 10, 20, 'in');
#
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
# Width and Height follow the right-hand rule. If the Axis is Z, then Width
# represents X-direction size and Height represents the Y-direction size
# and so on ...
def hfssRectangle(fid, Name, Axis, Start, Width, Height, Units):
    Transparency = 0.75;

    # Preamble.
    fid.write('\n')
    fid.write('oEditor.CreateRectangle _\n')

    # Rectangle Parameters.
    fid.write('Array("NAME:RectangleParameters", _\n')
    fid.write('"IsCovered:=", true, _\n')
    fid.write('"XStart:=", "{0}{1}", _\n'.format(Start(0), Units))
    fid.write('"YStart:=", "{0}{1}", _\n'.format(Start(1), Units))
    fid.write('"ZStart:=", "{0}{1}", _\n'.format(Start(2), Units))

    fid.write('"Width:=", "{0}{1}", _\n'.format(Width, Units))
    fid.write('"Height:=", "{0}{1}", _\n'.format(Height, Units))

    fid.write('"WhichAxis:=", "{0}"), _\n'.format(Axis.upper()))

    # Rectangle Attributes.
    fid.write('Array("NAME:Attributes", _\n')
    fid.write('"Name:=", "{0}", _\n'.format(Name))
    fid.write('"Flags:=", "", _\n')
    fid.write('"Color:=", "(132 132 193)", _\n')
    fid.write('"Transparency:=", {0}, _\n'.format(Transparency))
    fid.write('"PartCoordinateSystem:=", "Global", _\n')
    fid.write('"MaterialName:=", "vacuum", _\n')
    fid.write('"SolveInside:=", true)\n')


# ----------------------------------------------------------------------------
# hfssSubtract(fid, blankParts, toolParts)
#
# Description:
# ------------
# Creates the necessary VB script to subtract a set of tool parts from a set
# of blank parts, a.k.a., will produce blank parts - tool parts.
#
# Parameters :
# ------------
# fid        - file identifier of the HFSS script file.
# blankParts - a cell array of strings that contain the blank parts.
# toolParts  - a cell array of strings that contain the tool parts.
#
# Example :
# ---------
# fid = fopen('myantenna.vbs', 'wt');
# ...
# hfssSubtract(fid, {'BigPlate'}, {'SmallPlate'});
#
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

# ----------------------------------------------------------------------------
# CHANGELOG
#
# ??-????-2014: *Initial release (VR).
# 07-Augu-2014: *Added option to clone parts (DRP).
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Modified by Daniel Rodriguez Prado
# danysan@gmail.com / drprado@tsc.uniovi.es
# 07 August 2014
# ----------------------------------------------------------------------------

# Will result in blankParts - toolParts.
def hfssSubtract(fid, blankParts, toolParts, Clone='false'):
    # Preamble.
    fid.write('\n')
    fid.write('oEditor.Subtract _\n')
    fid.write('Array("NAME:Selections", _\n')

    # Add the Blank Parts.
    fid.write('"Blank Parts:=", _\n')
    if (len(blankParts) != 0):
        nBlank = len(blankParts)
        fid.write('"')

        for iB in range(0, nBlank - 1):
            fid.write('{0},'.format(blankParts[iB]))
        fid.write('{0}", _\n'.format(blankParts[nBlank - 1]))
    else:
        fid.write('"{0}", _\n'.format(blankParts))  ## !!!

    # Add the Tool Parts.
    fid.write('"Tool Parts:=", _\n')
    if (len(toolParts) != 0):
        nTool = len(toolParts)
        fid.write('"')
        for iB in range(0, nTool - 1):
            fid.write('{0},'.format(toolParts[iB]))
        fid.write('{0}"), _\n'.format(toolParts[nTool - 1]))
    else:
        fid.write('"{0}"), _\n'.format(toolParts))

    # Post-Amble.
    fid.write('Array("NAME:SubtractParameters", _\n')
    fid.write('"KeepOriginals:=", {0} \n'.format(Clone))
