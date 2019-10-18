This file contains instructions to help you store Anaconda environments on DORS instead of in your ACCRE home directory.
This is useful when you exceed the explicit memory and/or file number limits imposed by ACCRE (which happens frequently if you have multiple environments!).
You can move existing environments too; instructions included below.

### Choose your location

You first want to create or choose a directory to store your conda environments in on DORS.

I chose to put mine in my `users/[name]/resources` directory inside a new directory I called `conda_envs`.
I also created two directories inside `conda_envs` for `env_dirs` and `pkgs`.

*I saved all my existing environments into .yml files BEFORE moving to the next step, just to be safe.*

### Update `.condarc`
Either use the `conda config` commands to update your `.condarc` to now create environments in this location:
```
	conda config --add envs_dirs <path to directory>
	conda config --add pkgs_dirs <path to directory>
```

*OR*, you can update the file manually in your ACCRE home (`~`) directory to point to those new directories, for example:
```
channels:
  - bioconda
  - conda-forge
  - defaults

envs_dirs:
  - /dors/capra_lab/users/YOUR_ID_HERE/DIR_FOR_ENVS/conda_envs/env_dirs

pkgs_dirs:
  - /dors/capra_lab/users/YOUR_ID_HERE/DIR_FOR_ENVS/conda_envs/pkgs
```

### Re-install environments
After this step I re-created all my conda environments from the .yml files (made in step 1) and checked to make sure they were installing in the new place.
Finally I deleted the old `.conda` directory from `~`. (FYI, this deletion took quite a while.)

*Note: You can also do essentially the same thing by creating environments with the `--prefix` option and specifying a path on DORS, but I preferred this solution since I wanted environments saved in one place on DORS by default.*
