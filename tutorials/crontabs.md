## crontabs tutorial

crontabs enable every user to setup jobs they'd like to have automatically run at regular intervals. 
[Online How-to](https://help.ubuntu.com/community/CronHowto)


One use for this that we have discussed is to set up nightly automatic commits for project directories using git. Here's an example of how I set one up. 
Type ```crontab -e``` to edit your crontabs.

Enter and save this text:
```bash
MAILTO=""
1 4 * * * cd /dors/capra_lab/projects/enhancer_uniqueness && /usr/local/git/latest/x86_64/gcc46/nonet/bin/git -a -m "daily auto-commit: `date`"
```

This sets up a crontab to run every night at 4:01am that will commit all edited tracked files in the ```enhancer_uniqueness``` project directory with a timestamped message.

(Note that ```crontab -e``` will open whatever the default system editor is---most likely ```vi```. You can set your own default editor using the EDITOR variable.)
