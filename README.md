# Public Domain TTS Voice Samples

This repository contains 626 public domain English language audio samples and associated metadata for each file for use with voice cloning based text-to-speech (TTS) models such as Resemble AI's [Chatterbox](https://github.com/resemble-ai/chatterbox), or Kiutai's [Pocket-TTS](https://github.com/kyutai-labs/pocket-tts).

The metadata contained here is also useful for categorizing [Piper](https://github.com/OHF-voice/piper1-gpl) voices that have been trained on the LibriTTS corpus ([en_US-libritts](https://rhasspy.github.io/piper-samples/#en_US-libritts_r-medium)) using the ```piper_id``` field included for each speaker in the metadata. Note that not all voices in Piper's ```en_US-libritts_r-medium``` appear in the metadata due to not being annotated as part of the libriTTS-P corpus.

Check out the demo at [LibriTTS Voice Samples Demo](https://bernardoviotti.github.io/libritts-voice-samples-demo-public/).


# Citation

The samples and metadata here are based on the the LibriTTS-R and LibriTTS-P datasets released under CC BY 4.0 and cited below. The base data corpus is [LibriSpeech](http://www.openslr.org/12/), assembled by Vassil Panayotov with the assistance of Daniel Povey, which is itself derived from public domain recordings published on [LibriVox](https://librivox.org/). Names of individuals who contributed their voices have been anonymized, but they can be found in LibriTTS-R's ```speakers.tsv``` file.

```
@misc{koizumi2023librittsrrestoredmultispeakertexttospeech,
      title={LibriTTS-R: A Restored Multi-Speaker Text-to-Speech Corpus}, 
      author={Yuma Koizumi and Heiga Zen and Shigeki Karita and Yifan Ding and Kohei Yatabe and Nobuyuki Morioka and Michiel Bacchiani and Yu Zhang and Wei Han and Ankur Bapna},
      year={2023},
      eprint={2305.18802},
      archivePrefix={arXiv},
      primaryClass={eess.AS},
      url={https://arxiv.org/abs/2305.18802}, 
}
```

```
@inproceedings{librittsp,
    authors={Masaya Kawamura, Ryuichi Yamamoto, Yuma Shirahata, Takuya Hasumi, Kentaro Tachibana},
    title={LibriTTS-P: A Corpus with Speaking Style and Speaker Identity Prompts for Text-to-Speech and Style Captioning},
    booktitle={Proc. Interspeech 2024},
    month=sep,
    year=2024
}
```
## License
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) inherited from the datasets from which this data was collated.