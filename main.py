
import threading
import highway
import multilane
import settings
import ui
import time
import random

# 8 -- 518, 518, 518, 518, 518, 136, 163, 111
def main():
    settings.init()
    random.seed(time.time ())
    # print settings.UI_BASEMAP[1][250]
    GUI = ui.UI()

    # run(GUI)
    painterThread = threading.Thread(target=GUI.processMessage)
    painterThread.setDaemon(True)
    painterThread.start()
    # GUI.processMessage()

    GUI.mainloop()
    # test_run()

if __name__ == '__main__':
    main()


# hwy = MultiLane.MultiLane(5, 8, 0.6)
#
# print len(hwy.lanes)
