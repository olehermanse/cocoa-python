# Example of using ctypes with Cocoa to create an NSWindow with
# an application menu item for quitting.

import sys
from cocoapy import *

NSWindow = ObjCClass('NSWindow')
NSApplication = ObjCClass('NSApplication')
NSMenu = ObjCClass('NSMenu')
NSMenuItem = ObjCClass('NSMenuItem')
NSAutoreleasePool = ObjCClass('NSAutoreleasePool')

class MyWindow_Implementation(object):
    MyWindow = ObjCSubclass('NSWindow', 'MyWindow')

    @MyWindow.method(b'@'+NSUIntegerEncoding+b'@@B')
    def nextEventMatchingMask_untilDate_inMode_dequeue_(self, mask, date, mode, dequeue):

        print(f"nextEventMatchingMask({mask}, {date}, {mode}, {dequeue})")

        event = send_super(self, 'nextEventMatchingMask:untilDate:inMode:dequeue:',
                           mask, date, mode, dequeue, argtypes=[c_uint, c_void_p, c_void_p, c_bool])
        print("send_super returned")

        if event.value is None:
            ret = 0
        else:
            ret = event.value
        print("return value: " + str(ret))
        return ret

MyWindow = ObjCClass('MyWindow')

def create_window():
    print('creating window')
    frame = NSMakeRect(100, 100, 300, 300)
    window = MyWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        frame,
        NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask,
        NSBackingStoreBuffered,
        0)
    window.setTitle_(get_NSString("My Awesome Window"))
    window.makeKeyAndOrderFront_(None)
    return window

def create_autorelease_pool():
    pool = NSAutoreleasePool.alloc().init()
    return pool

def application_run():
    app = NSApplication.sharedApplication()
    create_autorelease_pool()
    create_window()
    app.run()  # never returns

######################################################################

if __name__ == '__main__':
    application_run()
