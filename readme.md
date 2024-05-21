# klm_calibration

runs on `basf2 release-08-01-03`

 - [calibration_outputdb](calibration_outputdb)
    - Output from Airflow
 - [scripts](scripts)
    - `generateValidationRoot.py`: Read in outputdb and writes `validation.root`
    - `MakePlots.C`: Use validation.root to make plots

# usage

 - run on calibration output and create the `validation.root` file

```
basf2 scripts/generateValidationRoot.py dirName/
```

 - create plots

```
root scripts/MakePlots.C\(\"validation.root\"\)
```
