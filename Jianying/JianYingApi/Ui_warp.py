"""
    Ui Warpper For JianYing

"""
import uiautomation as api32
import pyautogui as auto


def _radio_detect(x:int,y:int,max_retry_times:int=20):
    # Pixel Comparision 
    # Position (left + 8 , top + 8 )
    # (0, 193, 205) For On, return 1
    # (80, 80, 87)  For Off, return 0
    # (54, 54, 57)  For Disabled, return -1
    def diff(a:tuple,b:tuple,toler:int=0):
        # Compare Two  Tuples Different
        for i in zip(a,b):
            if abs(i[0]-i[1])>toler:return False
        return True
    im = auto.screenshot()
    rgb = im.getpixel((x,y))
    if diff(rgb,(0, 193, 205),toler=10) == True : return 1
    if diff(rgb,(80, 80, 87),toler=10) == True : return 0
    if diff(rgb,(54, 54, 57),toler=10) == True : return -1
    if diff(rgb,(27, 27, 28),toler=10) == True : return _radio_detect(x=x+1,y=y+1,max_retry_times=max_retry_times)
    # Attempt Using A Higher Resolution

def _search_include(windowObj:api32.Control,controlType:api32.Control,ClassName:str=None,Name:str=None)->api32.Control:
    """
        Return the control object where name / classname include certain string .
    """
    if ClassName == "" and Name == "": return -2
    for i in windowObj.GetChildren():
        _j , _k = False , False
        if ClassName is not None: _j = ClassName in i.ClassName
        if Name is not None: _k = Name in i.Name
        if _j or _k:
            if i.ControlTypeName == controlType.__name__:  return i
    return None

class Explorer_Files:
    # Some Actions About Explorer
    def __init__(self,File_Bar:api32.WindowControl) -> None:
        assert File_Bar.ClassName == "#32770" , "Not In Proper File Bar"
        self.FBar = File_Bar

    def _File_Posi(self)->tuple:
        """
            Return File Name & Floder Name Text Lable Position ( Center )
        """
        _p = self.FBar.ComboBoxControl(searchDepth=2,ClassName="ComboBox")
        if _p.Exists(maxSearchSeconds=0.1) == False: _p = self.FBar.EditControl(searchDepth=1)
        return  (_p.BoundingRectangle.xcenter(),_p.BoundingRectangle.ycenter())

    def _type_in(self,path:str,running_type:str,name:str=""):
        """running_type: media_add / export_select"""
        auto.hotkey("Alt","D") # Select Path Bar
        api32.SendKeys(path) # Type in path
        auto.press("Enter")
        if name!="":
            api32.Click(self._File_Posi()[0],self._File_Posi()[1])
            api32.SendKeys(name)
        _e = self.FBar.PaneControl(searchDepth=2,ClassName="DUIViewWndClassName").BoundingRectangle
        api32.Click(_e.right-10,_e.bottom-10,waitTime=0.5) # click the margin to avoid add the whole dict (occured in Version 3.3.5 Beta1)
        if running_type == "media_add": auto.press("Enter")
        elif running_type == "export_select" : self.FBar.ButtonControl(searchDepth=1,Name="选择文件夹").Click()