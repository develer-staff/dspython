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
 * @file main.cpp
 * @date Created: 2006/04/04  [12:06]
 * @author File creator: Juho "Garo" Mäkinen
 * @author Credits: Juho "Garo" Mäkinen
 */


/*
 * WELCOME dear Stackless python programmer.
 *
 * This example is based on the ideas from EVE presentation, held
 * at US PyCon 2006 and presented by CCP games. If you haven't yet read
 * the powerpoint, please go and read it, so you understant what are
 * the features I'm demoing you here.
 * http://www.stackless.com/Members/rmtew/News%20Archive/newsPyCon2006Pres
 *
 * Quick disclaimer:
 * This code is a stripped down from Project Xenocide svn repository
 * to contain only the most important parts. Because of that I needed to
 * truncate some classes, move a few methods, created a few globals
 * and drop a huge amount of code (like unittesting framework, log4cxx etc)
 * which we use, but are not needed here. That's why the code is a bit mess. ;)
 * If you are interested, the full Project Xenocide source is available
 * at www.projectxenocide.com
 *
 *
 * The basic workflow of this example is the following:
 *  1) Initialize python
 *  2) Export class Sync and method stacklessMain to python using boost.python
 *  3) Run a simple test to verify that python is working.
 *  4) Start the staclessMain, which is a C++ method, as the "main tasklet" into
 *     stackless context.
 *  5) Execute a few tests which demonstrate the beNice, Watchdog and Sleeper features.
 *
 * A word about the tests:
 * We use TDD (Test Driven Development) with project xenocide and we have found it usefull.
 * The features of this demo are all presented as simple tests. The Sync class has
 * a handy method, Sync::pushTestResult(py::object), which takes a python object, which
 * can be anything (number, string etc). Once the test case is completed, the results
 * are checked that they match what they are supposed to be. If you don't know
 * what TDD is, I'd suggest that you go and read some documentation (from Wikipedia,
 * for example)
 *
 * Notice that both popTestResult and py::extract can throw an error if they fail,
 * and these errors are not catched at this demo. Anyway, if everything is right,
 * they wont throw anything and the tests are executed as they should.
 *
 * TEST 1: Just verify that the pushTestResult, boost::python and python itself are working.
 * It simply pushes number 42 as a test result and then it reads it and asserts that it really
 * is the number 42.
 *
 * TEST 2: Create a tasklet, which calls beNice four times.
 *
 * TEST 3: Tests the watchdog feature. The idea is, that every running tasklet
 * should call beNice as soon as possible. Once every tasklet has called beNice,
 * the watchdog exists and returns Py_None. With game programming, for example
 * in our Project Xenocide, the method containing the watchdog loop is called
 * once every frame. So if a tasklet takes too much time without calling beNice,
 * the FPS rate slows down and this is bad.
 *
 * And this is the idea of the watchdog. If one process (a tasklet) goes wild,
 * and, for example, goes into while 1: -loop, the watchdog hits the execution limit
 * (which sould normally be much larger than the current 1000 executions in this demo)
 * and the watchdog method exists returning the tasklet object which took too much time.
 * This can be then used for stacktrace, debugging etc.
 *
 * So this test creates a tasklet running while 1 -loop and waits that the watchdog hits the limit.
 *
 * TEST 4: This tests the Sleeper system. Sync.sleepReal() is used to put the calling
 * tasklet into sleep so, that it doesn't use any processor time. It does not sleep
 * actually the specified amount of time, but it could very easily be modified to do
 * actual sleeping.
 *
 * This test creates five tasklets, which each sleeps for a different amount of time.
 * The system, which handles the sleeping, must wake the sleepers only when
 * the specified amount of time has passed, so this test verifies that the tasklets
 * are awaken in correct time (or actually in the correct order)
 *
 * If you have any guestions, please email to stackless mailing list (stackless@stackless.com),
 * or contact me (Juho "Garo" Makinen) at #xenocide IRC channel, located at freenode.net irc
 * network, or mailing me directly to juho.makinen@gmail.com
 *
 * - Juho Makinen, http://www.juhonkoti.net, 2006-04-04
 *
 */


#include <boost/python.hpp>
#include <iostream>

