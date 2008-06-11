"""
----------------------------------------------------------------------------

OpenSteer -- Steering Behaviors for Autonomous Characters

Copyright (c) 2002-2003, Sony Computer Entertainment America
Original author: Craig Reynolds <craig_reynolds@playstation.sony.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.


----------------------------------------------------------------------------

PyOpenSteer -- Port of OpenSteer to Python

Copyright (c) 2004 Lutz Paelike <lutz@fxcenter.de>

The license follows the original Opensteer license but must include 
this additional copyright notice.
----------------------------------------------------------------------------
"""

from vector import vec3

gBlack = vec3(0, 0, 0)
gWhite = vec3(1, 1, 1)

gRed     = vec3(1, 0, 0)
gYellow  = vec3(1, 1, 0)
gGreen   = vec3(0, 1, 0)
gCyan    = vec3(0, 1, 1)
gBlue    = vec3(0, 0, 1)
gMagenta = vec3(1, 0, 1)

gOrange = vec3(1, 0.5, 0)

gGray10 = vec3(0.1)
gGray20 = vec3(0.2)
gGray30 = vec3(0.3)
gGray40 = vec3(0.4)
gGray50 = vec3(0.5)
gGray60 = vec3(0.6)
gGray70 = vec3(0.7)
gGray80 = vec3(0.8)
gGray90 = vec3(0.9)
