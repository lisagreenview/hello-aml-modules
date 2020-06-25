SupplementatalLearners contains some additional learners that are not shown in the GUI. 

To show them in the GUI or make them work from the commandline, please do either of the following:
- Copy over the dll into the upper level directory (which contains tl.exe/tlc.exe)
- Specify the "Extra Assemblies" path in the GUI to be the full path to the "SupplementalLearners" folder. For commandline specify the "/dll:<path>" option.

SimpleTrainers.dll
------------------
Contains
- PriorPredictor
- RandomPredictor
These are demo trainers which show how can users create there own trainers/predictors.

FilterThenPredict.dll
---------------------
Contains the 'FilterThenPredict' trainer/predictor. 
This takes a base filter trainer that first trains on the data.
Then the 'filter-predictor' is used to filter out the features with weights that are below the specified "threshold".
Then the final trainer is trained on the data with only the 'filtered' features.

StratoLearner.dll
-----------------
Contains the StratoLearner and StratoLearnerRanker trainers.
Stratolearner takes a base trainer and a stratification key (which can either be one of the name or attribute features in the instancesettings)
It then partitions the training data based on the key and trains *multiple* models - one per partition. 
The 'min' paramter specifies the minimum number of instances that need to be part of a 'strata' to consider it as a partition that we train a model for.

ParameterMixer.dll
------------------
Contains the ParameterMixer trainer.
It takes a base trainer (only possible values are LinearSVM and LR) and a data pratitioning  scheme.
The training data is partitioned in the specified partitions and a model is created for each partition.
Finally, the parameters(weights) of all the models are averaged to get a single model.




