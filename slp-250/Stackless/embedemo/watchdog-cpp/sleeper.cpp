/*
--------------------------------------------------------------------------------
This source file is part of Xenocide
  by  Project Xenocide Team

For the latest info on Xenocide, see http://www.projectxenocide.com/

This work is licensed under the Creative Commons
Attribution-NonCommercial-ShareAlike 2.5 License.

To view a copy of this license, visit
http://creativecommons.org/licenses/by-nc-sa/2.5/
or send a letter to Creative Commons, 543 Howard Street, 5th Floor,
San Francisco, California, 94105, USA.
--------------------------------------------------------------------------------
*/

/**
 * @file sleeper.cpp
 * @date Created: 2006/03/27  [18:40]
 * @author File creator: Juho "Garo" Mäkinen
 * @author Credits: Juho "Garo" Mäkinen
 */

#include "sleeper.h"

//==========================================================================
//  Sleeper class implementation
//==========================================================================
Sleeper::Sleeper(int resumeTime)
{
  
  PyChannelObject* rawChannel = PyChannel_New(NULL);
  PyChannel_SetPreference(rawChannel, 0);
  
  channel = boost::python::object(boost::python::handle<>(reinterpret_cast<PyObject*>(rawChannel)));
  
  this->resumeTime = resumeTime;
}

//--------------------------------------------------------------------------
Sleeper::~Sleeper()
{
}


