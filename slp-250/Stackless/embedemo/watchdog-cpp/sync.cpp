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
 * @file Sync.cpp
 * @date Created: 2006/03/22  [20:01]
 * @author File creator: Juho "Garo" Mäkinen
 * @author Credits: Juho "Garo" Mäkinen
 */

////////////////////////////////////////////////////////////////////////////////
//  Headers
////////////////////////////////////////////////////////////////////////////////

#include "sync.h"

#include <stackless_api.h>

using namespace std;

Sync::TestResultValues Sync::testResultValues;
boost::python::object Sync::niceChannel;

Sync::SleepersSet Sync::realtimeSleepersSet;

//==========================================================================
//  Sync class implementation
//==========================================================================
Sync::Sync()
{
}

//--------------------------------------------------------------------------
Sync::~Sync()
{
}

//--------------------------------------------------------------------------
void Sync::beNice()
{
  PyChannel_Receive(reinterpret_cast<PyChannelObject*>(niceChannel.ptr()));
}

//--------------------------------------------------------------------------
// Method exported to python. This is used to put the calling tasklet
// into sleep for msec time. In this test program, it does not
// sleep msec (1/1000 of second), because correct currentTime
// is not fetched from system clock.
//
void Sync::sleepReal(int msec)
{
  namespace py = boost::python;
  
  py::handle<> handle(PyStackless_GetCurrent());
  py::object currentTasklet(handle);
  
  if (PyTasklet_IsMain(reinterpret_cast<PyTaskletObject*>(currentTasklet.ptr())) == 1)
  {
    throw string("sleepReal called for main tasklet");
  }
  
  // FIXME: currentTime should contain current time in microseconds.
  // But as we are just demonstrating how the sleepReal is used,
  // this doesn't matter.
  int currentTime = 0;
  int resumeTime = currentTime + msec;
  
  SleeperPtr sleeper(new Sleeper(resumeTime));
  addRealtimeSleeper(sleeper);
  
  // The name is just a gcc fix - it's an anonymous handle
  py::handle<> anon(PyChannel_Receive(sleeper->getBorrowedChannel()));
  
}

void Sync::addRealtimeSleeper(SleeperPtr sleeper)
{
  realtimeSleepersSet.insert(sleeper);
}

//--------------------------------------------------------------------------
// Push a python value (a test result) to the test result stack.
// In practice, this is called from tasklets and the results
// are then examined at main tasklet, or when the main tasklet
// has exited using the popTestResult method.
void Sync::pushTestResult(boost::python::object value)
{
  testResultValues.push_back(value);
}

//--------------------------------------------------------------------------
// This method is used to retrieve the stored test results from the
// test result stack. In practice, this is used to implement test cases
// in TDD (Test Driven Development)
boost::python::object Sync::popTestResult()
{
  // FIXME: Make this throw nicelly formed exception incase the list is empty
  boost::python::object value = (*testResultValues.begin());
  testResultValues.pop_front();
  return value;
  
}

//--------------------------------------------------------------------------
void Sync::clearTestResults()
{
  testResultValues.clear();
}



