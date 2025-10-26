@echo off
echo ===============================
echo  🚀 Training greetings_model.pt
echo ===============================

set CUDA_VISIBLE_DEVICES=
python ai-test.py train ^
  --csv hello.csv ^
  --text-col content ^
  --out greetings_model.pt ^
  --seq-len 120 ^
  --batch-size 64 ^
  --epochs 10 ^
  --lr 0.003

echo.
echo ====================================
echo ✅ Training finished: greetings_model.pt
echo ====================================
pause