#include "sync.h"
#include "sleeper.h"

using namespace std;
namespace py = boost::python;

// Stackless ticker. This takes care of re-scheduling
// tasklets which have called beNice (every tasklet should call beNice)
// and running the watchdog.
void stacklessTick()
{
  using namespace boost::python;

  // Normally call wakeupSleepers here, but as we are only demonstrating
  // how the sleepers system works, we call it manually from stacklessMain
  // during the sleeper test case.

  // Run the reScheduler, which will load the taskler running queue
  try
  {

    int balance = extract<int>(Sync::niceChannel.attr("balance"));

    PyChannelObject *channel = reinterpret_cast<PyChannelObject*>(Sync::niceChannel.ptr());

    for (int i = balance; i < 0; i++)
    {
      PyChannel_Send(channel, Py_None);
    }

  }
  catch (boost::python::error_already_set&)
  {
    std::cerr << "reShedule error" << std::endl;
    PyErr_Print();
    PyErr_Clear();
  }


  // Run all pending tasklets until they call themselfs nice
  handle<> watchdogHandle;
  do
  {
    try
    {
      watchdogHandle = handle<>(allow_null(PyStackless_RunWatchdog(1000)));

      py::object obj(watchdogHandle);
      if (obj.ptr() != Py_None)
      {
	// handle stacklet which has been running too long
	cerr << "Watchdog interrupted a tasklet which was running too long without calling beNice" << endl;

	int retval = PyTasklet_Kill(reinterpret_cast<PyTaskletObject*>(obj.ptr()));
	cerr << "Killing this tasklet, retval: " << retval << " (expecting 0)" << endl;
      }
    }
    catch (error_already_set&)
    {
      std::cerr << "Got error from a tasklet process" << std::endl;
      PyErr_Print();
      PyErr_Clear();
    }

  }
  while (!watchdogHandle);

}

// This method is used to wake up the sleepers.
// Parameters:
//   currentTime: This is a variable which holds number of "time units"
//                passed from the beginning of the program.
//
//   sleepers:    This is a SleepersSet which contains the sleepers
//                which are sleeping. If a sleepers getResumeTime()
//                is greater than currentTime, then the sleeper must
//                be awaken.
//
// The program might have multiple SleepersSets, one for real time
// sleepers and another for "game time" sleepers and this function
// can be used for both of them by supplying different arguments.
//
// Normally you would call this from stacklessTick method,
// but here we call this from stacklessMain when we test and demostrate
// how this is used.
int wakeUpSleepers(int currentTime, Sync::SleepersSet& sleepers)
{
  Sync::SleepersSet::iterator begin = sleepers.begin();
  Sync::SleepersSet::iterator end = sleepers.end();

  if (begin == end)
    return 0;

  if ((*begin)->getResumeTime() > currentTime)
    // There are no sleepers to be resumed
    return 0;

  Sync::SleepersSet::iterator pos = begin;
  Sync::SleepersSet::iterator next;

  int count = 0;
  while (1)
  {
    SleeperPtr sleeper = *pos;
    next = pos;
    next++;

    sleepers.erase(pos);
    pos = next;

    py::object none;
    PyChannel_Send(sleeper->getBorrowedChannel(), none.ptr());
    count++;

    if (next == end)
      break;

    if ((*next)->getResumeTime() <= currentTime)
      break;

  }


  return count;
}



