# How to Set up a Mac for programming

## If you want to do work locally:
1. Install Xcode from apple store
2. A nice guide to development environment setup: https://github.com/nicolashery/mac-dev-setup
   The following things are especially useful. The rest may not be necessary in the beginning.
     - iTerm2 (better terminal)
     - Homebrew (install and update applications)
     - Git (version control)
     - Sublime Text (text editing)
     - Conda (virtual environments)
     - IPython/Jupyter (interactive coding)
     
Numpy, Scipy are also very useful if you use python. [Conda](https://store.continuum.io/cshop/anaconda/) has all of those and other common python things, as well as packages and installations for other languages. Installation is free.

## If you want to use ACCRE:
1. Get ACCRE account
  See computing section in “Introduction to the Capra Lab” [Note](https://github.com/CapraLab/resources/blob/master/WelcomeInfo.md).
2. Get SAMBA access (If you didn’t get it from the first step.)
  To use SAMBA, select "Connect to Server" under the "Go" menu when on the Desktop, and then enter the server address. The short cut is cmd-K.
  
  To access the capra_lab DORS space use this address: ```smb://mako-smb.its.vanderbilt.edu/capra_lab``` and your VUnet ID. The password for DORS is the e-password, not the ACCRE password.
  
  To access your personal ACCRE directory:Open a helpdesk request on ACCRE website. Include the information of what directories need to be mounted to the local computer via SAMBA. A email contains the temporary SAMBA password and the server address will come. (smb://samba.accre.vanderbilt.edu/<VUnetID>)
3. ACCRE Usage
  Work directly on ACCRE:
    Log in to ACCRE through chgr1 or chgr2 (recommended).
    In terminal, type ```ssh your_vunetid@chgr1.accre.vanderbilt.edu```

The benefits of working directly on ACCRE is that almost everything we normally use is already installed. But the text editor (```nano``` or ```vim```) is not as easy to pick up as Sublime.  If you also want to use the capra lab utilities, edit the ```.bashrc``` file as following:
```bash
nano ~/.bashrc
#Add the following lines to the file:
export PATH=“/dors/capra_lab/bin/:$PATH"
```

Work through SAMBA on the local computer:
Connect to the server.(On desktop, cmd-K. Enter the server address.)
The files on the server will be open in a finder window and can be used as any other local files. The location is ```/Volumes/capra_lab/ (dors)``` or ```/Volumes/vunetid``` (home directory) depending on which server is connected. Then you can operate on the files on the local computer.
