The raw data from this file has been ommitted, but can be downloaded with the following commands:

```
curl -OL "https://openslr.trmal.net/resources/141/doc.tar.gz"
tar -xf "doc.tar.gz"
rm doc.tar.gz
mv ./LibriTTS_R/speakers.tsv ./
rm -rf ./LibriTTS_R
```

> [WARNING] The following command will downlaod the ```train-clean-360``` set from LibriTTS-R which is a 28GB tarball.

```
curl -OL "https://openslr.trmal.net/resources/141/train_clean_360.tar.gz"
tar -xf ./train_clean_360.tar.gz
rm ./train_clean_360.tar.gz
```

Will download the following files:
```
speakers.tsv 84K
train_clean_360.tar.gz 28GB
```