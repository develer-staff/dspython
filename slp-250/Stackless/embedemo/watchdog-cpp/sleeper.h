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
 * @file sleeper.h
 * @date Created: 2006/03/27  [18:40]
 * @author File creator: Juho "Garo" Mäkinen
 * @author Credits: Juho "Garo" Mäkinen
 */

#ifdef XENOCIDE_PRAGMA_ONCE
#pragma once
#endif // XENOCIDE_PRAGMA_ONCE

#ifndef xenocide__snake__sleeper_h
#define xenocide__snake__sleeper_h

#include <boost/smart_ptr.hpp>
#include <boost/python.hpp>
#include <stackless_api.h>

class Sleeper;
typedef boost::shared_ptr<Sleeper> SleeperPtr;

//==========================================================================
//  Sleeper class declaration
//==========================================================================
/** @brief
 */
class Sleeper
{
 private:
  
 protected:
  int resumeTime;
  
  boost::python::object channel;
  
 public:
  
  
  class Comparator
    {
    public:
      bool operator()(const SleeperPtr& a, const SleeperPtr& b)
	{
	  return a->resumeTime < b->resumeTime;
	}
    };
  
  /** @brief Default constructor.
   */
  Sleeper(int resumeTime);
  
  /** @brief Default destructor.
   */
  ~Sleeper();
  
  bool operator< (const Sleeper& sleeper)
  {
    return resumeTime < sleeper.resumeTime;
  }
  
  /** \brief Returns Borrowed Reference for channel
   */
  PyChannelObject* getBorrowedChannel()
  {
    return reinterpret_cast<PyChannelObject*>(channel.ptr());
  }
  
  /** \brief Returns channel which is used to wake this sleeper
   */
  boost::python::object getChannel()
  {
    return channel;
  }
  
  /** \brief Returns resumeTime
   */
  int getResumeTime()
  {
    return resumeTime;
  }
};


#endif // xenocide__snake__sleeper_h
