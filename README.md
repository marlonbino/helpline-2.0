# Helpline 2.0
Start with the following command:

```sh
workon asr
```

# Parakeet ASR
```python
import nemo.collections.asr as nemo_asr
asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(model_name="nvidia/parakeet-tdt-1.1b")
output = asr_model.transcribe(['audio-item.wav'])
print(output[0].text)
```


