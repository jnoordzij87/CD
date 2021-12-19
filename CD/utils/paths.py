from enum import Enum

class Programs(Enum):
    Client = 1
    WebService = 2

class Versions(Enum):
    Release = 1
    PreRelease = 2

class Folders(Enum):
    UpdateFolder = 1
    LiveFolder = 2

class Environments(Enum):
    HbR = 1
    Stek = 2
    Monumentenwacht = 3
    DemoSecureRelease = 4
    DemoSecurePreRelease = 5
    DemoDemoRelease = 6
    DemoDemoPreRelease = 7
    BIMSpeed = 8
    Sandbox = 9

class Servers(Enum):
    DapsTS2 = "daps-ts-2"
    DemoTS2 = "demo-ts-2"
    DapsTSG2 = "daps-tsg-2"

ClientSoftwareLiveFolderPaths = {
            Environments.HbR : r"\\daps-ts-2\DEMO\Havenbedrijf\RE_Suite_TestJNO",
            Environments.Stek : r"\\daps-ts-2\DEMO\Stek\RE_Suite_TestJNO",
            Environments.Monumentenwacht: r"\\daps-ts-2\DEMO\Monumentenwacht\RE_Suite_TestJNO",
            Environments.DemoSecureRelease : r"\\daps-ts-2\DEMO\Demonstratie\Release_TestJNO",
            Environments.DemoSecurePreRelease : r"\\daps-ts-2\DEMO\Demonstratie\PreRelease_TestJNO",
            Environments.DemoDemoRelease : r"\\demo-ts-2\DEMO\Demonstratie\Release_TestJNO",
            Environments.DemoDemoPreRelease : r"\\demo-ts-2\DEMO\Demonstratie\PreRelease_TestJNO",
            Environments.BIMSpeed : r"\\demo-ts-2\DEMO\BIMSpeed\Re_Suite_TestJNO",
            Environments.Sandbox : r"\\demo-ts-2\DEMO\Sandbox\RE_Suite_TestJNO"
            }
            
ClientSoftwareUpdateFolderPaths = {
            Environments.HbR : r"\\daps-ts-2\DEMO\Havenbedrijf\Updates_TestJNO",
            Environments.Stek : r"\\daps-ts-2\DEMO\Stek\Updates",
            Environments.Monumentenwacht: r"\\daps-ts-2\DEMO\Monumentenwacht\RE_Suite_TestJNO",
            Environments.DemoSecureRelease : r"\\daps-ts-2\DEMO\Demonstratie\Updates\_Release",
            Environments.DemoSecurePreRelease : r"\\daps-ts-2\DEMO\Demonstratie\Updates\_PreRelease",
            Environments.DemoDemoRelease : r"\\demo-ts-2\DEMO\Demonstratie\Updates\_Release",
            Environments.DemoDemoPreRelease : r"\\demo-ts-2\DEMO\Demonstratie\Updates\_PreRelease",
            Environments.BIMSpeed : r"\\demo-ts-2\DEMO\BIMSpeed\Updates_TestJNO",
            Environments.Sandbox : r"\\demo-ts-2\DEMO\Sandbox\Updates_TestJNO"
            }
            
WebServiceLiveFolderPaths = {
            Environments.HbR : r"\\daps-tsg-2\wwwroot\HBR\RE_Suite_WebService_TestJNO",
            Environments.Stek : r"\\daps-tsg-2\wwwroot\stek\WebService_TestJNO",
            Environments.Monumentenwacht: r"\\daps-tsg-2\wwwroot\Monumentenwacht\WebService_TestJNO",
            Environments.DemoSecureRelease : r"\\daps-tsg-2\wwwroot\Demonstratie\Release_TestJNO",
            Environments.DemoSecurePreRelease : r"\\daps-tsg-2\wwwroot\Demonstratie\PreRelease_TestJNO",
            Environments.DemoDemoRelease : r"\\demo-ts-2\wwwroot\Demonstratie\Release_TestJNO",
            Environments.DemoDemoPreRelease : r"\\demo-ts-2\wwwroot\Demonstratie\PreRelease_TestJNO",
            Environments.BIMSpeed : r"\\demo-ts-2\wwwroot\BIMSpeed\RE_Suite_WebService_TestJNO",
            #Environments.Sandbox : r"\\demo-ts-2\DEMO\Sandbox\Updates_TestJNO"
            }
            
WebServiceUpdateFolderPaths = {
            Environments.HbR : r"\\daps-tsg-2\wwwroot\HBR\_update\TestJNO",
            Environments.Stek : r"\\daps-tsg-2\wwwroot\stek\WebService updates",
            Environments.Monumentenwacht: r"\\daps-tsg-2\wwwroot\Monumentenwacht\_updates\TestJNO",
            Environments.DemoSecureRelease : r"\\daps-tsg-2\wwwroot\Demonstratie\Updates\Release_TestJNO",
            Environments.DemoSecurePreRelease : r"\\daps-tsg-2\wwwroot\Demonstratie\PreRelease\WebService_updates",
            Environments.DemoDemoRelease : r"\\demo-ts-2\wwwroot\Demonstratie\Updates\Release_TestJNO",
            Environments.DemoDemoPreRelease : r"\\demo-ts-2\wwwroot\Demonstratie\PreRelease\WebService_updates",
            Environments.BIMSpeed : r"\\demo-ts-2\wwwroot\BIMSpeed\Updates_TestJNO",
            #Environments.Sandbox : r"\\demo-ts-2\DEMO\Sandbox\Updates_TestJNO"
            }