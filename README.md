# Student math score prediction

Train the model from the student dataset and save the fitted preprocessor and
regressor under `artifacts`:

```powershell
python -m pip install -r requirement.txt
python -m src.compoments.data_reader
```

Run the interactive terminal predictor after training:

```powershell
python -m src.pipline.pridiect
```

Enter the prompted student details; the command prints the predicted math score.
The same predictor is available in Python through `PredictionPipeline.predict`.