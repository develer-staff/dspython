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
 * @file Sync.h
 * @date Created: 2006/03/22  [20:01]
 * @author File creator: Juho "Garo" Mäkinen
 * @author Credits: Juho "Garo" Mäkinen
 */

#ifdef XENOCIDE_PRAGMA_ONCE
#pragma once
#endif // XENOCIDE_PRAGMA_ONCE

#ifndef xenocide__snake__Sync_h
#define xenocide__snake__Sync_h


#include <boost/python.hpp>
#include <list>
#include <set> // for std::multiset

#include "sleeper.h"


//==========================================================================
//  Sync class declaration
//==========================================================================
/** @brief
 */
class Sync
{
 public:
  typedef std::multiset<SleeperPtr, Sleeper::Comparator> SleepersSet;    
  static SleepersSet realtimeSleepersSet;
 protected:
  
  /** \brief List of python values for returning unittest results from python code.
   */
  typedef std::list<boost::python::object> TestResultValues;
  static TestResultValues testResultValues;
  
  
  
 public:
  /** @brief Default constructor.
   */
  Sync();
  
  /** @brief Default destructor.
   */
  ~Sync();
  
  static void beNice();
  
  /** \brief Sleeps for msec (1/1000 of a second).
   *
   * Can only be called from a tasklet, but not from main tasklet.
   */
  static void sleepReal(int msec);
  
  static void addRealtimeSleeper(SleeperPtr sleeper);
  
  
  static void pushTestResult(boost::python::object value);
  
  static boost::python::object popTestResult();
  
  static void clearTestResults();
  
  
  static boost::python::object niceChannel;
};


#endif // xenocide__snake__Sync_h
