
How to run jupyter notebooks remotely (alternative to SLURM method)

Login to the server from your local workstation (i.e. chgr1 or chgr2) and in the same connection do the port forwarding.

Follow these commands
```bash
user@local$ ssh -X -L 8889:localhost:8889 username@remote_host
user@remote_host$ ml Intel IntelMPI Anaconda2
user@remote_host$ cd /path/to/notebooks
user@remote_host$ jupyter notebook --no-browser --port=8889
```
For ACCRE, replace ```user@remote_host``` with ```VUNETID@chgr2.accre.vanderbilt.edu```.

Now open a web browser on your local machine and point it to localhost:8889
