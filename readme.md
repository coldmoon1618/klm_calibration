# klm_calibration

runs on `basf2 release-08-01-07`

 - [calibration_outputdb](calibration_outputdb)
    - Output from Airflow
 - `generateValidationRoot.py`: Read in outputdb and writes `validation.root`
 - `MakePlots.C`: Use validation.root to make plots

# usage

 - run on calibration output and create the `validation.root` file

```
basf2 generateValidationRoot.py dirName/
```

 - create plots

```
root 'MakePlots.C("validation.root")'
```
