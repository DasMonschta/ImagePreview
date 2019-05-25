from ts3plugin import ts3plugin
import ts3defines
import ts3lib as ts3
from PythonQt.QtCore import Qt, QTimer
from PythonQt.QtGui import QLabel, QPixmap
import urllib.request
from pytson import getCurrentApiVersion

class ImageInChat(ts3plugin):
    name            = "Image Preview"
    requestAutoload = False
    version         = "1.0"
    try: apiVersion = getCurrentApiVersion()
    except: apiVersion = 21
    author          = "Luemmel"
    description     = "Creates previews for image urls."
    offersConfigure = False
    commandKeyword  = ""
    infoTitle       = None
    hotkeys         = []
    menuItems       = [(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 0, "Contact Manager Settings", "")]
    
    status          = True
    showTime        = 5000
    imageMaxHeight  = 200
    contenttypes    = ["image/jpeg", "image/png", "image/gif"]
    
    def getWidgetByObjectName(self, name):
        QApp = QApplication.instance()
        widgets = QApp.topLevelWidgets()
        widgets = widgets + QApp.allWidgets()
        for x in widgets:
            if str(x.objectName) == name: return x
            
    def onTextMessageEvent(self, schid, targetMode, toID, fromID, fromName, fromUniqueIdentifier, message, ffIgnored):
        if self.status:
            (error, myid) = ts3.getClientID(schid)
            
            # get plain url from bbcode url
            # https://github.com/DerLuemmel/pyTSon_ts3_linkinfo/blob/master/__init__.py
            message = message.lower()
            if not myid == fromID and ("[url]" in message or "[url=" in message):
                start = message.find("[url]")
                if not start == -1:                   
                    end = message.find("[/url]")
                    message = message[start + 5:end]
                else:
                    start = message.find("[url=")
                    end = message.find("]")
                    message = message[start + 5:end]

                # Open stream and read content type
                stream = urllib.request.urlopen(message)
                contenttype = stream.info().get_content_type()                

                # if contenttype is png, gif, jpeg
                if contenttype in self.contenttypes:
                    
                    # get image data
                    data = stream.read()
                    
                    # label and pixmap
                    image = QLabel("image")   
                    pixmap = QPixmap()
                    
                    # load url data to pixmap
                    pixmap.loadFromData(data)      

                    # set max width to self.imageMaxHeight
                    pixmap = pixmap.scaledToHeight(self.imageMaxHeight, Qt.FastTransformation)
                    
                    # set image to label
                    image.setPixmap(pixmap)  
                    
                    # set margins for better looking
                    image.setStyleSheet("QLabel{margin: 10px;}")
                    
                    # Get chatlayout
                    chatlayout = self.getWidgetByObjectName("MainWindowChatWidget").layout()
                    
                    # Add image to chatlayout
                    chatlayout.addWidget(image)
                    
                    # Deletes image label after self.showTime
                    QTimer.singleShot(self.showTime, lambda : self.removeImage(chatlayout, image)) 

    def removeImage(self, chatlayout, image):    
        chatlayout.removeWidget(image)
        image.deleteLater()
        
    def __init__(self):    
        pass
        
    def stop(self):
        pass
        