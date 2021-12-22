Prerequisites: 

* Python version:
	* Script has been built on Python 3.7.9
* Packages:
	* tkinter
	* ttkwidgets
	* zipfile
	* The unzip mechanism uses psexec. For this PsTools must be installed locally. See documentation here: https://docs.microsoft.com/en-us/sysinternals/downloads/psexec. This is done so that unzip actions on server are handled by the server itself instead of by the local machine
* Servers must be accessible from local machine through their names. E.g. typing \\\\daps-ts-2 in explorer should result in access to the shared folders on server

