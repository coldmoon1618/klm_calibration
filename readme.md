# klm_calibration

runs on `basf2 release-08-01-07`

 - [calibration_outputdbs](calibration_outputdbs)
    - Output from Airflow for calibration campaigns
 - `generateValidationRoot.py`: Read in outputdb and writes `validation.root`
 - `MakePlots.C`: Use validation.root to make plots

# usage
 
 - download calibration output using [`b2conditionsdb legacydownload`](https://software.belle2.org/development/sphinx/framework/doc/tools/06-b2conditionsdb.html#legacydownload)
```
b2conditionsdb legacydownload <globaltag> -f KLMChannelStatus --run-range expLow runLow expHigh runHigh -c
```
 - run on calibration output and create the `validation.root` file

```
basf2 generateValidationRoot.py dirName/
```

 - create plots

```
python3 MakePlots.py validation.root
```
