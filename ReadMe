# klm_calibration

runs on basf2 release-08-01-03

calibration_outputdb/
    Output from Airflow
Scripts/
    generateValidationRoot.py
        Read in outputdb and writes validation.root
    MakePlots.C
        Use validation.root to make plots

    Note: leave all the plots here and remove the local Mac version of repo

# usage

 - run on calibration output and create the `validation.root` file

```
basf2 scripts/generateValidationRoot.py dirName/
```

 - create plots

```
root scripts/MakePlots.C\(\"validation.root\"\)
```
