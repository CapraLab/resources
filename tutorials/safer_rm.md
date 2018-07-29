This note describes how to replace the ```rm``` command with a script that copies everything you delete to a temporary folder (/tmp) that is deleted on every reboot (a fairly rare occurrence). This provides a safety net for when you accidentally delete a file. ACCRE and DORS have nightly backups, but it can be annoying and time consuming to get data back from them.

The script ```trash.pl``` in ```/dors/capra_lab/bin``` acts like the command ```rm```, but it moves files you want to delete to ```/tmp```. This is a directory for storing temporary files that are deleted on reboot, so if you accidentally delete something, you can easily copy it back from there. The script tells you exactly where it has moved the "deleted" files. For example:
> [capraja@chgr2 capraja]$ rm example.txt 
> --------------------------------------------------------------------------------
> trash.pl: example.txt -> /tmp/capraja/Trash/dors/capra_lab/capraja/example.txt
> trash.pl: Note: the trash directory will be auto-deleted every reboot, without warning.
> --------------------------------------------------------------------------------
> [capraja@chgr2 capraja]$


In order to use this script, make sure that the ```/dors/capra_lab/bin``` directory is in your ```PATH``` variable. (If that doesn't make sense, google "setting unix path variable".) Then, add the following lines to the file ```.bashrc``` in your ACCRE home directory:
> ```alias rm="trash.pl"```
> ```alias rrm="'rm'"```

The ```.bashrc``` file is read and executed every time you start a new shell (more or less). 

After creating these aliases, whenever you type ```rm```, the shell will replace it with ```trash.pl```. The second line maps ```rrm``` to ```rm`` in case you want to really delete something. 

NOTE: If you are deleting large files (say >100 Mb), it is better to use the system ```rm``` command (which is now aliased to "rrm.”)

As soon as you log out or re-source your ```.bashrc```, ```trash.pl``` should work. You'll know if it is working because whenever you delete something, you'll see the message above.
