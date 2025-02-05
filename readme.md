# klm_calibration

runs on `basf2 release-08-02-00`

 - [calibration_outputdbs](calibration_outputdbs)
    - Output from Airflow for calibration campaigns
 - `generateValidationRoot.py`: Read in outputdb and writes `validation.root`
 - `MakePlots.C`: Use validation.root to make plots

# usage
 
 - download calibration output using 

   - [`gfal-copy`](https://www.mankier.com/1/gfal-copy): setup gbasf2 environment and look at calibration job ticket comment for `gfal-copy` command

   - [`b2conditionsdb legacydownload`](https://software.belle2.org/development/sphinx/framework/doc/tools/06-b2conditionsdb.html#legacydownload)
```
b2conditionsdb legacydownload <globaltag> -f KLMChannelStatus --run-range expLow runLow expHigh runHigh -c
```

 - run on calibration output and create the `validation.root` and `plots.pdf`

```
basf2 klm_channel_status.py <job_path> <input_data_path> <requested_iov> <expert_config>
```
