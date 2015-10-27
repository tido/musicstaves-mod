# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

#----------------------------------------------------------------

#
# Copyright (C) 2015 Christoph Dalitz
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

#----------------------------------------------------------------

from gamera.core import *
from gamera.core import Point as CorePoint

from gamera.toolkits.musicstaves.plugins import *

from gamera.args import *
from gamera.args import Point as ArgsPoint

from gamera.toolkits.musicstaves.stafffinder \
     import StaffFinder as _virtual_StaffFinder

from gamera.toolkits.musicstaves.stafffinder import StafflineSkeleton

#----------------------------------------------------------------

class StaffFinder_stable_path(_virtual_StaffFinder):
    
    """Finds staff lines with by the stable path algorithm, as described in
    Cardoso, J., A. Capela, A. Rebelo, C. Guedes, and I. Porto (2008):
    A connected path approach for staff detection on a music score.
    15th IEEE International Conference on Image Processing, pp. 1005-8.

:Authors: Ian Karp (algorithm) and Christoph Dalitz (wrapper class)
"""

    #------------------------------------------------------------

    def __init__(self, img, \
                 staffline_height = 0, \
                 staffspace_height = 0):
        
        _virtual_StaffFinder.__init__(self, img, \
                                      staffline_height, \
                                      staffspace_height)
        
        self.find_staves_args = Args([Bool('with_trimming', default = True), \
                                      Bool('with_deletion', default = False), \
                                      Bool('with_staff_fixing', default = False), \
                                      Bool('enable_strong_staff_pixels', default = False)])

    #------------------------------------------------------------
    def find_staves(self, with_trimming=True, with_deletion=True, \
                        with_staff_fixing=True, \
                        enable_strong_staff_pixels=False):
        """Method for finding the staff lines.

Signature:

  ``find_staves(with_trimming=True, with_deletion=True, with_staff_fixing=True, enable_strong_staff_pixels=False)``

with

- *with_trimming*:
  Trims staff sets where white space or ornamentations are found.
        
- *with_deletion*:
  If true, the image will be processed once and will create an image comprised of only found staves and then the code is run again. More accurate for images with a lot of lyrics or ornamentation.
        
- *with_staff_fixing*:
  Uses the slopes of staff sets to fix staff lines that differ wildly from the slope at specific intervals.
        
- *enable_strong_staff_pixels*:
  Experimental method that reduces the weights of vertical runs that are the exact width of staffline_height and are exactly staffspace_height away from the closest black pixel.

This method fills the *self.linelist* attribute for further
processing.
"""

        # Get the skeleton list
        skeleton_list = self.image.get_stable_path_staff_skeletons( \
            with_trimming=with_trimming, \
            with_staff_fixing=with_staff_fixing, \
            enable_strong_staff_pixels=enable_strong_staff_pixels, \
            staffline_height=self.staffline_height, \
            staffspace_height=self.staffspace_height)

        # copy over to stafflist
        self.linelist = []

        print len(skeleton_list)
        for g in skeleton_list:
            newstaff = []
            for s in g:
                skel = StafflineSkeleton()
                skel.left_x = s[0]
                skel.y_list = s[1]
                newstaff.append(skel)
            self.linelist.append(newstaff)
        