void stacklessMain()
{

  // TEST 2
  //
  // Test the beNice implementation.
  // Notice that this function is actually the main tasklet,
  // so we first define a function, then we start this function as
  // another tasklet, which calls beNice once a while.
  string code =
    "def func2():\n"
    "  c = 0\n"
    "  for i in xrange(4):\n"
    "    c += 1\n"
    "    print \"from stacklessMain: c is: \" + str(c)\n"
    "    Sync.beNice()\n"
    "  Sync.pushTestResult(c)\n"
    "stackless.tasklet(func2)()\n";

  PyRun_SimpleString(code.c_str());

  for (int i = 0; i < 5; i++)
  {
    // Execute the stackless ticker. This is what you would call
    // once on every frame of a game, for example.
    stacklessTick();
  }

  // correct value for c is 4
  int retval = py::extract<int>(Sync::popTestResult());
  cout << "Checking that c is actually four: c == " << retval << endl;
  assert(retval == 4);

  // TEST 3
  //
  // Test the watchdog.
  code =
    "def func3():\n"
    "  c = 0\n"
    "  while 1:\n"
    "    c += 1\n"
    "    pass\n"
    "stackless.tasklet(func3)()\n";

  PyRun_SimpleString(code.c_str());

  // Execute the stackless ticker. As our func3() behaves badly,
  // and doesn't call Sync.beNice(), the Watchdog should interrupt
  // the execution.
  stacklessTick();


  // TEST 4
  //
  // Test the sleep implementation
  // Notice that this implementation doesn't use real clock times,
  // but we only simulate this by adding 250 "time units"
  // on each ticker loop.


  code =
    "def func4(time):\n"
    "  Sync.sleepReal(time)\n"        // sleep for time amounts of "time units", supplied as argument
    "  Sync.pushTestResult(time)\n"   // Push the sleeped time to the test result stack
    "  print \"I'm awake, I slept for \" + str(time) + \" time units\"\n"
    "stackless.tasklet(func4)(500)\n" // Create tasklet which sleeps for 500 "time units"
    "stackless.tasklet(func4)(2000)\n"
    "stackless.tasklet(func4)(1000)\n"
    "stackless.tasklet(func4)(1000)\n"
    "stackless.tasklet(func4)(250)\n";


  PyRun_SimpleString(code.c_str());

  // We simulate the time by having "current time" variable, which is incremented on every loop iteration
  int currentTime = 0;
  for (int i = 0; i < 10; i++)
  {
    wakeUpSleepers(currentTime, Sync::realtimeSleepersSet);
    stacklessTick();
    currentTime += 250;
  }

  // Verify that the sleepers were awaken in the right order.
  assert(static_cast<int>(py::extract<int>(Sync::popTestResult())) == 250);
  assert(static_cast<int>(py::extract<int>(Sync::popTestResult())) == 500);
  assert(static_cast<int>(py::extract<int>(Sync::popTestResult())) == 1000);
  assert(static_cast<int>(py::extract<int>(Sync::popTestResult())) == 1000);
  assert(static_cast<int>(py::extract<int>(Sync::popTestResult())) == 2000);
}


int main (int argc, char** argv)
{

  // Initialize Python
  Py_SetProgramName(argv[0]);
  Py_InitializeEx(0);

  if (!Py_IsInitialized())
  {
    cerr << "Python initialization failed" << endl;
    return -1;
  }


  PySys_SetArgv(argc, argv);

  // setup the niceChannel object
  Sync::niceChannel = py::object(py::handle<>(reinterpret_cast<PyObject *>(PyChannel_New(NULL))));
  PyChannel_SetPreference(reinterpret_cast<PyChannelObject *>(Sync::niceChannel.ptr()), 0);

  PyRun_SimpleString("import stackless\n"
		     "stackless.getcurrent().block_trap = True");

  py::handle<> mainHandle(py::borrowed(PyImport_AddModule("__main__")));
  py::object mainModule(mainHandle);

  py::scope mainScope(mainModule);


  py::object class_Sync = py::class_<Sync, boost::noncopyable>("Sync")
    .def("beNice", &Sync::beNice)
    .staticmethod("beNice")
    .def("sleepReal", &Sync::sleepReal)
    .staticmethod("sleepReal")
    .def("pushTestResult", &Sync::pushTestResult)
    .staticmethod("pushTestResult")
    ;

  py::def("stacklessMain", &stacklessMain);

  //
  // TEST 1: Verify that python is initialized and it's working
  //
  // Run simple test to verify that everything is running fine
  PyRun_SimpleString("Sync.pushTestResult(42)");

  int retval = py::extract<int>(Sync::popTestResult());
  cout << "Checking that we could execute a python code. retval == " << retval << " (expected 42)" << endl;
  assert(retval == 42);


  // Start the stacklessMain method inside stackless context
  // This function call will block until the stacklessMain method is done
  PyStackless_CallMethod_Main(mainModule.ptr(), "stacklessMain", 0);

  Py_Finalize();

}
