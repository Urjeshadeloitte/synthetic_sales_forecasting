"""Final verification test for weather pipeline."""

from weather import graph

# Run pipeline
print("Running pipeline verification...")
result = graph.invoke({})

# Verify state has all required keys
required_keys = ['raw_weather', 'cleaned_weather', 'features_df', 'train_test_split', 'model', 'forecast_30d', 'metrics', 'outputs_saved']
present_keys = [k for k in required_keys if k in result]
missing_keys = [k for k in required_keys if k not in result]

print('\nPipeline Verification Report')
print('=' * 50)
print(f'Expected keys: {len(required_keys)}')
print(f'Present keys:  {len(present_keys)}')
print(f'Missing keys:  {len(missing_keys)}')
if missing_keys:
    print(f'  Missing: {missing_keys}')
else:
    print('  ✓ All keys present')

print()
print('Data Summary:')
print(f'  Raw weather:      {len(result.get("raw_weather", []))} days')
print(f'  Cleaned weather:  {len(result.get("cleaned_weather", []))} days')
print(f'  Features rows:    {len(result.get("features_df", []))} (after drop first 30)')
print(f'  Train samples:    {len(result.get("train_test_split", {}).get("train", []))}')
print(f'  Test samples:     {len(result.get("train_test_split", {}).get("test", []))}')
print(f'  Forecast days:    {len(result.get("forecast_30d", []))}')
print(f'  Model type:       {type(result.get("model")).__name__}')
print(f'  Outputs saved:    {result.get("outputs_saved")}')

print()
print('Model Metrics:')
metrics = result.get('metrics', {})
for key, value in sorted(metrics.items()):
    if isinstance(value, float):
        print(f'  {key:.<25} {value:.6f}')

print()
print('✓ Pipeline Verification Complete')
print('=' * 50)
