cd ctr_avazu
pip install -r requirements.txt
mkdir ~/.kaggle
mv kaggle.json ~/.kaggle
kaggle competitions download -c avazu-ctr-prediction
gunzip train.gz
gunzip test.gz
mv train data
mv test data
mv sampleSubmission.gz data
cd ..
nohup python -m ctr_avazu --train ./ctr_avazu/data/train --test ./ctr_avazu/data/test > log 2>&1 &
kaggle competitions submit -f ctr_avazu/submission.csv -m jasoncoding13 -q avazu-ctr-prediction
cd ..